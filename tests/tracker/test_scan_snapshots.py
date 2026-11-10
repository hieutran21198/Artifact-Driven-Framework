"""Seeded browser proofs of immutable scan inputs and truthful read outcomes."""
import json

from tests.tracker.browser import BrowserTestCase


SEED = r"""() => {
  window.results = [];
  window.analyses = [];
  window.requests = [];
  window.sources = {};
  window.hooks = {};
  window.digestVersion = 'seed-analyzer';
  window.workspace = {type:'github',repo:'team/knowledge',branch:'main',token:'',parts:{}};
  config = {version:2,workspaces:[workspace],selected:workspace.repo};
  $('ws').innerHTML = '<option>team/knowledge</option>';
  shown = null;
  loading = false;
  drawSite = () => {};
  const originalCoverage = window.baseDrawCoverage || (window.baseDrawCoverage = drawCoverage);
  drawCoverage = b => { results.push(JSON.parse(JSON.stringify(b))); originalCoverage(b); };
  run = async files => { analyses.push(JSON.parse(JSON.stringify(files))); return ['<html></html>', '']; };
  analyzer = async () => ({digest:digestVersion,python_version:'3.13.2'});
  refs = async () => ['main','other'];
  window.seed = (repo, conf, files={}, commit='abcdef0123456789012345678901234567890123', ref='main') => {
    const contents = {...files};
    if (conf !== null) contents['artifact-driven.json'] = JSON.stringify(conf);
    sources[repo+'@'+ref] = {commit,contents};
  };
  window.knowledge = {'docs/software-knowledges/goals/read.md':'# Goal: Read\n\n| G-READ-1 | Read | F-READ-1 |'};
  window.fetch = async (url, options={}) => {
    const request = {url:String(url),authorization:options.headers?.Authorization || null};
    requests.push(request);
    if (hooks.before) await hooks.before(request);
    let body, status=200;
    const u = new URL(url);
    if (u.hostname === 'api.github.com') {
      const match = /^\/repos\/([^/]+\/[^/]+)\/(commits|git\/trees|git\/blobs)\/(.+)$/.exec(u.pathname);
      if (!match) throw Error('Unexpected API path: '+u.pathname);
      const [,repo,kind,value] = match;
      if (kind === 'commits') {
        const s = sources[repo+'@'+decodeURIComponent(value === 'HEAD' ? 'main' : value)];
        if (!s) status=404;
        else body={sha:s.commit,commit:{tree:{sha:s.commit}}};
      } else {
        const s = Object.entries(sources).find(([k,s]) => k.startsWith(repo+'@') && (kind === 'git/trees' ? s.commit===value : Object.entries(s.contents).some(([p,t]) => btoa(unescape(encodeURIComponent(t)))===value)))?.[1];
        if (!s) status=404;
        else if (kind === 'git/trees') body={tree:Object.entries(s.contents).map(([path,text])=>({type:'blob',path,sha:btoa(unescape(encodeURIComponent(text)))}))};
        else body={content:value};
      }
    } else if (u.hostname === 'raw.githubusercontent.com') {
      const [,owner,repo,commit,...path] = u.pathname.split('/');
      const s=Object.entries(sources).find(([k,s])=>k.startsWith(owner+'/'+repo+'@')&&s.commit===commit)?.[1];
      body=s?.contents[path.map(decodeURIComponent).join('/')];
      if (body === undefined) status=404;
    } else throw Error('Unexpected fetch: '+url);
    if (hooks.fail && hooks.fail(request)) status=503;
    return {ok:status===200,status,headers:{get:()=>null},json:async()=>body,text:async()=>body};
  };
}"""


class ScanSnapshotTests(BrowserTestCase):
    def setUp(self):
        super().setUp()
        self.open_tracker()
        self.page.evaluate(SEED)

    def test_TRK_15_F_VIEW_17_captures_configuration_refs_and_credentials(self):
        """TRK-15, TRK-12, TRK-6, F-VIEW-17: later edits stay pending."""
        result = self.page.evaluate(r"""async () => {
          seed(workspace.repo, {}, knowledge);
          seed('team/service', null, {'one_test.js':'TRK-1'});
          workspace.token='team'; workspace.parts={api:{ref:'main',token:'team'}};
          workspace.configuration={services:{api:{tests:{folder:'api',repository:'team/service'}}}};
          setToken('team','first-value');
          let release, started;
          const gate=new Promise(r=>release=r), ready=new Promise(r=>started=r);
          hooks.before=async q=>{if(q.url.includes('/commits/main')&&q.url.includes('knowledge')){started();await gate;}};
          const pending=load(); await ready;
          workspace.branch='other'; workspace.parts.api.ref='other'; delete workspace.configuration;
          setToken('team','second-value'); release(); await pending;
          return {b:results[0],requests,dirty:$('status').textContent};
        }""")
        self.assertEqual(result['b']['provenance']['configuration']['source'], 'browser_override')
        self.assertEqual(result['b']['provenance']['parts'][0]['source']['requested_ref'], 'main')
        self.assertTrue(all(q['authorization'] == 'Bearer first-value' for q in result['requests']))
        self.assertNotIn('first-value', json.dumps(result['b']))
        self.assertIn('Press Load', result['dirty'])

    def test_TRK_15_F_VIEW_18_obsolete_success_and_failure_are_ignored(self):
        """TRK-15, F-VIEW-18: a late success or error cannot publish."""
        for failure in (False, True):
            with self.subTest(failure=failure):
                self.page.evaluate(SEED)
                result=self.page.evaluate(r"""async failure => {
                  seed(workspace.repo, {}, knowledge); seed(workspace.repo, {}, knowledge, '1234567890123456789012345678901234567890','other');
                  let release, started;
                  const gate=new Promise(r=>release=r),ready=new Promise(r=>started=r);
                  hooks.before=async q=>{if(q.url.includes('/commits/main')){started();await gate;if(failure)throw Error('obsolete error');}};
                  const old=load(); await ready; workspace.branch='other'; await load(); release(); await old;
                  return {results,status:$('status').textContent,disabled:$('load').disabled};
                }""", failure)
                self.assertEqual(len(result['results']),1)
                self.assertEqual(result['results'][0]['provenance']['workspace']['requested_ref'],'other')
                self.assertNotIn('obsolete error',result['status'])
                self.assertFalse(result['disabled'])

    def test_TRK_16_F_VIEW_20_F_VIEW_23_partial_part_failure_is_atomic_and_retried(self):
        """TRK-3, TRK-5, TRK-9, TRK-16, F-VIEW-20, F-VIEW-23."""
        result=self.page.evaluate(r"""async () => {
          seed(workspace.repo,{services:{broken:{tests:{folder:'broken'}},good:{tests:{folder:'good'}}}},
            {...knowledge,'broken/one_test.js':'TRK-1','broken/two_test.js':'TRK-2','good/ok_test.js':'TRK-3'});
          hooks.fail=q=>q.url.endsWith('/broken/two_test.js'); await load();
          hooks.fail=null; await load();
          return {results,analyses,warning:$('left-out').textContent};
        }""")
        self.assertEqual([p['status'] for p in result['results'][0]['provenance']['parts']],['failed','complete'])
        self.assertNotIn('broken/one_test.js',result['analyses'][0])
        self.assertIn('good/ok_test.js',result['analyses'][0])
        self.assertEqual([p['status'] for p in result['results'][1]['provenance']['parts']],['complete','complete'])
        self.assertIn('broken/one_test.js',result['analyses'][1])
        self.assertNotIn('503',result['warning'])

    def test_TRK_16_F_VIEW_21_missing_groups_remain_distinct_and_cacheable(self):
        """TRK-2, TRK-3, TRK-5, TRK-16, F-VIEW-21: missing is not failed."""
        result=self.page.evaluate(r"""async () => {
          seed(workspace.repo,{services:{same:{},good:{tests:{folder:'good'}}},clients:{same:{tests:{folder:'absent'}}},e2e:{folder:'e2e'}},
            {...knowledge,'good/ok_test.js':'TRK-3','e2e/README.md':'No matching tests'});
          await load(); await load(); return {b:results[1],runs:analyses.length};
        }""")
        parts=result['b']['provenance']['parts']
        self.assertEqual([(p['group'],p['name'],p['status']) for p in parts],
                         [('service','same','missing'),('service','good','complete'),('client','same','missing'),('e2e','e2e','missing')])
        self.assertEqual(len({p['reason'] for p in parts if p['status']=='missing'}),3)
        self.assertEqual(result['runs'],1)

    def test_TRK_5_F_VIEW_22_full_commits_and_current_alias_provenance(self):
        """TRK-5, TRK-17, F-VIEW-22: short prefixes never identify a build."""
        result=self.page.evaluate(r"""async () => {
          seed(workspace.repo,{},knowledge,'abcdef0000000000000000000000000000000000');
          await load();
          seed(workspace.repo,{},knowledge,'abcdef0111111111111111111111111111111111','other');
          workspace.branch='other'; await load();
          seed(workspace.repo,{},knowledge,'abcdef0111111111111111111111111111111111','tag');
          workspace.branch='tag'; await load(); return {results,runs:analyses.length};
        }""")
        self.assertEqual(result['runs'],2)
        self.assertNotEqual(result['results'][0]['provenance']['workspace']['commit'],result['results'][1]['provenance']['workspace']['commit'])
        self.assertEqual(result['results'][2]['provenance']['workspace']['requested_ref'],'tag')

    def test_TRK_9_F_VIEW_29_fatal_read_preserves_previous_build_and_retries(self):
        """TRK-9, TRK-15, TRK-17, F-VIEW-29: old coverage keeps its identity."""
        result=self.page.evaluate(r"""async () => {
          seed(workspace.repo,{},knowledge); await load();
          seed(workspace.repo,{}, {...knowledge,'docs/software-knowledges/new.md':'TRK-1'}, 'ffffffffffffffffffffffffffffffffffffffff','other');
          workspace.branch='other'; hooks.fail=q=>q.url.endsWith('/new.md'); await load();
          const failed={count:results.length,status:$('status').textContent,shown:shown.id,label:shown.label};
          hooks.fail=null; await load(); return {failed,results,status:$('status').textContent};
        }""")
        self.assertEqual(result['failed']['count'],1)
        self.assertIn('abcdef0',result['failed']['label'])
        self.assertIn('503',result['failed']['status'])
        self.assertEqual(len(result['results']),2)
        self.assertNotIn('503',result['status'])

    def test_TRK_15_F_VIEW_27_loaded_configuration_owns_parts(self):
        """TRK-2, TRK-15, F-VIEW-27: no settings visit is required."""
        result=self.page.evaluate(r"""async () => {
          seed(workspace.repo,{services:{old:{tests:{folder:'old'}}}}, {...knowledge,'old/a_test.js':'TRK-1'});
          seed(workspace.repo,{clients:{added:{tests:{folder:'new'}}}}, {...knowledge,'new/a_test.js':'TRK-2'},'ffffffffffffffffffffffffffffffffffffffff','other');
          await load(); workspace.branch='other'; await load();
          return {b:results[1],controls:$('part-refs').textContent};
        }""")
        self.assertEqual(result['b']['provenance']['parts'][0]['name'],'added')
        self.assertIn('added',result['controls'])
        self.assertNotIn('old',result['controls'])

    def test_TRK_5_F_VIEW_28_configuration_and_analyzer_identity_invalidate_cache(self):
        """TRK-5, TRK-12, TRK-17, F-VIEW-28: all analysis inputs identify reuse."""
        result=self.page.evaluate(r"""async () => {
          seed(workspace.repo,{},knowledge); await load();
          workspace.configuration={standards:['CUSTOM']}; await load();
          digestVersion='different-analyzer'; await load();
          delete workspace.configuration; await load();
          return {results,runs:analyses.length};
        }""")
        self.assertEqual(result['runs'],4)
        self.assertNotEqual(result['results'][0]['provenance']['configuration']['digest'],result['results'][1]['provenance']['configuration']['digest'])
        self.assertNotEqual(result['results'][1]['provenance']['analyzer']['digest'],result['results'][2]['provenance']['analyzer']['digest'])
        self.assertFalse(result['results'][3]['overridden'])

    def test_TRK_15_F_VIEW_19_late_refs_and_configuration_cannot_restore_old_controls(self):
        """TRK-15, F-VIEW-19, F-VIEW-27: reversed responses keep current choices."""
        result=self.page.evaluate(r"""async () => {
          let release;
          const gate=new Promise(r=>release=r);
          refs=async repo=>{if(repo==='team/old'){await gate;return ['obsolete'];}return ['current'];};
          workspace.configuration={services:{same:{tests:{folder:'one',repository:'team/old'}}}};
          drawPicker();
          workspace.configuration={services:{same:{tests:{folder:'two',repository:'team/new'}}}};
          workspace.parts={same:{ref:'current',token:'new'}};
          drawPicker(); await Promise.resolve(); release(); await Promise.resolve(); await Promise.resolve();
          const options=document.querySelector('select[data-part-ref="same"]').textContent;
          const selected=document.querySelector('select[data-part-ref="same"]').value;
          delete workspace.configuration;
          confOf[workspace.repo]={services:{same:{tests:{folder:'one',repository:'team/old'}}}};
          confKeys[workspace.repo]=configPick(workspace);drawPicker();
          // A settings response changed the source config before its final redraw.
          confOf[workspace.repo]={services:{same:{tests:{folder:'two',repository:'team/new'}}}};
          await Promise.resolve();await Promise.resolve();await Promise.resolve();
          return {options,selected,configurationOptions:document.querySelector('select[data-part-ref="same"]').textContent};
        }""")
        self.assertIn('current',result['options'])
        self.assertNotIn('obsolete',result['options'])
        self.assertEqual(result['selected'],'current')
        self.assertNotIn('obsolete',result['configurationOptions'])

    def test_TRK_8_F_VIEW_26_local_working_copy_reloads_and_reports_missing_and_failed(self):
        """TRK-8, TRK-16, TRK-17, F-VIEW-26: Git is context, not a snapshot."""
        result=self.page.evaluate(r"""async () => {
          workspace={type:'local',name:'seed-folder'}; config.workspaces=[workspace];config.selected='local:seed-folder';
          $('ws').innerHTML='<option>local:seed-folder</option>';
          const files={...knowledge,'.git/HEAD':'ref: refs/heads/topic',
            'artifact-driven.json':JSON.stringify({skip:['ignored'],services:{api:{tests:{folder:'api'}},missing:{tests:{folder:'missing'}}}}),
            'api/one_test.js':'TRK-1','api/two_test.js':'TRK-2',
            'docs/software-knowledges/ignored/hidden.md':'TRK-9','api/node_modules/vendor_test.js':'TRK-9'};
          let broken=true,reads=0;
          picked[workspace.name]=new Map(Object.keys(files).map(path=>[path,{text:async()=>{
            reads++;if(broken&&path==='api/two_test.js')throw Error('disk read failed');return files[path];
          }}]));
          freshPicked.add(workspace.name);
          pickFiles=async()=>({name:workspace.name,files:picked[workspace.name]});
          await load(); const firstReads=reads;
          broken=false;files['api/one_test.js']='TRK-3';await load();
          return {results,analyses,firstReads,reads};
        }""")
        first,second=result['results']
        self.assertEqual(first['provenance']['workspace'],{'kind':'working_copy','folder':'seed-folder','git_label':'topic'})
        self.assertEqual([p['status'] for p in first['provenance']['parts']],['failed','missing'])
        self.assertNotIn('api/one_test.js',result['analyses'][0])
        self.assertEqual(result['analyses'][1]['api/one_test.js'],'TRK-3')
        self.assertNotIn('docs/software-knowledges/ignored/hidden.md',result['analyses'][1])
        self.assertNotIn('api/node_modules/vendor_test.js',result['analyses'][1])
        self.assertGreater(result['reads'],result['firstReads'])
        self.assertIn('working copy',second['label'])

    def test_TRK_17_F_VIEW_23_unresolved_repository_is_failed_then_retried(self):
        """TRK-5, TRK-9, TRK-17, F-VIEW-23: unavailable commits are not guessed."""
        result=self.page.evaluate(r"""async () => {
          seed(workspace.repo,{services:{api:{tests:{folder:'api',repository:'team/api@main'}}}},knowledge);
          await load(); seed('team/api',null,{'one_test.js':'TRK-1'},'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb');
          await load(); return {results,analyses};
        }""")
        first=result['results'][0]['provenance']['parts'][0]
        self.assertEqual(first['status'],'failed')
        self.assertIsNone(first['source']['commit'])
        self.assertIn('token',first['reason'])
        self.assertEqual(result['results'][1]['provenance']['parts'][0]['status'],'complete')
        self.assertIn('api/one_test.js',result['analyses'][1])

    def test_TRK_9_F_VIEW_29_configuration_failure_keeps_identity_and_recovers(self):
        """TRK-9, TRK-12, F-VIEW-29: fatal configuration reads are retryable."""
        result=self.page.evaluate(r"""async () => {
          seed(workspace.repo,{},knowledge);await load();
          seed(workspace.repo,{standards:['CUSTOM']},knowledge,'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb','other');
          workspace.branch='other';hooks.fail=q=>q.url.endsWith('/artifact-driven.json');await load();
          const failed={count:results.length,label:shown.label,status:$('status').textContent};
          hooks.fail=null;await load();return {failed,results};
        }""")
        self.assertEqual(result['failed']['count'],1)
        self.assertIn('abcdef0',result['failed']['label'])
        self.assertIn('503',result['failed']['status'])
        self.assertEqual(result['results'][1]['provenance']['configuration']['value'],{'standards':['CUSTOM']})

    def test_TRK_12_F_VIEW_15_reused_analysis_keeps_current_configuration_source(self):
        """TRK-5, TRK-12, F-VIEW-15: restore never relabels an old build."""
        result=self.page.evaluate(r"""async () => {
          seed(workspace.repo,{},knowledge);workspace.configuration={};await load();
          delete workspace.configuration;
          const before=results[0].overridden;await load();return {before,results,runs:analyses.length};
        }""")
        self.assertTrue(result['before'])
        self.assertEqual(result['runs'],1)
        self.assertEqual(result['results'][0]['provenance']['configuration']['source'],'browser_override')
        self.assertEqual(result['results'][1]['provenance']['configuration']['source'],'workspace')

    def test_TRK_15_F_VIEW_27_late_settings_configuration_cannot_replace_loaded_parts(self):
        """TRK-15, F-VIEW-27: a delayed settings response is not authoritative."""
        result=self.page.evaluate(r"""async () => {
          let release,started;const gate=new Promise(r=>release=r),ready=new Promise(r=>started=r);
          checkWorkspace=async (w,apply)=>{started();await gate;apply({services:{obsolete:{tests:{folder:'old'}}}});return ['on','Connected'];};
          const check=checkOne(workspace);await ready;
          seed(workspace.repo,{services:{current:{tests:{folder:'new'}}}}, {...knowledge,'new/a_test.js':'TRK-2'});
          await load();release();await check;
          return {controls:$('part-refs').textContent,configuration:effectiveConf(workspace)};
        }""")
        self.assertIn('current',result['controls'])
        self.assertNotIn('obsolete',result['controls'])
        self.assertIn('current',result['configuration']['services'])

    def test_TRK_5_F_VIEW_29_incomplete_analyzer_initialization_is_not_reused(self):
        """TRK-5, TRK-9, TRK-17, F-VIEW-29: retry a failed analyzer file read."""
        result=self.page.evaluate(r"""async () => {
          pyodide=null;pythonReady=null;analyzerIdentity=null;
          let starts=0,failed=true;
          loadPyodide=async()=>{starts++;return {globals:{set(){}},runPython:()=> '3.13.2'};};
          fetch=async path=>({ok:!(failed&&path.endsWith('site.html')),status:failed?503:200,text:async()=>String(path)});
          let error;try{await python();}catch(e){error=e.message;}
          const kept=!!pyodide;failed=false;await python();
          return {starts,error,kept,identity:analyzerIdentity};
        }""")
        self.assertEqual(result['starts'],2)
        self.assertFalse(result['kept'])
        self.assertIn('site.html',result['error'])
        self.assertTrue(result['identity']['digest'].startswith('sha256:'))
        self.assertEqual(result['identity']['python_version'],'3.13.2')


    def test_SYS_5_TRK_2_source_configuration_keeps_script_parsing_semantics(self):
        """SYS-5, TRK-2: source extensions, null options and absent tests remain valid."""
        result=self.page.evaluate(r"""async () => {
          const source={extension:{flag:true},services:{empty:{tests:{}}},site:null,e2e:null};
          seed(workspace.repo,source,knowledge);await load();
          const accepted=results[0];
          workspace.configuration=source;await load();
          const overrideError=failedLoad;
          delete workspace.configuration;
          for (const [ref,text] of [['bad-json','{oops'],['bad-type','[]']]) {
            seed(workspace.repo,{},knowledge,ref.padEnd(40,'0'),ref);
            sources[workspace.repo+'@'+ref].contents['artifact-driven.json']=text;
            workspace.branch=ref;await load();
          }
          return {accepted,overrideError,count:results.length,label:shown.label,error:failedLoad};
        }""")
        self.assertEqual(result['accepted']['provenance']['configuration']['value']['extension'],{'flag':True})
        self.assertEqual(result['accepted']['provenance']['parts'][0]['status'],'missing')
        self.assertIn('not a configuration key',result['overrideError']['error'])
        self.assertEqual(result['count'],1)
        self.assertIn('abcdef0',result['label'])
        self.assertIn('must be an object',result['error']['error'])

    def test_TRK_8_F_VIEW_26_directory_input_reenumerates_and_preserves_identity_on_cancel(self):
        """TRK-8, TRK-15, F-VIEW-26: new membership needs a fresh selection."""
        result=self.page.evaluate(r"""async () => {
          workspace={type:'local',name:'seed-folder-2',folderName:'seed-folder'};
          config.workspaces=[workspace];config.selected='local:seed-folder-2';$('ws').innerHTML='<option>local:seed-folder-2</option>';
          const files={...knowledge,'artifact-driven.json':JSON.stringify({services:{api:{tests:{folder:'api'}}}})};
          const selection=extra=>new Map(Object.entries({...files,...extra}).map(([path,text])=>[path,{text:async()=>text}]));
          picked[workspace.name]=selection({'api/old_test.js':'TRK-1'});freshPicked.add(workspace.name);
          let prompts=0,next={name:'seed-folder',files:selection({'api/new_test.js':'TRK-2'})};
          pickFiles=async()=>{prompts++;return next;};
          await load();const firstPrompts=prompts;await load();
          next=null;await load();const cancellation=failedLoad.error;
          next={name:'different-folder',files:selection({'api/wrong_test.js':'TRK-3'})};await load();
          return {results,analyses,prompts,firstPrompts,cancellation,mismatch:failedLoad.error};
        }""")
        self.assertEqual(result['firstPrompts'],0)
        self.assertEqual(result['prompts'],3)
        self.assertEqual(len(result['results']),2)
        self.assertIn('api/old_test.js',result['analyses'][0])
        self.assertNotIn('api/old_test.js',result['analyses'][1])
        self.assertIn('api/new_test.js',result['analyses'][1])
        self.assertEqual(result['results'][1]['provenance']['workspace']['folder'],'seed-folder')
        self.assertIn('cancelled',result['cancellation'])
        self.assertIn('different-folder',result['mismatch'])

    def test_TRK_17_http_digest_fallback_uses_initialized_runtime(self):
        """TRK-10, TRK-17: HTTP hosts can hash without Web Crypto or recursion."""
        result=self.page.evaluate(r"""async () => {
          const text='Cấu hình ☃ / analyzer π';const expected=await digest(text);
          const original=Object.getOwnPropertyDescriptor(crypto,'subtle');
          const seen=[],values=new Map();
          const runtime={globals:{set:(k,v)=>values.set(k,v),delete:k=>values.delete(k)},
            runPython:code=>{seen.push({code,value:values.get('_digest_input')});return expected;}};
          Object.defineProperty(crypto,'subtle',{configurable:true,value:undefined});
          let actual;
          try {actual=await digest(text,runtime);} finally {
            if(original)Object.defineProperty(crypto,'subtle',original);else delete crypto.subtle;
          }
          return {actual,expected,seen,leftover:values.size};
        }""")
        self.assertEqual(result['actual'],result['expected'])
        self.assertEqual(result['seen'][0]['value'],'Cấu hình ☃ / analyzer π')
        self.assertIn('hashlib.sha256',result['seen'][0]['code'])
        self.assertEqual(result['leftover'],0)


PARITY_CONFIGURATION = {
    'services': {'failed': {'tests': {'folder': 'failed'}},
                 'good': {'tests': {'folder': 'good'}}, 'missing': {}},
    'clients': {'web': {'tests': {'folder': 'web', 'glob': '**/*.spec.js'}}},
    'e2e': {'folder': 'e2e'},
}
PARITY_FILES = {
    'docs/software-knowledges/system/requirements.md': '# Requirements\n\n| ID | Requirement |\n| --- | --- |\n| SYS-4 | Read only. |\n| SYS-6 | No tests run. |\n',
    'docs/software-knowledges/goals/view.md': '# Goal: Read\n\n| ID | Criterion | Proven by |\n| --- | --- | --- |\n| G-VIEW-1 | Read coverage. | F-VIEW-1 |\n',
    'docs/software-knowledges/flows/view.md': '# View\n\n| ID | Given | When | Then | Rules |\n| --- | --- | --- | --- | --- |\n| F-VIEW-1 | Files. | Read. | Coverage. | TRK-1, TRK-2 |\n',
    'docs/software-knowledges/artifacts/tracker/specification.md': '# Tracker\n\n| ID | Rule | Error |\n| --- | --- | --- |\n| TRK-1 | Read. | — |\n| TRK-2 | Analyze. | — |\n',
    'failed/one_test.js': '// TRK-2 SYS-6',
    'failed/two_test.js': '// TRK-2',
    'good/one_test.js': '// G-VIEW-1 F-VIEW-1 TRK-1 SYS-4',
    'web/one.spec.js': '// TRK-1',
    'e2e/README.md': '# No matching tests',
}


class CoverageParityTests(BrowserTestCase):
    def route_request(self, route):
        # The production browser runtime is pinned; every repository response is seeded.
        if route.request.url.startswith('https://cdn.jsdelivr.net/pyodide/v0.26.4/full/'):
            route.continue_()
        else:
            super().route_request(route)

    def test_TRK_3_F_VIEW_5_real_browser_analysis_matches_cli_included_files(self):
        """TRK-3, TRK-17, F-VIEW-5: actual Pyodide and CLI count the same IDs."""
        from tests.scripts.workspace import Workspace
        self.open_tracker()
        self.page.evaluate('() => { window.realRun=run; window.realAnalyzer=analyzer; window.realFetch=fetch; }')
        self.page.evaluate(SEED)
        result=self.page.evaluate(r"""async ({configuration,files}) => {
          const mockFetch=fetch;
          fetch=(url,...args)=>/^https:\/\/(api.github.com|raw.githubusercontent.com)\//.test(String(url))
            ? mockFetch(url,...args) : realFetch(url,...args);
          run=async (...args)=>{analyses.push(args[0]);return realRun(...args);}; analyzer=realAnalyzer;
          seed(workspace.repo,configuration,files);hooks.fail=q=>q.url.endsWith('/failed/two_test.js');
          await load();return {b:results[0],files:analyses[0],error:failedLoad};
        }""", {'configuration':PARITY_CONFIGURATION,'files':PARITY_FILES})
        self.assertIsNone(result['error'])
        expected_files={path:text for path,text in PARITY_FILES.items()
                        if path.startswith('docs/') or path.startswith('good/') or path.endswith('.spec.js')}
        expected_files['artifact-driven.json']=json.dumps(PARITY_CONFIGURATION,separators=(',',':'))
        self.assertEqual(result['files'],expected_files)
        ws=Workspace(PARITY_CONFIGURATION)
        self.addCleanup(ws.close)
        for path,text in expected_files.items():
            ws.write(path,text)
        cli=ws.run('impact.py','--coverage')
        self.assertEqual(cli.returncode,0,cli.stderr)
        self.assertEqual(result['b']['coverage'],cli.stdout)
        self.assertIn('rules 1/2',cli.stdout)
        self.assertEqual(result['b']['provenance']['parts'][0]['status'],'failed')
        self.assertTrue(result['b']['provenance']['analyzer']['digest'].startswith('sha256:'))

    def test_F_VIEW_31_TST_4_flow_rule_browser_cli_parity(self):
        """F-VIEW-31, TST-4, TRK-17: real trusted parser counts rules, not scenario proof."""
        from tests.scripts.test_site import flow_rule_workspace
        ws = flow_rule_workspace()
        self.addCleanup(ws.close)
        configuration = {"services": {"web": {"tests": {"folder": "tests", "glob": "*.py"}}}}
        ws.write("artifact-driven.json", json.dumps(configuration))
        ws.write("tests/rules.py", "# FR-LOCAL-1 FR-SHARED-1 FR-LEGACY-1 TH-1\n")
        files = {str(p.relative_to(ws.root)): p.read_text() for p in ws.root.rglob("*") if p.is_file()}
        # A workspace's parser-shaped module must never enter the trusted closure.
        files["flow_rules.py"] = "raise RuntimeError('untrusted parser executed')"
        self.open_tracker()
        result = self.page.evaluate("""async files => {
          const [html,coverage]=await run(files,'flow-rules');
          const runtime=await python();
          return {html,coverage,sources:SCRIPTS,
            parser:runtime.runPython('import flow_rules; flow_rules.__file__')};
        }""", files)
        cli = ws.run("impact.py", "--coverage")
        self.assertEqual(cli.returncode, 0, cli.stderr)
        self.assertEqual(result["coverage"], cli.stdout)
        self.assertIn("rules 4/4", cli.stdout)
        self.assertIn("scenarios 0/1", cli.stdout)
        self.assertIn("flow_rules.py", result["sources"])
        self.assertEqual(result["parser"], "/analyzer/flow_rules.py")
        self.assertIn('"flowRules":', result["html"])

    def test_TRK_17_HTTP_real_hashlib_bootstrap_and_failed_runtime_retry(self):
        """TRK-5, TRK-10, TRK-17: real stdlib hashing matches Web Crypto on HTTP."""
        self.open_tracker()
        result=self.page.evaluate(r"""async () => {
          const text='Cấu hình ☃ / analyzer π';const expected=await digest(text);
          const descriptor=Object.getOwnPropertyDescriptor(crypto,'subtle');
          const realLoad=loadPyodide,realFetch=fetch;let starts=0,fail=true;
          loadPyodide=async(...args)=>{starts++;return realLoad(...args);};
          fetch=(url,...args)=>fail&&String(url).endsWith('/site.html')
            ? Promise.resolve(new Response('unavailable',{status:503})) : realFetch(url,...args);
          Object.defineProperty(crypto,'subtle',{configurable:true,value:undefined});
          try {
            let failure;try{await python();}catch(e){failure=e.message;}
            const partialKept=!!pyodide;fail=false;await python();
            return {actual:await digest(text),expected,starts,failure,partialKept,identity:analyzerIdentity};
          } finally {
            if(descriptor)Object.defineProperty(crypto,'subtle',descriptor);else delete crypto.subtle;
            fetch=realFetch;loadPyodide=realLoad;
          }
        }""")
        self.assertEqual(result['actual'],result['expected'])
        self.assertEqual(result['starts'],2)
        self.assertFalse(result['partialKept'])
        self.assertIn('site.html',result['failure'])
        self.assertTrue(result['identity']['digest'].startswith('sha256:'))

    def test_SYS_6_TRK_2_workspace_modules_are_data_and_staging_cannot_escape(self):
        """SYS-6, TRK-2: trusted imports never execute staged workspace modules."""
        self.open_tracker()
        files={path:text for path,text in PARITY_FILES.items() if path.startswith('docs/')}
        files['artifact-driven.json']=json.dumps({'services':{'untrusted':{'tests':{'folder':'scripts','glob':'**/*.py'}}}})
        files['scripts/datetime.py']="import js\njs.window.qaExecutionMarker='workspace-module-executed'\n# TRK-1 G-VIEW-1 F-VIEW-1\n"
        files['scripts/project.py']='# TRK-2\n'
        files['scripts/flow_rules.py']="import js\njs.window.qaExecutionMarker='workspace-parser-executed'\n"
        result=self.page.evaluate(r"""async files => {
          delete window.qaExecutionMarker;
          const [html,coverage]=await run(files,'seed');
          const runtime=await python();
          const before=runtime.runPython('import os, sys; (os.getcwd(), tuple(sys.path))').toJs();
          const errors=[];
          for (const path of ['/outside.py','../outside.py','scripts/../../outside.py','./artifact-driven.json','bad\u0000.py']) {
            try {await run({...files,[path]:'# data'},'invalid');errors.push(null);} catch(e){errors.push(String(e));}
          }
          const after=runtime.runPython('import os, sys; (os.getcwd(), tuple(sys.path))').toJs();
          const escaped=runtime.runPython('from pathlib import Path; Path("/outside.py").exists()');
          const [,recovered]=await run(files,'retry');
          return {html,coverage,recovered,errors,before,after,escaped,marker:window.qaExecutionMarker || null};
        }""", files)
        self.assertIsNone(result['marker'])
        self.assertIn('rules 2/2',result['coverage'])
        self.assertEqual(result['coverage'],result['recovered'])
        self.assertTrue(all(result['errors']))
        self.assertEqual(result['before'],result['after'])
        self.assertFalse(result['escaped'])

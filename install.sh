#!/bin/sh
# Creates an Artifact Driven workspace in a new folder: the framework's shared
# files, and the sample of template/ in place of the framework's own knowledge.
#
#   install.sh <folder> [ref]
#
# ref is a branch, tag or commit of the framework, main by default.
# AD_SOURCE=<folder> copies from a clean local copy of the framework instead of
# downloading it.
set -eu

dest=${1:?usage: install.sh <folder> [ref]}
ref=${2:-main}
if [ -e "$dest" ]; then
  echo "install.sh: $dest already exists" >&2
  exit 1
fi

# The workspace is made in a new folder beside the one given, and takes the
# given name only when it is complete, so a creation that fails leaves no
# folder (WS-9). Whatever was downloaded goes too (WS-7).
download=""
build=""
cleanup() {
  [ -z "$download" ] || rm -rf "$download"
  [ -z "$build" ] || rm -rf "$build"
}
trap cleanup EXIT

src=${AD_SOURCE:-}
if [ -z "$src" ]; then
  download=$(mktemp -d)
  src=$download
  curl -fsSL "https://codeload.github.com/hieutran21198/Artifact-Driven-Framework/tar.gz/$ref" |
    tar -xz -C "$src" --strip-components=1
fi

parent=$(dirname "$dest")
mkdir -p "$parent"
build=$(mktemp -d "$parent/.install.XXXXXX")
# mktemp makes the folder for its owner only; give it the usual permissions.
chmod "$(printf '%o' $(( 0777 & ~$(umask) )))" "$build"

copy() {
  mkdir -p "$build/$(dirname "$2")"
  cp -R "$src/$1" "$build/$2"
}

# The shared files, as the framework has them.
for path in .agents .claude .editorconfig .gitignore AGENTS.md CLAUDE.md CONTRIBUTING.md \
  docs scripts services/README.md apps/README.md e2e/README.md; do
  copy "$path" "$path"
done

# The sample replaces what belongs to the framework itself.
rm -rf "$build/docs/software-knowledges"
for path in README.md artifact-driven.json docs/software-knowledges docs/architecture/domain-map.md \
  services/README.md apps/README.md; do
  rm -rf "${build:?}/$path"
  copy "template/$path" "$path"
done

# A local copy that is a Git working tree gives no file Git ignores there, such
# as caches and editor files. Without Git, every file is copied (WS-10, SYS-1).
if [ -n "${AD_SOURCE:-}" ] && command -v git >/dev/null 2>&1 &&
  [ "$(git -C "$src" rev-parse --is-inside-work-tree 2>/dev/null)" = true ]; then
  git -C "$src" ls-files --others --ignored --exclude-standard --directory |
    while IFS= read -r path; do
      path=${path%/}
      rm -rf "${build:?}/$path"
      case $path in template/*) rm -rf "${build:?}/${path#template/}" ;; esac
    done
fi

mv "$build" "$dest"
build=""

cat <<EOF
Created $dest with the library lending sample. Next:

  cd $dest
  git init
  python3 scripts/check_structure.py
  python3 scripts/check_docs.py

Then follow "Start a new project" in README.md.
EOF

# Introduction specification

The behavior of the landing page: its story, its reader cards and its links.
It holds no knowledge of any service or flow.

## Model

```mermaid
classDiagram
    class Story {
        +Play()
        +Show(step)
    }
    class Step {
        <<enumeration>>
        goal
        flow
        rule
        artifact
        client
        test
        change
    }
    class ReaderCard {
        +Questions()
        +Links()
    }
    Story --> Step
```

The page has one story and one card for each reader: the stakeholder, the
solution architect and the product owner.

## Rules

| ID | Rule | Error |
| --- | --- | --- |
| INTRO-1 | The story has seven steps in this order: goal, flow, rule, artifact, client, test, change. Each step shows what the step before it showed and adds one layer, with one sentence that says what the new layer is. | — |
| INTRO-2 | Every goal, flow, knowledge ID, artifact and client that the story shows is one the sample holds, linked as the sample links it. Which rules the story shows as tested is an example, and the test step says so. | — |
| INTRO-3 | The page says that a rule with a test is not proof that the code is right (TST-3). | — |
| INTRO-4 | The change step starts from one rule and shows every flow and client that a change to it affects, and the clients it does not affect. The page states no cost, duration, plan or status. | — |
| INTRO-5 | The story plays by itself, one step after the other, and goes back to the first step after the last. It stops when the reader picks a step. When the reader's system asks for reduced motion, the story does not play and shows the last step. | — |
| INTRO-6 | Each reader card lists the questions of its reader and links each question to the page that answers it. | — |
| INTRO-7 | The page has a light theme only, also when the reader's system uses a dark theme. At a width of 360 px it needs no horizontal scrolling. | — |
| INTRO-8 | The page needs no build step and loads no script from another host. Without access to another host, it still shows the story, in the fonts of the system. | — |
| INTRO-9 | Each block of the story, when the reader points at it or taps it, explains in plain words what it is in the sample. While the reader points at a block, the story does not move on. | — |

## Lifecycle

```mermaid
stateDiagram-v2
    [*] --> playing: Open
    [*] --> stopped: Open with reduced motion
    playing --> stopped: Show(step)
    stopped --> playing: Play
    playing --> stopped: Play
```

Return to [Introduction](README.md).

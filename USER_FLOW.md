# Family Line — why the two sides connect

[Open the diagram](http://127.0.0.1:8778/static/user-flow.html) · [PNG for the video](artifacts/family-line-user-flow.png) · [SVG](artifacts/family-line-user-flow.svg)

## The product idea behind the image

Helping a family member from a distance takes more than availability. It takes knowledge of their situation: what they are using, what information they have, what has happened before, and what help they need now. Much of that knowledge lives with different family members or disappears between conversations.

Family Line gives that context somewhere to live and a familiar way to use it. The top row of the image is the family's knowledge of home. The middle row is an older relative's phone conversation, supported by that knowledge and by questions about the current situation. The bottom row is the information that comes back to the family, so someone can understand what happened and take over when needed.

## Why the dashboard has two parts

| Area | The need it addresses | How the design supports it |
|---|---|---|
| **Family assistant** | Relevant help depends on concrete information that the older relative should not have to explain from scratch on every call. | Family members can combine photos, documents, links and everyday details in a conversation. The assistant asks for missing context, and the family reviews what becomes shared household knowledge. |
| **Overview** | Family members need to understand what came up and where they can help, including when they missed the moment itself. | Call records and requests show the context for follow-up. A family member can take responsibility and save a response or next step. Records across calls can help reveal recurring questions. |

These areas connect through the phone conversation. Information from Family assistant gives the call a useful starting point. The call produces context for Overview. Family follow-up notes can then inform a later call. That return path is what allows help to continue across people and across time.

## How to explain the image aloud

“At the top is what the family knows about home. In the middle is a phone conversation that can use that knowledge. At the bottom is what the family learns from the call and can respond to. The return arrow matters because the next conversation can benefit from that follow-up.”

Introduce these needs and the two dashboard areas first. Then narrow to today's television example. The photo and household notes demonstrate why both visible details and family knowledge matter; the actual call demonstrates that the information is usable; the saved request demonstrates how a family member can pick up from there.

## Implementation behind the experience

| Component | Contribution |
|---|---|
| Family web interface | A place to build household context and a place to understand and respond to calls. |
| OpenAI intake | Reads uploads and helps prepare factual records and source notes for review. |
| Guava | Conducts the live phone exchange, asks questions, and invokes registered actions. |
| Python backend | Retrieves context, validates and saves confirmed changes, and records requests and follow-ups. |
| SQLite | Persists approved facts, resource references, conversations, outcomes and family notes. |

The family view reflects what is shared in conversations and saved records. The assistant still asks for current observations. A reported observation is recorded as such; approved device details require an explicit confirmed update.

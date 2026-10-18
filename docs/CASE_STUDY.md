# Family Line — case study

## Outcome and scope

The project owner confirmed the presentation was completed on October 17, 2026 and requested that this case be wrapped up. The result is a local prototype, a fictional household demonstration and a set of presentation assets. No adoption, usability-study result, business traction or clinical benefit is claimed. The final recording is still pending in `demo/video/`.

## The everyday problem

Relatives cannot always answer a call. Even when available, they need information to help from a distance: what the person sees, which device or document they have, and what has already happened. Explaining everything repeatedly is work for both sides. A new AI app can introduce another unfamiliar interaction.

Rbc’s product positioning puts concrete information and continuity at the center. The older relative uses a familiar phone call. Family members supply background and later see the record they need to continue helping.

## The two sides

**For the older relative:** start with an ordinary question, answer a focused follow-up and receive one useful step at a time. A family request can be left in the same call.

**For the family:** prepare useful household context, then see the conversation, attempted steps and requests. A response can become useful context for a later call. These are intended benefits of the design, not measured outcomes.

## Concrete scenario

June wants to watch Netflix. Her granddaughter Emma has provided a real reference photo of the black Roku remote, its location in a woven basket beside the armchair, and a note that Netflix was set up. June asks which remote or button to use. Guava can ask about the color or labels, while the backend supplies the saved facts.

June can then ask Emma to help choose something to watch. The phone action creates a persistent dashboard request. A successful button explanation and a remaining family request are separate outcomes; neither implies that the television was repaired or that Emma has already responded.

The household is fictional. The photo is real and attributed. Model processing, registered phone actions and database writes are actual system behavior. A screen observation is supplied by the caller, not remotely observed by the agent.

## How the design changed

| Decision | Why it mattered |
|---|---|
| Began with a todo tutorial | Made the boundary between semantic understanding and backend actions concrete. The old scripts remain as learning artifacts. |
| Chose everyday family support | Shifted from a generic assistant toward a familiar situation where context and follow-up matter. Other directions were explored, not validated as unmet needs. |
| Combined upload, links and chat | Separate intake forms felt fragmented. A single conversation can ask why a photo or document matters before saving it. |
| Added explicit review | A model interpretation is a draft. The family confirms records and source notes before they enter the phone context. |
| Replaced the synthetic remote with an attributed photo | Made the case concrete and exposed the need to distinguish visible controls, household setup and unknown screen state. |
| Stopped treating every TV request as a preset channel question | The agent should clarify the goal and current situation rather than map a broad topic to an old preference. |
| Prioritized requests and the latest call | The family’s first need is knowing where help is needed; history and the asset library are secondary. |
| Kept Guava and code responsibilities visible | Live understanding and responsive conversation are central. Code supplies retrieval, validation, persistence and follow-up. |
| Presented the broad problem before the TV example | Electronics demonstrate the idea; they do not define the entire product. |
| Renamed Callback to Family Line | The final interface and presentation use Family Line. Older filenames and migration identifiers remain historical implementation details. |

## Future vision

Future work could connect permission-based smart-home actions, optional Apple Watch activity/wellness context and proactive calls for agreed reminders or follow-up. These would require separate integration work and validation. The current code includes a basic scheduled outbound-call path, not a verified monitoring or emergency-response system.

If the project resumes, the highest-value questions are whether families can prepare enough reliable context with little effort, whether older relatives find the phone interaction useful, and whether the resulting record helps someone follow up. Tests should use specific everyday situations and examine where the assistant asks, acts, or hands over.

## Materials

- [Product workflow](../USER_FLOW.md)
- [Architecture](ARCHITECTURE.md)
- [Current feature inventory](FEATURES.md)
- [Solo presentation](../PRESENTATION_SCRIPT.md)
- [Video script](../VIDEO_SCRIPT_4MIN.md)
- [Historical project log](history/PROJECT_LOG.md)

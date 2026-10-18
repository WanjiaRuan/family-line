# Family Line — four-minute video script

**Format:** your opening video, two presenters, the existing workflow diagram, the prepared dashboard, and one real phone call.

**The story:** families cannot always pick up. Helping from a distance takes concrete information, and staying involved means knowing what happened afterward. Family Line connects those needs through a familiar phone call.

**Roles:** Presenter A introduces the problem, explains the diagram and returns to the family follow-up. Presenter B introduces the prepared household and makes the demonstration call.

**Timing:** a four-minute editing target, with 20 seconds reserved for your opening video and 80 seconds for the real call. This is not a timed rehearsal. Screen directions are not spoken aloud.

**Household continuity:** the current dashboard uses **June Hayes**, granddaughter **Emma Hayes**, and backup contact **Daniel Hayes**, under **June’s circle**. The script uses these existing names so the narration, phone context and screen match.

**Diagram:** [exported image](artifacts/family-line-user-flow.png) · [presentation page](http://127.0.0.1:8778/static/user-flow.html).

**Closing system visual:** [4K PNG](artifacts/family-line-system-design.png) · [editable SVG](artifacts/family-line-system-design.svg) · [presentation page](artifacts/family-line-system-design.html). Use this three-circle image after the call to explain the familiar phone medium, Guava live agent and code-maintained context. The earlier workflow diagram stays in the product overview.

## Narration and screen plan

| Time | Speaker | What the audience sees | English narration / audio |
|---|---|---|---|
| **0:00–0:20** | **Opening video** | Your prepared scene: an older relative calls her granddaughter, who does not answer. Rewind. She calls **Family Line** instead. End as Family Line answers; the detailed demonstration comes later. | Use the video's own audio. No presenter narration is needed here. |
| **0:20–0:55** | **A** | Return to the presenters or the **Family Line** title. Keep the framing about everyday family support. | “That’s a familiar moment. Someone you love needs help, and you can’t pick up. Even when you can, understanding what’s happening from a distance can be difficult. For some older relatives, reading instructions or navigating a new app adds another task when they’re already stuck. Saying ‘just ask AI’ doesn’t necessarily help. But a phone call is familiar. So we built **Family Line**, using Guava’s voice capabilities to make everyday help available through a conversation.” |
| **0:55–1:35** | **A** | Show the existing diagram. Follow the **family member** row into shared household context, then the **older relative** row, then **family follow-up** and its return arrow. Briefly point to the Guava/code labels at the bottom. | “The idea is to connect what the family knows with the help their relative needs. Family members provide photos, instructions and everyday details. The assistant asks follow-up questions, and they review what gets remembered. Their older relative can then call, describe the problem, and get guidance grounded in that information. Afterward, the family can see what happened and where someone is needed. Their response adds context for next time. Guava handles the live conversation; our code connects it to household information and saves the follow-up.” |
| **1:35–2:05** | **B** | Open the dashboard. Briefly show **Overview**, then **Family assistant**. Expand **Saved information** to show the existing remote photo and reviewed TV notes, including remote location and button guidance. No upload or intake demonstration. | “Let’s try this with a prepared household: June and her granddaughter, Emma. The dashboard has two parts. **Overview** shows what needs the family’s attention. **Family assistant** is where they build and review the information behind the calls. Here, the remote photo and household notes are already saved, including where June keeps it. Television guidance is our example today. Let’s hear how that information helps during a call.” |
| **2:05–3:25** | **B, on the phone** | Call **+1 484 990 7296**. Keep the relevant household information or live call view on screen. Use real call audio, without narration over the agent. The caller first asks for guidance, then asks for a message to Emma in the dashboard. | Follow the **caller script below**. Keep the agent’s actual replies. The exchange should show a concrete clarification, a useful instruction, and confirmation of the family request. |
| **3:25–4:00** | **A** | Start with the call view as you acknowledge the rough demonstration. Show the closing three-circle system image: familiar phone access, Guava live conversation, and our code maintaining shared context. Point to Family Line at their intersection. Then open this call’s transcript and request in **Overview / Needs your attention** for the final sentence. End on **Family Line**. | “This is a rough demonstration, but it shows how Family Line can use specific household context and ask follow-up questions. A familiar phone call is the entry point. Guava provides the natural, responsive conversation, while our code maintains the information and saves what happened. Together, they connect household knowledge, guidance and family follow-up. So instead of just a missed call, the family now has concrete context: what came up, what was tried, and where their help is needed.” |

The final sentence is for a recording where the transcript and request are visible. Wait for the call record to finish updating before recording that screen segment; show the actual new record.

## English caller script — one call, two outcomes

**Demo caller:** June in the prepared sample household. Speak normally. These are your lines, not a fixed script for the agent. Respond to its questions and skip a line if it has already answered it.

**1. Begin with the need.**

> Hi, it’s June. I’d like to watch Netflix, but I’m not sure which remote to use.

Let the agent respond. It may use the saved location — the woven basket beside the armchair — or ask which remote you have.

**2. Give a concrete detail when asked.**

> I have the black one with the purple arrow buttons.

This is visible in the prepared photo. The agent can use the household information to connect that description to the Roku remote.

**3. Ask for help identifying the control.**

> There’s an OK button in the middle. Is that the one I need?

Let the agent guide you to the Netflix shortcut. In the saved photo, it is the **white button with red Netflix lettering**, below the playback controls and to the left of Disney+.

If the agent has already explained the correct button clearly, go directly to the next line instead of repeating this question.

**4. Acknowledge the guidance and ask for family help.**

> I found the Netflix button. Could you leave Emma a message in the family dashboard? I’d like her to help me choose something to watch when she has time.

This demonstrates both parts in one conversation: the assistant helped identify a control, and the caller still wants a family member’s help with the next part.

**5. Confirm if asked, then end the call.**

> Yes, please save that for Emma.

After the agent confirms what it has saved:

> Thank you. Goodbye.

### If the agent asks about the TV screen

The main script can be demonstrated with the remote photo; it does not require claiming that a physical TV changed state. If you do not have the TV there, answer:

> I don’t have the TV in front of me for this demonstration. I’m looking at the remote photo.

Then continue with the button question and the request for Emma.

If you do have the matching setup available, describe what actually appears after following the instruction. For example, **only if Netflix opens**:

> Netflix is open now. Could you leave Emma a message? I’d like her to help me choose something to watch when she has time.

The agent’s questions and wording will vary. Keep its real replies and any clarification needed to reach the saved request.

## What to show after the call

Keep this screen segment focused on the connection between the conversation and the family’s next step:

- **Latest call:** open this recording’s transcript. Highlight the remote/button exchange and the request for Emma.
- **Needs your attention:** open the saved request. The meaningful content is that June wants Emma’s help choosing something to watch; use the actual generated wording.
- **Family response:** point to where Emma can add a response or take ownership. A new response does not need to be entered during the video.

A new TV request may be grouped with an existing TV item. In that case, show its newest occurrence and the corresponding call. An older TV fault is not evidence from this demonstration. Finding a button also does not mean the family request is resolved.

## Recording preparation

- Have your opening video ready; the first 20 seconds of this plan are reserved for it.
- A keeps the [dashboard](http://127.0.0.1:8778/) and [workflow diagram](http://127.0.0.1:8778/static/user-flow.html) open. Keep the app and phone listener running.
- In **Family assistant**, have the already saved remote photo and household notes ready to open. You do not need to re-upload, re-confirm or narrate the intake process.
- B has **+1 484 990 7296** ready to dial. Record both sides of the call with your available audio setup.
- Label the TV segment once as **“Sample household · Real phone interaction.”** Household details are fictional; the conversation and dashboard writes are real.
- Trim dialing, silence and screen switching to fit four minutes. Preserve the clarification, useful instruction and saved-request confirmation. If the call needs more time, shorten the diagram narration before removing either of the two phone outcomes.
- Keep connection credentials and unrelated call records outside the recording. This script edit does not rename household data or create any call records.

## Photo credit

For the video description or final frame: **“A Roku TV Remote” by Texas Lane**, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:A_Roku_TV_Remote.jpg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Original photograph unchanged.

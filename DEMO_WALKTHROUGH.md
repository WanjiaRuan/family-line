# Family Line — presenter preparation

Product: http://127.0.0.1:8778/

Phone: **+1 484 990 7296**

Video: [four-minute script and shot list](VIDEO_SCRIPT_4MIN.md)

The dashboard is the product interface. Presentation instructions and materials live here, outside the dashboard.

## Ready to call

The original presentation dataset already has June's reviewed Roku photo, operating reference notes and household setup. On a clean checkout, first run the preparation command in [RUNBOOK.md](RUNBOOK.md):

- Black remote, purple directional pad, in the woven basket beside the armchair.
- White Netflix shortcut with red lettering, below the playback controls and left of Disney+.
- Emma set up Netflix; she is the primary dashboard contact. Daniel is the backup.

Start with: **“I'm June. I'd like to watch Netflix, but I can't find the remote.”**

The assistant should ask about the current screen or remote when necessary, explain one step, and wait for the result. Old seeded channel preferences are archived. A request about “the TV” is a conversation to clarify, not a shortcut to a particular channel.

## Show the younger-generation side

1. **Overview → Family & sharing settings:** show Emma, June and Daniel.
2. **Family assistant → New conversation:** attach `examples/tv-demo/roku-tv-remote.jpg`.
3. Answer the assistant naturally. Use `household-note.txt` as context and attach `source-notes.md` in the same conversation.
4. Ask it to prepare the handover. Review and click **Confirm & save handover**.
5. The current setup is already saved, so this should update the same household record.

Download the three materials together: http://127.0.0.1:8778/api/demo/kit

## Show the phone side

**Successful path:** ask where the remote is and how to open Netflix. After following the instruction, report “Netflix opened. That's what I needed.”

**Family follow-up path:** report the screen remains black, describe what happened after the suggested step, then ask “Please leave a request for Emma and tell her what I've tried.” End the call. Open the request on Overview, claim it, and add a next step as **I'm handling this**.

To test clarification, ask “Can you help me with the TV?” without a desired task. The assistant should ask what you want to do or what you see. It should ask for details of an unfamiliar remote rather than inventing its controls.

## What's real in the presentation

The family is fictional; the remote photograph is a real reference photo. Upload processing, phone calls, database writes and dashboard requests are real. If matching physical equipment is unavailable, screen observations are role-played. The phone provides guidance, not direct control of the television.

The product is a single local household. Account separation, invitation delivery, live shipment tracking and health integrations are outside the current build. Existing original call transcripts remain in the database; scripted sample calls are hidden from the everyday dashboard.

## Source material

- [Texas Lane's photo](https://commons.wikimedia.org/wiki/File:A_Roku_TV_Remote.jpg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), unchanged.
- [Roku simple-remote guide](https://support.roku.com/en-au/article/simple-remote-setup).
- [Netflix on Roku](https://help.netflix.com/en/node/23886/).

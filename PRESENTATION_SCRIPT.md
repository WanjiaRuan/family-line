# Family Line — live presentation script

单人英文现场稿，约 3–4 分钟，正文 421 words。按顺序直接讲即可；斜体括号内是画面提示，不朗读。可以配合现有图片和 dashboard 展示，不需要现场拨号。时长为估计，尚未计时排练。

## Presentation script

*[Show the opening illustration: artifacts/family-line-opening-story.png.]*

We built Family Line around a familiar moment: someone you love needs help, and you can’t pick up.

It might be a question about a delivery, a confusing message, or something at home. Even when you answer, helping from a distance takes context. What are they looking at? What have they already tried? You want to help, but you’re trying to understand a situation you can’t see.

For some older relatives, our usual suggestion — “just ask AI” — creates another task. They still have to find an app, describe the problem, and work out what information to provide.

A phone call is already familiar. That’s our starting point.

*[Show the workflow diagram: artifacts/family-line-user-flow.png. Explain the family, phone and follow-up rows without reading the numbered boxes.]*

So Family Line brings two sides together. Family members use a conversational dashboard to share photos, instructions and everyday details. The assistant asks follow-up questions, and the family reviews what gets saved.

An older relative can then call and ask for help in their own words. The voice agent uses that household context, asks about anything unclear, and guides the conversation from there.

After the call, the family can see what happened and what still needs their attention.

*[Show Family assistant with the saved remote photo and household notes. This is the prepared sample household; uploading does not need to be demonstrated live.]*

In our prototype, we’re demonstrating that with June and her granddaughter, Emma. Emma has already provided a remote photo and notes about June’s television setup.

June can call and say, “I want to watch Netflix, but I’m not sure which remote to use.” The assistant can ask about the remote’s color or buttons and use the saved information to guide her.

If June wants Emma’s help, she can leave a request during the same call. That request appears alongside the call record in the family dashboard.

*[Show Overview: a call record and its corresponding request. If showing a recorded test, use its actual record.]*

That creates value for both sides. For June, it reduces the effort needed to ask for help: she can start with an ordinary question and work through it conversationally. For Emma, it provides a clearer starting point for following up. She can see what came up, what was tried, and where she is needed.

*[Show the three-circle system image: artifacts/family-line-system-design.png. Finish with Family Line on screen.]*

The system combines three things: a familiar phone call, Guava’s live conversational abilities, and our code for maintaining household information and saving outcomes. Guava’s ability to understand, clarify and respond is central to the experience. Our application connects that conversation to information the family has reviewed and records they can act on.

This is an early prototype. Today’s television example demonstrates the broader idea: everyday help with context that carries forward.

So instead of just a missed call, the family now has concrete context: what came up, what was tried, and where their help is needed.

## Optional future vision

可放在 “This is an early prototype...” 之后、最后一句收尾之前。约增加 1 分钟；基础稿仍为约 3–4 分钟。下面是未来设想，当前原型尚未接入家庭设备或 Apple Watch，也未实现这些自动外呼流程。

Looking ahead, we want Family Line to become more connected to everyday life.

With smart home integrations, it could check device status and, with permission, help with simple actions like adjusting a thermostat or turning on a light. We’d also explore Apple Watch integration, allowing older relatives to choose whether selected activity or wellness information becomes part of their shared context.

Another direction is proactive support through outbound calls: a reminder about a confirmed delivery, a check-in after an unresolved problem, or a call to a family member when someone has asked for help.

These are future directions we’d need to build and validate. The goal is to make support more timely and informed, while keeping control with the older relative and keeping the experience as simple as a phone call.

## Presentation assets

- [Opening illustration](artifacts/family-line-opening-story.png)
- [Product workflow](artifacts/family-line-user-flow.png)
- [Closing system image](artifacts/family-line-system-design.png)
- [Dashboard](http://127.0.0.1:8778/)
- [Four-minute video and caller script](VIDEO_SCRIPT_4MIN.md)

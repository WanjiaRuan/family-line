# Visual and presentation assets

All existing authored visuals are retained. The October 17 presentation is complete; screenshots below are historical captures, not a live service-status check. The full demo recording is pending in [`demo/video/`](../demo/video/README.md).

## Current presentation images

| File | Use | Source / editable version |
|---|---|---|
| [Opening story](family-line-opening-story.png) | Everyday help, a missed family call and the familiar phone entry point. | AI-generated using the built-in image generator; [exact prompt](family-line-opening-story-prompt.md). |
| [Product workflow](family-line-user-flow.png) | Family information → older-relative call → family follow-up and returned context. | [SVG](family-line-user-flow.svg), [HTML](family-line-user-flow.html). |
| [System concept](family-line-system-design.png) | Three intersecting capabilities: phone, Guava live conversation and persistent context. | 3840×2160 PNG; [SVG](family-line-system-design.svg), [HTML](family-line-system-design.html). |
| [Simplified Overview capture](family-line-simple-dashboard.png) | Attention-first family interface. | Historical narrow viewport; its existing TV request predates the final Roku scenario. |
| [Conversation capture](english-conversation.png) | One conversation containing a photo and follow-up. | Historical screenshot. |

## Other retained captures

`family-line-dashboard.png`, `family-line-flow-page.png`, `english-overview.png`, `callback-dashboard.png`, `dashboard.png` and `ai-query.png` preserve earlier layouts, names and language. The initial Chinese interface and Callback name are history, not the current product specification. Some captures show earlier fictional controls or the original local call number; use the current scripts and your own Guava configuration for a new demonstration.

## Household source materials

[`examples/tv-demo/`](../examples/tv-demo/) contains the actual Roku remote photograph, household note and source note. The unchanged photo is by **Texas Lane**, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:A_Roku_TV_Remote.jpg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The copy in `family/static/demo/` serves the download kit. Retain the credit when reusing the photo.

`examples/demo-remote.png` and `examples/bedside-lamp.md` belong to the early tutorial; they are not the current TV reference.

[`docs/ASSET_MANIFEST.json`](../docs/ASSET_MANIFEST.json) lists image paths, byte sizes and SHA-256 checksums, including runtime copies. Diagrams were produced as native SVG and exported to PNG; the opening illustration was generated. No additional product capabilities should be inferred from the visuals.

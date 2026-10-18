# Historical project log

Preserved at case wrap-up on October 17, 2026. Entries below describe successive prototypes and changing presentation plans; the current README and architecture document take precedence. Older live-state claims are historical observations, not current service status.

# Family Line · A family handover, a phone call away

Local app: http://127.0.0.1:8778 · Phone: **+1 484 990 7296**

- [Live presentation script: problem, product value and system](../../PRESENTATION_SCRIPT.md)
- [Present the two-sided TV demo](../../DEMO_WALKTHROUGH.md)
- [Run the app, inspect the data model and see actual limits](../../RUNBOOK.md)
- [Quick presenter test card](../../TEST_CASES.md)
- [Real photo and source materials](../../examples/tv-demo/source-notes.md)

## October 17 live presentation script

Future-vision addition: Rbc requested smart home and Apple Watch connections plus outbound calls. The presentation now includes an optional roughly one-minute segment framing these as integrations to build and validate, with permission-based device actions, optional sharing of selected wellness context, and calls for reminders or follow-up. These are future concepts, not claims of current integrations or autonomous calling.

Rbc requested a backup presentation in case the team has an opportunity to present. [The live script](../../PRESENTATION_SCRIPT.md) is a standalone English pitch for one presenter, approximately 3–4 minutes at presentation pace. Rbc confirmed the single-presenter format; speaker labels and handoff instructions have been removed. It explains the everyday remote-help problem, the value for both the older relative and family, a concrete prepared TV example, and the roles of Guava’s live agent and our context-storage code. It can be delivered without the opening video or a live call. Timing is estimated from word count, not a rehearsal; product benefits are presented as the prototype’s intended value, not measured user-study outcomes.

## October 17 opening narration image

Rbc requested an image for the everyday-support opening narration. [The generated wide illustration](../../artifacts/family-line-opening-story.png) shows an older relative at home with household instructions and a parcel, a younger relative occupied at work, and a phone/voice motif connecting the story to Family Line. English copy emphasizes a familiar phone call and identifies Guava as the conversation provider. Generated with the built-in image_gen tool, visually inspected, and copied unchanged into the project; [the exact prompt](../../artifacts/family-line-opening-story-prompt.md) is saved alongside it.

## October 17 closing system visual

Rbc requested a final image showing the technology concept, with Guava’s live agent treated as a core capability. The [three-circle visual](../../artifacts/family-line-system-design.png) combines familiar phone access, Guava’s understanding/clarification/guidance, and our code retrieving household information and saving call outcomes and family requests. Family Line occupies the intersection. The closing script now references this image, while the earlier workflow image remains in the overview.

Delivered: a 3840×2160 PNG, editable SVG and local presentation HTML in `artifacts/family-line-system-design.*`. The graphic follows the existing warm white/green palette, adds blue for Guava and sand for persistent context, and uses exact English labels. Exported from the native SVG and visually inspected for legibility; no product code or call data changed.

## October 17 opening video and one-call demonstration revision

Closing refinement: Rbc asked to acknowledge the rough demonstration immediately after the call, explain context-specific guidance and follow-up questions, and connect the familiar phone medium, Guava conversation and our information-storage code. The final sentence returns to the concrete context a family can use to help next. The closing narration and screen directions were updated; the rest of the recording plan is unchanged.

Rbc specified a new sequence for the [four-minute script](../../VIDEO_SCRIPT_4MIN.md): their opening missed-call/rewind/Family Line video; the everyday problem and familiar phone entry point; the existing diagram explaining both roles and follow-up; the prepared household dashboard; one real call showing remote/button guidance and a saved request for Emma; then the transcript and attention item. There is no live upload/intake demonstration. The two dashboard areas are introduced by purpose, and the TV appears as the current functional example rather than the whole product scope.

The script includes separate English caller lines, uses June/Emma to match the existing application, and reserves 80 seconds for the call. The caller can identify the control from the photo without inventing a physical TV outcome. The opening clip is Rbc’s planned material, not a newly produced asset. This supersedes the earlier no-staged-opening presentation plan below. Validation was a document readback and timing/word-count review only; no application changes, new calls or broad tests were made.

## October 17 presentation rationale revision

Rbc rejected narration that simply lists actions and requested a connected explanation of why the product is designed this way. The [four-minute script](../../VIDEO_SCRIPT_4MIN.md) now uses the existing diagram to explain the need for context before, during and after a call, introduces the two dashboard areas and their purposes, and then narrows to the TV example. The image remains unchanged. Clicks are screen directions; the spoken narrative explains the product decisions and the connection between the two sides. Two presenters and a real call remain the production format. Timing is an edit target, not a rehearsed duration.

## October 17 flow diagram and simpler presentation surface

Rbc requested a clearer explanation of the whole user flow and a lighter dashboard for showcasing the use case. [The user flow](../../USER_FLOW.md) now has an exportable SVG/PNG and a separate [explanation page](http://127.0.0.1:8778/static/user-flow.html). It separates family information intake, the phone conversation, and family follow-up, with approved household context and saved follow-up notes connecting them.

Overview now foregrounds requests and one latest call. Earlier calls, completed items, reminders and the activity log are inside **History & more**. Draft review stays with the intake conversation; the source library is collapsed beneath the conversation. Family setup and all existing records remain accessible. The flow link is in the footer, and the video script uses the exported diagram for its short architecture explanation. Validation: JavaScript syntax and rendered Overview/conversation checks; no new model sessions or broad test run.

## October 17 positioning and video revision

Latest naming decision: Rbc chose **Family Line**. The dashboard, phone greeting, upload assistant, presenter script and downloadable kit use this name; the agreed positioning and two-presenter flow remain the same.

Rbc clarified that Family Line addresses an everyday moment of remote-help frustration: family cannot always answer, helping from a distance requires concrete context, and the next person needs to know what happened. A familiar phone call lets June begin in ordinary words while the assistant guides the exchange. The family view gives Emma the saved facts, attempted steps, outcomes and a place to follow up. This is the user-confirmed positioning; universal claims about older adults or continuous monitoring are not implied.

The [four-minute English video script](../../VIDEO_SCRIPT_4MIN.md) now pairs narration with screen actions around that story. Rbc further clarified the opening: establish the broader everyday-support need first, then explicitly introduce TV/device guidance as today's specific example. That earlier script introduced remote details at 1:55, after the product and dashboard explanation. Rbc then specified two presenters and limited production time: that version became a plain product walkthrough with screen recording, a real phone segment, and a short explanation of the Guava/code division. In that version, the presenters spoke as themselves and staged family scenes were removed; the newer opening-video plan above supersedes that choice. Timings are editing targets, not a measured rehearsal. This turn changes the script and project record only; the running product and household data are unchanged.

## October 17 dashboard cleanup

Rbc requested a plain dashboard, a ready-to-call TV setup, natural clarification instead of visible prompt warnings, and a four-minute video. Presentation tooling moved out of the everyday interface. Old seeded channel/pickup/parcel facts are archived, original calls remain preserved, and the current Roku/Netflix setup stays available for calls. Sample calls are hidden instead of relabeled as real calls. Phone guidance now asks one concrete question when the goal, screen or remote is unclear. Household records contain facts rather than model instructions.

- [Four-minute English narration, live-call lines and shot list](../../VIDEO_SCRIPT_4MIN.md)
- [Presenter preparation and current test flow](../../DEMO_WALKTHROUGH.md)
- Architecture emphasis: Guava owns the live conversation; Family Line code retrieves and persists shared information and follow-ups. OpenAI handles upload understanding.
- Validation for this edit is intentionally limited to syntax, startup/listener registration and a rendered-page check. No new model sessions or broad test run were requested.

## October 17 English revision

Rbc requested an English presentation, a believable family and TV example, and follow-ups before information storage. The next correction made the key interaction a single conversation: upload, understand, ask, consolidate, confirm. The asset library is secondary.

Implemented: English interface and generated notes; overview prioritizing requests; three-step fictional-family onboarding; persistent chat with photo/document/link attachments; atomic approval of records and sources; actual licensed Roku remote photograph; household notes and presenter scripts; actionable family resolution notes. Earlier conflicting silver-remote and synthetic-image fixtures are archived.

Verified: 33 local tests; real OpenAI image understanding and complete reviewed handover; actual source URL extraction; two Guava real-model text scenarios (successful Netflix guidance and unresolved-TV fallback) using only fictional test material. The earlier actual user phone call remains preserved. A live audio rehearsal of this revised flow remains for the presenters.

Why the change mattered: the earlier phone call affirmed an undocumented red button and its summary lost the problem in farewell lines. The new flow keeps unknown controls explicit and preserves attempted steps and outcomes. Successful guidance is no longer automatically an unresolved family task.

## Earlier exploration history

The following is retained as historical project context, not the current demo script.

以下保留最初待办教学实验的历史。原代码已保存为 `main.todo.py`；下面旧运行命令描述的是当时版本，不是当前入口。

目的：通过一个小实验理解 Guava 对话层与自己编写的业务代码如何协作。

## 运行

在终端执行：

```sh
cd /Users/rbc/demo-agent
guava run
```

输入 `I want to read a chapter.`，等助手追问耗时，再输入 `Half an hour.`。
也可以问 `What have I already put on my list?` 查询同目录 `todos.jsonl`。
每次运行演示一次新增或查询，完成后结束对话。Ctrl+C 可退出。
如果终端报 `curses` 颜色错误，可执行 `TERM=xterm-256color guava run`。

麦克风模式：`guava run -- --voice`（尚未实测，可能需要麦克风权限）。

## 读代码

- `start()`：打招呼，让用户选择新增或查询。
- `intent_recognizer`：我们声明 add_todo / list_todos 两种动作及含义。
- `choose_action()`：用 Guava 的 IntentRecognizer 做语义分类，日志显示 [Intent]。
- `add_todo()`：声明 Task 和 Fields；Guava 理解对话、追问并提取信息。
- `read_todos()` / `list_todos()`：Python 读取真实文件，交给 Guava 回答。读取错误明确报错。
- `answer_question()`：处理 Guava 的问题通道；查询类问题读取同一个文件，只读不写。问题与动作可能同时触发。
- `save_todo()`：Guava 触发完成回调，我们校验数据并用 Python 写入文件。
- `call.hangup()`：保存后让 Guava 反馈结果并结束。
- `main.original.py`：创建项目时的官方示例备份。

## 进展与证据 — 2026-10-17

- 已通过真实 Guava 文字会话测试：输入 read a chapter，助手追问耗时；Half an hour 被提取为整数 30。
- 已观察到 collect_todo 完成事件、保存函数日志，并读回 todos.jsonl 中对应数据。文件保留这条测试待办。
- 第一轮已提取字段但迟迟未触发完成事件；明确 completion_criteria（收集完即完成，保存由回调执行）后重测成功。不能据此断定初次停顿的唯一原因。
- 工具终端初次因 TERM 不支持颜色而报 curses 错误；设置 TERM=xterm-256color 后正常。
- 当前项目虚拟环境实际为 Python 3.12.13，guava.toml 的部署镜像为 3.14；本机默认 python3 为 3.14.3。三者是不同环境；本次是在现有项目虚拟环境中验证。
- 这是单条待办教学 demo，不提供提醒、删除、修改功能。语音模式与云端部署尚未验证。

## 查询与意图分流 — 2026-10-17

- 动机：Rbc 希望亲眼看到语义理解如何区分新增/查询，以及 SDK 接口和自定义业务逻辑的边界。
- 采用 SDK 自带 guava.helpers.llm.IntentRecognizer，不做关键词分支。源码表明它将动作说明和 JSON schema 发到 Guava 的 /v1/llm/generate；未暴露具体底层模型 ID。
- 真实查询输入 What have I already put on my list?：分类为 list_todos，问题和动作回调都读取真实文件，助手回答 read a chapter；文件未增加记录。
- 新增输入 reviewing the Guava demo / fifteen minutes：分类为 add_todo；第一轮动作交接后未立即提取，用户重述并确认后保存成功。为动作处理函数补充明确的返回指令，说明当前仅开始收集、尚未保存。
- 本地临时文件检查通过：文件不存在、损坏 JSON、查询不修改文件、无效耗时不写入。
- 官方 developers 页面声称自有 ASR/TTS/语言模型一体化；招聘页提到训练和微调。具体基座、型号、是否从零预训练以及 helper 是否使用同一模型均未确认。来源：https://goguava.ai/developers 和 https://goguava.ai/careers/machine-learning-engineer 。

- 补充动作返回说明后真实重测：Add a test todo called routing check, five minutes. 一次输入即完成意图分类、字段提取、保存、成功反馈和结束。已仅移除本轮 routing check 测试行，保留 read a chapter 与 review the Guava demo 两条示例记录。

## 手机呼入 — 2026-10-17

运行 `guava run -- --phone`，读取 guava.toml 的 phone_number 并启动监听；保持进程运行，手机即可拨打该号码尝试呼入。它与 --voice 互斥，不加参数仍为文字模式。

用户首次尝试拨号时，检查发现没有运行中的 agent，代码也尚无电话入口。已添加 --phone 并启动，SDK 日志确认号码监听注册成功（0 other listeners）。这只验证了监听连接，尚未验证真实手机呼入、语音效果或电话资费。

## 视障手机使用场景探索 — 2026-10-17

Rbc 当前意图：先了解盲人/低视力用户真实生活中尚未解决好的手机使用场景，不急于选方案。Rbc 提出“手机操作是否麻烦、能否用电话帮助完成”的待验证假设；不是用户研究结论。

本轮公开资料发现（主要为英美来源，不能直接外推到中国；历史报告/个人经历不能证明当前特定 App 版本仍有同样问题）：
- RNIB 2024 报告强调群体内部技术熟练度差异；不能将使用障碍归因于盲人普遍不擅长手机。https://www.rnib.org.uk/professionals/research-and-data/reports-and-insight/sight-loss-and-technology/
- AFB BDIS2（2023 年 20 人、10 天日记，2024 年发布）记录表单、出行预订等任务被中断，包括父亲无法完成蹦床公园免责声明表单、另一参与者转电话订机票耗费三小时。https://www.afb.org/research-and-initiatives/research/summaries/barriers-digital-inclusion-2
- Michael Taylor 2025 年第一人称度假村经历：无标签接驳车按钮、不可读取时间列表、数量修改读屏与实际值不同，影响完成与确认。商业无障碍服务商博客上的个人经历，不是代表性调查。https://blog.usablenet.com/resort-mobile-app-accessibility-blind-guest
- Broken Access（WWW 2025；2026 年 arXiv）是读屏认证流程的系统评估，非盲人生活日记；提示登录/2FA及跨设备流程值得进一步实地了解。https://arxiv.org/abs/2603.07820
- 已有直接相关产品 InnoSearch Shop by Phone，不能称电话购物是空白。https://www.innosearch.ai/us/shop
- AFB AccessWorld 2025 年 InnoSearch 亲测文章记录 AI 电话购物时仅浏览的商品进入购物车、纠正选项需要耐心；是历史体验，未核查目前是否修复。https://afb.org/aw/summer2025/innosearch-review
- Be My Eyes 已提供视觉问答、志愿者和企业支持目录；其支持覆盖受地区、语言和服务方影响。https://support.bemyeyes.com/hc/en-us/articles/360005523318-Call-a-company-through-the-Service-Directory

Codex 待验证推断：值得观察的可能是“任务卡在最后几步、无法确认真实状态、失去对选项/操作的控制”，而非把所有界面替换为语音。电话入口本身不提供对其他 App 的读取/操作权限，仍需后端接入。尚未访谈用户或选定方案。

### 新增探索分支：区域山火预警电话 — 2026-10-17

Rbc 提出：进入某个区域后收到山火等预警电话。暂未选择为方案，也未授权创建监控、对外呼叫或定位采集。
- 官方 Alert LA County 已提供订阅式电话/短信/邮件通知：https://ready.lacounty.gov/emergency-notifications/ 。不能把自动电话预警视作尚无人提供。
- FEMA 的 WEA 机制已有地域定向；它与我们自建 App 的后台 GPS 区域触发、电话号码拨号是不同机制。
- Codex 待验证推断：潜在价值可能在官方警报之后的可访问解释、区域核对与连接已有支持，而非自行判断火情/发布撤离命令。需进一步查视障人士的具体经历；不能假设所有官方警报不可被读屏读取。
- 若做原型应使用明确标注的模拟事件。真实应用依赖权威且及时的区域/警报数据、定位与通知可靠性，电话通道本身也可能受断网/拥塞影响。

## 方向推进：家人录入、长辈电话使用的家庭助手 — 2026-10-17

来源：Rbc 在本对话中完整描述的产品设想。目标人群暂偏老年人，不把所有老年人视为相同需求，也未得出视障支持已经充分的结论。
- Rbc 设想：年轻人或其他信息提供者，通过后台上传文档、图片、文字，或通过语音/电话录入家庭信息；agent 在录入时追问足够的情境信息，例如遥控器颜色、对应设备和家庭接线。
- 长辈通过电话询问设备使用、快递等家庭事务；信息也可用于主动电话提醒，例如到村口指定便利店取件。希望减少阅读/操作负担，以及家人不在场或有时差时的信息断层。
- 不限于家电；“设备说明”和“取件提醒”是当前例子，尚未确定第一版范围。用户此次要求先理解和检查想法，并未要求开发后台或拨打电话。
- 技术核对：官方 DocumentQA 接收 str/list[str]，支持文档增改删；不能据此声称它直接解析原始图片/PDF。可由我们建设上传和解析层，核对图片提取的型号/按钮等关键事实后，向对话提供文本与结构化记录。https://goguava.ai/docs/document-qa
- 安装版 SDK 的 Agent.call_phone 提供外呼入口；本方向尚未实测外呼、定时提醒和多家庭隔离。此前用户已反馈现有 demo 手机呼入成功（“nice it works”）。
- Codex 待验证判断：主要难点是录入负担、信息新鲜度、通话中未知现场状态、多人更新冲突和提醒的退出条件。说明书适合资料查询；包裹预计/已到/已取与提醒时间需要持久化状态，不能仅作为一段背景 prompt。
- 关键语义边界：家人说“买了”不等于“已经到店”；长辈说“知道了/明天取”不等于“已经取件”。后续需验证这些区别能否在真实对话中保持。

### Rbc 补充与纠正：自动跟踪、偏好记忆和联系家人

- 快递的预期体验是提供单号后系统自动跟踪并适时提醒，不要求家人手动维护物流状态。可接物流查询 API / webhook；本轮核实 TrackingMore 官方 SDK 提供登记、查询、承运商识别接口，其官方文档也提供 webhook。实际承运商覆盖、取件码/门店信息是否可得尚未验证，不能从运输状态推断长辈已经取件。
- Rbc 希望助手记住日常偏好（例如常看 67 频道）；解决不了时可联系预先配置的家人，用电话解释长辈需要什么帮助。也提出按既定安排提醒吃药的生活助手方向。
- 安装版 Guava 有 call.transfer 和 Agent.call_phone；实时转接与另拨家人电话是不同流程，均未实测。接口存在不保证号码、账户和线路当前已具备相关权限。
- Codex 建议（尚未作为用户确定的实施方案）：一个 Python 服务加数据库、上传/对话录入页面、后台任务 worker，复用 Guava 处理电话；按家庭隔离资料，保存信息来源、更新时间、偏好和事件状态；后台按物流事件/时间触发外呼，保存通知与重试状态。首版选家电指导、自动物流提醒、失败后电话交接三条完整流程；药物仅按已确认计划提醒，不推断剂量或补服方案。
- 本轮只讨论搭建方式、核对接口并更新记录；未开发新功能、接物流账户、创建定时任务或拨打电话。

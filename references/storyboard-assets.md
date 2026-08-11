# 分镜、真人、动态覆盖与素材

## 时间轴真本

优先级：锁定录音/口播精确时长 > 中文 SRT 时间骨架 > 正文语义 > 估算时长。标题静音、章节停顿和尾部余量单独标记。

若录音与 SRT 末尾不一致，先检查静音、裁切和采样率；未经确认不得拉伸主音频来迁就旧时间表。

## 拆语义，不按标点机械切

1. 先识别章节：钩子、问题、背景、论据、对比、转折、结论、桥接。
2. 以一个完整观点或动作链为 Scene。每个 Scene 只承担一个主要叙事任务。
3. 中文短句少于约 8 字且不能独立成立时并入相邻句；长句超过约 30 字时可在因果、转折、并列或举例处拆分，但不截断语义。
4. 图片单张展示 5–10 秒。视频源长不少于 5 秒时完整自然播放，超过 10 秒也不裁切；不足 5 秒时完整播放一次后保持末帧至 5 秒。短促重锤由程序化文字/图形承担。
5. 关键信息落定后保留 0.5–1 秒稳定帧。超过 30 分钟的长视频每 5–8 分钟安排一次明确注意力重置：新问题、新案例、新视觉形式或新观点。

## 先做场景类型大纲

在写 `video-spec.json` 前先写 `outline-scene-types.json`。每个语义段只能先选一个主类型，可附一个辅助类型：

| 主类型 | 适用内容 | 最低要求 |
|---|---|---|
| `chapter_title` | 每章题目与内容总览 | 超大双语标题铺满主视觉区、2–4 个要点/逻辑框架、动态建立、阅读 hold、强化声音 cue |
| `chart` | 因果、趋势、对比、排名 | 数据来源、口径、单位、结论 |
| `screenshot` | 产品/网页/文档操作 | 关键 UI、可读区域、隐私处理 |
| `data` | 数字、统计、指标 | 数值来源、日期、单位、误差 |
| `key_text` | 定义、转折、核心判断 | 已审文字、阅读时间、层级 |
| `image_explainer` | 普通图片承载环境、人物、物件或问题 | 清晰原图全屏、零模糊、确定性动态、HyperFrames 局部文字毛玻璃、字幕排除区 |
| `archive` | manifest 标记为 `archive_evidence` 或 `book_evidence` 的证据 | 简中＋英文标题/来源区、大幅清晰证据图、零模糊、无动态说理 |
| `map` | 地理、迁移、路线 | 投影、边界口径、时间与来源 |
| `relationship` | 权力、制度、流程、因果 | 节点、边、方向、层级 |
| `environment` | 地点、时代、氛围、呼吸 | 氛围功能，不冒充证据 |
| `presenter` | 建立关系、强调立场、情绪回环 | 完整句、占比预算、全屏/小窗理由 |
| `argument_bridge` | 缺少合适媒体或具体动态图解时的低频补位 | 左双语大论点、右 2–4 个双语动态分论点、HyperFrames、占比与每章上限 |

大纲每段写：原文范围、核心命题、主类型、镜头功能、观众先看什么、看完明白什么、证据/数据需求、文字需求、潜在工具和回退。通过后再转换为执行分镜。

## 真人连续段

硬规则：从完整句开始，到完整句结束。字幕条、半句话和过渡词不能单独成为真人补录段。

优先位置：

- 全片开头：真人从 `00:00` 起最多全屏 15 秒；左右必须由 HyperFrames 建立 2–4 个问题、承诺、关键词、进度或证据预告，不能裸讲。
- 章节开头：先播放全屏超大标题章节总览卡；进入正文后真人只能使用抬高避开字幕区的小窗或撤下，禁止任何中段全屏例外。
- 章节总结：完成结论、回扣和下一章桥接，仍使用小窗或撤下。
- 全片结尾：只有最终总结允许真人重新全屏并持续到实际最后一帧；总结组件逐镜比较 Remotion 与 HyperFrames，至少使用进度、路径或逻辑箭头之一闭环。
- 论证中段：只有表情或目光能帮助理解时才留圆窗，否则撤下；关键手势不要依赖圆窗展示。

一段通常 2–6 个完整句、20–45 秒；天然完整总结可延长到 60 秒。不要为凑时长截断逻辑。真人成片累计时长必须严格小于总时长 20%；先建立全片预算表，再选段。开场全屏在 15 秒前最近的自然停顿开始缩窗；口播可以连续，不因画面缩窗截断语义。除最终总结外不允许再回全屏。

全屏转圆窗：先建立主素材 12–24 帧，再用约 36–60 帧缩到内容安全的一侧；只改变位置、尺寸、圆形 mask 和克制描边，不叠旋转、弹跳和光效。2560×1440 默认直径约 360px，可在 340–380px 内按头肩构图微调；小窗底边必须高于 220px 字幕排除区，并以人脸、口型、双语图解和主证据复核。圆窗不承担关键手势展示。

拍摄默认：16:9 全屏、2560×1440 最低/4K 优先、60fps、固定曝光白平衡焦点；人物居中并保留圆形头肩裁切安全区，同时保留开场全屏需要的双手范围。每段先留 5 秒中性姿态与纯静音，再录入双短提示音，连续讲完整段，结束录入双短提示音，再留 5 秒中性姿态与纯静音；每段 1–2 个克制手势。后期负责裁圆窗，不要求用户另拍小窗版。

## Scene 固定字段

```yaml
id: S001
start: 00:00:00.000
end: 00:00:05.000
chapter: 开场
source_range: 从完整起始句到完整结束句
scene_type: chapter_title|chart|screenshot|data|key_text|image_explainer|archive|map|relationship|environment|presenter|argument_bridge
function: introduce_chapter|explain_causality|provide_evidence|provide_atmosphere|emphasize_turn|presenter_connection|bridge_argument
task: 抛题|解释|证据|对比|转折|总结|情绪缓冲
viewer_should_notice: 观众此刻首先注意什么
viewer_should_understand: 本镜结束时观众应明白什么
carrier: presenter_full|presenter_pip|broll|archive|image|map|remotion|hyperframes
programmatic_opportunity: preferred|support|not_suitable
programmatic_declined_reason: 仅 not_suitable 时填写
programmatic_mandatory_kind: not_applicable|chapter_open|causal|process|institutional_relation|structural_relation|textual_reasoning
composition: 主窗口、辅助层、人物和字幕安全区
visual_mode: image_fullscreen_clear_local_text_glass|historical_evidence_split_title_source_plus_large_image|video_fullscreen_clear_local_text_glass|argument_bridge_bilingual|presenter_opening_full_overlay|presenter_pip|presenter_closing_full_summary|other
semantic_segment_id: 当前唯一文案语义段 ID
source_text_ids: [同一语义段内的已审文字 ID]
text_provenance: verbatim|faithful_compression|approved_summary|layout_only
text_change_kind: unchanged_approved|layout_only|new|changed
new_claims_added: false
cross_chapter_merge: false
visual_page_id: 全片唯一页面 ID；总结/观点/程序化信息页必填
content_fingerprint: 从已审标题、要点、节点与结论生成的稳定指纹
duration_fill_strategy: not_needed|extend_internal_choreography|new_semantic_page
repeat_page_to_fill_duration: false
internal_phases: [同一 HyperFrames composition 内的新信息/视觉状态]
animation_intent: [explain|focus|compare|relate|quantify|demonstrate|transition|identity|rhythm|atmosphere|delight]
motion_role: primary|support|ambient|mixed
engine: remotion|hyperframes|lottie|d3|blender|manim|none
engine_selection: {semantic_accuracy: 0-5, subject_safety: 0-5, render_stability: 0-5, visual_impact: 0-5, near_tie: true|false, selected_engine: remotion|hyperframes, reason: 选择理由}
motion_family: materialize|mask_reveal|focus_relay|path_draw|progress_build|type_sequence|count_transform|spatial_push|parallax_evidence|comparison_morph|chart_growth|shape_handoff
motion_signature: {layout: 构图, direction: 方向, build_order: 建立顺序, easing: 缓动, pace_class: fast|medium|slow|very_slow}
variation_from_previous: {mode: changed|slower|not_applicable, changed_dimensions: [], pace_multiplier: 1.0}
apple_logic: {purpose: 目的, focal_hierarchy: 注意点顺序, spatial_origin: 空间锚点, material_response: 材质层级, continuity: 前后接力, settle_state: 落定与阅读, delight: 克制增益或 none}
library_candidates: [统一 catalog ID]
library_selection: {primary: catalog ID|custom, ambient: catalog ID|null}
motion: 一个主要运动动词
material: glass_thin|glass_regular|glass_thick|none
background_visibility: faint|subtle|evidence|none
subject_safe_zones: [文字|人脸|手势|数据|证据原文|关键 UI]
legibility: {text_class: body|large|display|support|source, minimum_font_px: 42, contrast_ratio_target: 4.5, busy_frame: 待验收}
subtitle_exclusion_bottom_px: 220
text_motion: 逐项浮现|mask_reveal|进度推进|路径箭头|数字变换|同位置替换|none
screen_en: 英文主文
screen_zh: 中文标注
text_status: 原文直取|忠实压缩|编辑性总结
tool: Remotion|HyperFrames|统一 Remotion 资料库候选
engine: remotion|hyperframes|lottie|d3|blender|manim|none
assets: [编号/路径/状态]
asset_assignment: {manifest_order: 1, assigned_asset_path: 用户锁定路径, assigned_script_segment_id: 当前语义段 ID, user_verified: true, assignment_locked: true, assignment_reassessed: false}
media_kind: image|video|none
master_media_ids: [母图片/母视频 ID]
source_duration_seconds: 源视频自然时长；图片留空
timeline_duration_seconds: 图片5.0-10.0；视频按自然时长/末帧保持规则
playback_mode: image_hold|natural_full_once|play_once_then_hold_last_frame|not_applicable
last_frame_hold_seconds: 源视频不足5秒时补足量，否则0
video_looped: false
video_muted: true
video_trimmed: false
fullscreen: true
original_media_clear: true
media_body_blur_px: 0
source_aspect_ratio: 16:9 或实际比例
material_class: archive_evidence|book_evidence|ordinary_image|ai_image|video|other
asset_folder: 实际文件夹
frame_treatment: image_fullscreen_bleed|image_fullscreen_contain_solid_matte|historical_evidence_split_title_source_plus_large_image|video_fullscreen_clear
text_overlay_engine: hyperframes|none
text_overlay_scope: local_text_glass_only|none
glass_problem_points: [已审要点，普通图片 1–4 项]
image_motion: slow_push|pan|focus_relay|parallax_2_5d
source_file_metadata: {file: 历史资料文件, institution: 机构, author: 作者, date_page: 日期/页码, excerpt: 关键摘录}
argument_bridge: {insufficiency_reason: 缺少何种合适媒体/图解, left_en: 双语主论点英文, left_zh: 双语主论点中文, left_font_px: 88, right_font_px: 48, right_items: [{en: 分论点英文, zh: 分论点中文}], target_ratio: 0.04-0.06}
left_component_present: true|false
right_content_flow: vertical|not_applicable
burned_in_captions: false
gpu_eligible: true|false
render_segment: SEG-xxx
transition_in: hard_cut|crossfade|push|hidden_cut|shape_match|focus_relay|chapter
sound: 人声/BGM/环境/转场/拟音/情绪 cue
reuse: 首次|回扣及新增意义
```

检查：Scene 首尾覆盖锁定音频、不重叠、不留空；同一接缝只允许一个顶层转场。

## 镜头功能与视觉缓冲

- 解释因果 → 动态图表、结构图、变量变化或关系动画。
- 提供证据 → 可读史料、原始数据、权威截图；必须能看清来源和关键区域。
- 提供氛围 → 环境素材；只承担氛围，不冒充机制或证据。
- 强调转折 → 构图、尺度、色块、空间层级或结构关系发生明确变化。
- 抽象概念优先转成节点、边、层级、流向、约束和反馈，不堆历史素材。
- 禁止让历史人物讲话画面承载旁白中的经济/制度机制解释，除非讲话内容本身就是正在引用的证据。
- 连续出现多个年份、人物、制度名称或多层因果时，必须加入时间轴、地图、结构图、数据变化或权力关系图之一作为视觉缓冲。

## 动态覆盖

知识长视频默认以动态体验覆盖不低于 75% 为目标；所有 `programmatic_opportunity=preferred` 的 Scene 都必须优先落到 Remotion/HyperFrames/五源资料库或写明可复核的失败原因。运动分为三层：

- `primary`：承担解释、比较、数据、操作、焦点、关系或转场的主要动作。
- `support`：强化层级、指向、材质建立、阅读节奏或状态回执。
- `ambient`：提供氛围、趣味、触感、节奏或空间深度；允许不承担事实解释，但必须服从主体。

推荐来源比例：

- 外部视频主画面：35%–55%
- 动态图片/资料/地图：15%–30%
- 程序化信息画面：10%–25%
- 完全静态：不高于 25%，只用于证据凝视、阅读和情绪留白

图片发生语义推近、横移、局部放大、分层视差、焦点变化、标注建立或前后对照时属于主要/辅助动态。经过明确节奏设计的呼吸、漂浮、渐变、光斑、颗粒、goo 或玻璃后图案可作为环境动态计入观看体验，但不能连续替代实质内容；若影响文字、人脸、手势、数据、证据或关键 UI，立即降强度、改路径、暂停或替换。

Remotion 和 HyperFrames 同级参与动效选型。语义准确、层级清楚、主体安全和渲染稳定合格后选择当前文案下观感更好的候选，效果接近时可优先 HyperFrames；不设引擎比例、每章配额或使用上限。依赖缺失时阻塞实现 Gate，不静默替换成空白页或重复静态 PPT。

含文字的 `remotion` / `hyperframes` Scene 默认填写 `glass_regular + faint`。背景本身是证据时使用 `evidence`，把文字移到独立安全区；不需要玻璃时填写 `none` 并在 spec 记录理由。

每 5–10 秒应有一次焦点、构图、素材、层级或观看体验变化；每 20–30 秒检查动态来源是否单一。不要机械快切，也不要靠持续背景流动掩盖主体长期不变。章节之间必须使用动态接力，普通硬切只保留给有书面理由的刻意语义撞击。

相邻程序化 Scene 比较 `engine + motion_family + motion_signature`。完全相同直接退回；同一 motion family 连用时，改变至少两个可见维度，或将后一镜动作/hold 放慢到 1.25–1.60 倍。超过 60 秒的章节至少使用 3 个 motion family，较短章节至少 2 个；文字动画在逐项浮现、mask、进度、箭头/路径、数字变化和同位置替换之间轮换。

总结、观点和程序化信息页另比较 `visual_page_id` 与 `content_fingerprint`。相邻任一重复都判为同一页面连续播放；换速度、缓动、背景或轻微排版不构成新页。禁止把同一 composition/MP4/Scene 连播两遍补时长。需要延长时，在一个 HyperFrames Scene 内写至少 3 个 `internal_phases`（字体变迁、逐项建立、进度推进、箭头闭环、数字/构图状态变化等）；否则切换到内容指纹和版式都不同的新页面。

## 素材取得顺序

1. 读取用户已核对的文案顺序与文件内素材清单，按 `manifest_order` 锁定路径和 `assigned_script_segment_id`；不重新判断、交换或跨段借用。
2. 只有清单出现明确缺项时才检索真实来源：官方机构、档案馆、博物馆、图书馆、大学数字馆藏和明确授权素材库。
3. 搜索真实视频时给中文和英文关键词；记录平台、URL、作者、授权和下载日期。
4. 找不到合格画面再用 AI 图片/视频；AI 不承担史实、数据或引用证明。
5. 章节开头、关系、机制、制度、文字说理、数据、地图、论证因果和流程必须程序化表达，不硬搜无关 B-roll。新增候选经用户核对后才并入锁定清单。

## 三类需求目录

图片：

`编号｜标题｜时间码与原句｜叙事任务｜已有判断｜中文搜索词｜英文搜索词｜来源优先级｜构图｜动态化方式｜AI 备用提示词｜性质标识`

视频：

`编号｜标题｜时间码与原句｜独立任务｜中文搜索词｜英文搜索词｜建议平台｜时长｜构图与单一动作｜复用级别｜纯视频提示词`

真人：

`编号｜开始｜结束｜完整起始句｜完整结束句｜全部台词｜段落职责｜全屏/小窗流程｜手势｜文件名｜对应音频切片`

## AI 提示词

图片提示词包含：主题、时代地点、主体、动作、环境、镜头、构图安全区、光线、材质、现实瑕疵、连续性锚点和比例。需要作为毛玻璃后景时，要求大形体、低细节、低局部对比并避开文字安全区；准确文字由后期叠加。

AI 图片需求数量不设上限，按锁定文案的视觉缺口和 `5–10 秒/张` 的计划展示时长计算；长语义段拆出主画面、细节、状态变化、衔接和备用变体，不用少量图片反复拼凑。每条写明语义段、原文范围、时间码、叙事功能、计划秒数、连续性、安全区、运动、变体角色、中英提示词和审核状态，并汇总覆盖秒数与未解决缺口。

AI 视频按语义规划，单条 `5–15 秒`、16:9、无声、无字幕、写实、一个主体动作、一个克制镜头动作、最后约 0.8 秒自然稳定；全项目需求不超过 `250` 条，不为凑满上限生成。优先请求 2560×1440、60fps；平台不支持时用其最高稳定规格生成并在后期适配，记录是否插帧。进入时间线后按源文件完整播放，不循环；视频在屏时减少额外动态说理。

通用模板：

```text
生成一段5秒横屏16:9写实视频，目标2560×1440、60fps，无声。场景为【时代/地点/环境】，主体是【人物/物体】，只完成【一个明确动作】。镜头采用【固定/缓推/横移/跟随/轻手持】，运动服务【空间建立/动作细节/情绪推进/因果结果】。光线、材质、天气和服装符合真实世界，为字幕或人物小窗预留【位置】安全区。最后约0.8秒自然减速并稳定停留。
```

## 素材复用

- 辨识度高的肖像、事件现场、地图或档案证据默认一次；明确主题回环时最多再出现一次，并增加新证据意义。
- 中性环境、手部、道路、门、账本等母素材最多 3 次；动作强、人物明显、构图独特的镜头最多 2 次。
- 每次复用至少改变 3 个维度，其中至少 2 个视觉维度：入/出点、速度、裁切、焦点、比例、版式、动作阶段、前后语境、文字、音乐段落。
- 同一母图片或母视频不得在相邻两个 Scene 连续出现；换裁切、入点、速度、调色或文字也不能规避。环境空镜相隔至少 90 秒，明显人物/动作至少 180 秒，高辨识象征镜头至少隔一个章节。跨到后面的章节可复用，但仍须三维变化、换前后镜并增加新语义。
- 同一段视频不得自行循环或前后接两遍填时长；更换匹配素材或切入程序化图解。
- 每次复用都更换前一镜、后一镜和旁白结论；第二次不得沿用相同全屏比例、相同入点和相同前后转场，第三次必须进入信息卡/分屏，不再作为全屏主镜头。
- 不用镜像、倒放或简单调色伪装重复；地图、文字、军服标识、旗帜、人物惯用手、车辆方向和因果动作禁止镜像/倒放。
- 可复用：环境、物件、匿名手部、抽象制度动作。不可复用：具体历史事件复原、唯一人物面孔、可读史料、精确地图边界和连续战斗动作。
- 高潮和结尾优先独有镜头；通用复用素材放在解释、过渡和证据呼吸段。程序化模板可反复调用，但每次替换节点、文字、数据、配色权重与运动方向。

## 画幅与字幕

- 最终视频不烧录连续字幕，只交外挂 SRT/ASS。中英双语标题、节点、标签、数字和逻辑说明属于解释图层，必须大而醒目并先过文字门禁。
- 普通/AI 图片以清晰原图全屏进入，非 16:9 使用实色衬底，不做模糊延展；只有上方文字使用局部毛玻璃。`archive_evidence` 与 `book_evidence` 采用简中＋英文标题/来源区＋大幅清晰证据图，且证据在屏时禁止动态说理。
- `argument_bridge` 左侧中英主论点字号至少 88px，右侧中英细分论点字号至少 48px；必须引用当前单一 `semantic_segment_id` 与 `source_text_ids`，不得新增观点或跨章拼接。
- 2560×1440 底部固定保留 220px 字幕排除区；所有动销、总结卡、进度条、逻辑箭头、人物小窗和关键文字都抬到其上。解释正文从 42–54px 起调，辅助文字至少 32px，来源元数据至少 26px。
- 画面右上角不放“历史资料”“情景演绎”“AI生成”“示意画面”等常驻说明；来源边界进入 manifest 和交付文档。

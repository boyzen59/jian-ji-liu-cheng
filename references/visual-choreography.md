# 画面编排、双引擎与苹果式运动硬规则

本文件把图片、真人、文字、字幕安全区、Remotion/HyperFrames 分工和相邻动效变化落成可执行规则。任何分镜、`video-spec.json`、`animation-plan.json` 和 QA 都不得只写“Apple 风”“加强动效”而缺少下列字段与证据。

## 1. 真人时间线

- 开场真人可全屏，但全屏状态从成片 `00:00` 起累计不得超过 `15.0 秒`；优先在 15 秒前最近的自然停顿开始缩窗，口播可连续，不要求切断句子。
- 开场全屏不得是裸人物。左右两侧必须由 HyperFrames 建立至少 2 个、至多 4 个与当前钩子对应的说明组件，例如问题、承诺、关键词、时间/进度、因果箭头或证据预告。组件必须避开脸、口型、手势和底部字幕区。
- 开场之后到最终总结之前，真人只能是小窗或撤下；禁止任何中段全屏例外。小窗默认圆形、固定右下并抬到字幕排除区之上；只有主体碰撞且用户批准时换位。
- 只有全片最终总结允许真人再次全屏。该 Scene 必须位于时间线结尾、承担 `summarize` 并持续到实际最后一帧；总结组件由逐镜候选比较选择 Remotion 或 HyperFrames，至少包含进度、逻辑箭头、路径线或逐项落位之一。
- 开场与结尾全屏都先确定人物安全区，再从人物、当前问题或前一镜的可见锚点“长出”说明；禁止无来源地从屏幕中央弹出卡片。

## 2. 图片与历史资料分流

`ordinary_image` 与 `ai_image` 默认使用 `image_fullscreen_clear_local_text_glass`，不是 PPT 嵌图模板：

1. 图片先作为清晰原图全画布主视觉进入；16:9 可有依据地全幅覆盖，非 16:9 使用全屏舞台 `contain` 与纯色/暖白实色衬底，保持原比例和关键主体。图片本体固定 `media_body_blur_px=0`，禁止同图模糊延展和整屏磨砂。
2. 图片承担空间与情绪，使用一个确定性主动作：缓推、横移、景深/焦点接力、2.5D 分层视差、局部证据推近或前后对照。不得机械静止，也不得无依据裁切、拉伸或制造不存在的画面。
3. 图片身份建立后，再由 HyperFrames 在字幕区上方 materialize 局部 Soft Signal 毛玻璃文字框；按口播顺序逐项列出 1–4 个同一语义段的问题/结论要点。要点不一次性堆满，落定后保留阅读 hold。
4. 图片仍是主角；毛玻璃只覆盖安全区，不把全屏图片重新缩成左侧卡片。

manifest 标为 `archive_evidence` 或 `book_evidence` 时使用 `historical_evidence_split_title_source_plus_large_image`：一侧为简体中文＋英文标题/来源说明区，另一侧为大幅清晰证据图。证据图固定 `media_body_blur_px=0`；证据在屏时禁止动态说理，只允许证据支持动作。

视频使用 `video_fullscreen_clear_local_text_glass`：清晰原画全屏、静音、只播放一次，本体 `media_body_blur_px=0`。源长不少于 5 秒时完整沿用自然时长，超过 10 秒也不裁切；不足 5 秒时完整播放后保持末帧至 5 秒。只有上方文字可由 HyperFrames 使用局部毛玻璃。

## 3. 字幕排除区与大字号

- 2560×1440 默认保留底部 `220px` 为 `subtitle_exclusion_zone`；所有卡片、进度条、逻辑箭头、人物小窗、来源面和关键文字的底边均不得进入该区。项目例外按画面高度至少保留 `15%`。
- 不因主交付不烧录字幕而取消该安全区；它服务外挂字幕、平台字幕和后续审片叠字。
- 1440p 字号从以下范围起调：章节/英雄标题 `156–220px`，主结论 `104–148px`，一级标题 `88–112px`，二级标题 `64–80px`，正文/卡片 `42–54px`，辅助说明 `32–40px`，来源元数据不得低于 `26px`。1080p 可按 `0.75` 等比换算。
- 一行只放一个自然语组。右侧存在信息面时使用竖向层级：标题 → 逐项要点 → 进度/箭头 → 来源；禁止把右侧内容横向挤成小字表格。

## 4. 苹果式逻辑，不是只套毛玻璃

每个程序化 Scene 都填写 `apple_logic`：

```yaml
apple_logic:
  purpose: 这一镜为何存在
  focal_hierarchy: 第一、第二、第三注意点
  spatial_origin: 动效从哪个可见主体/前一镜锚点产生
  material_response: 哪个层级使用 thin/regular/thick，为什么
  continuity: 入退路径和前后镜如何接力
  settle_state: 何时完全落定、阅读多久
  delight: 克制的触感/空间增益；没有则写 none
```

- Apple 感来自明确目的、可预测空间、物理连续、材质层级、即时视觉回执和克制愉悦；不来自复制 macOS/iOS 界面。
- 最重要的对象先响应，辅助项再建立；进入从当前可见状态/锚点开始，退出沿同一路径或交给场景转场完成。
- 默认临界阻尼、无弹跳；只有明确惯性动作允许一次轻回弹。玻璃要同步建立 blur、scale、边缘受光和阴影，不能只淡入 opacity。
- 简洁不是空。真人全屏、图片全屏和总结帧都必须有第二焦点和可理解的视觉路径，但同一时刻仍只允许一个主要动作家族。

## 5. Remotion / HyperFrames 双引擎

- Remotion 与 HyperFrames 同级进入程序化动效选型。逐镜比较语义准确、主体安全、渲染稳定和视觉冲击；前三项合格后选择观感更炫酷者，效果接近时优先 HyperFrames，并记录 `engine_selection`。
- Remotion 始终拥有唯一总时间线、主媒体、人物小窗、全局帧、片段嵌入和静音终渲；该工程职责不构成动效优先级。它自身也必须承担可见的媒体运动、空间接力、蒙版、标注或结构变化。
- 开场、结尾和正文程序化段都对 Remotion 与 HyperFrames 候选同场比较；不设引擎占比、每章配额或使用上限。效果接近时可优先 HyperFrames，但不得以配额替代语义判断。
- 章节开头以及因果、流程、制度关系、结构关系和文字说理段必须使用程序化动态效果解释问题。
- HyperFrames 段遵循 `build → breathe → resolve`，每个可见元素都有明确入场，使用场景转场完成前一场退出；时间线 `paused`、同步注册、有限时长、确定性、无 `repeat:-1`。
- 生产前为 HyperFrames 写 `hyperframes_recipe`、hero frame、入场顺序、转场、落定帧和 Remotion 嵌入区间；生产后必须通过 lint、validate、inspect，并审阅 animation map。

## 6. 动效丰富度与相邻去重

每个程序化 Scene 写 `motion_family` 和 `motion_signature`：

```yaml
engine: remotion|hyperframes|lottie|d3|blender|manim
motion_family: materialize|mask_reveal|focus_relay|path_draw|progress_build|type_sequence|count_transform|spatial_push|parallax_evidence|comparison_morph|chart_growth|shape_handoff
motion_signature:
  layout: full_image_overlay|split_evidence|presenter_sides|vertical_logic|data_stage|other
  direction: left_to_right|right_to_left|center_out|depth|vertical|radial
  build_order: subject_then_glass_then_text|title_then_points_then_path|data_then_conclusion|other
  easing: spring_standard|spring_gentle|sine|expo|custom
  pace_class: fast|medium|slow|very_slow
variation_from_previous:
  mode: changed|slower|not_applicable
  changed_dimensions: [layout, direction]
  pace_multiplier: 1.0
```

- 相邻两个动画解说不得拥有完全相同的 `engine + motion_family + motion_signature`。
- 每个总结页、观点页和程序化信息页另写 `visual_page_id` 与 `content_fingerprint`。相邻两个 Scene 只要页面 ID 或内容指纹相同，就视为同页连续播放，直接失败；改变缓动、速度、裁切或背景不能把重复页伪装成新页。
- 禁止复制同一 composition、MP4 或页面 Scene 连播两次补旁白时长。`duration_fill_strategy` 只能是：`not_needed`、`extend_internal_choreography` 或 `new_semantic_page`。
- 使用 `extend_internal_choreography` 时，把时长留在一个 HyperFrames composition 内，并写至少 3 个有新视觉/信息状态的 `internal_phases`，例如“标题材质化 → 关键词变迁 → 进度推进 → 箭头闭环 → 最终结论放大”；不能只延长静止 hold、重复同一 tween 或从头重播。
- 使用 `new_semantic_page` 时，新页必须同时更换 `visual_page_id`、内容指纹和主版式，并承担不同的原句/结论；只换标题颜色或背景不算新内容。
- 相邻 Scene 若沿用同一 `motion_family`，要么至少改变两个可见维度（构图、方向、建立顺序、载体、空间原点、转场），要么把后一镜的动作/hold 放慢到前一镜的 `1.25–1.60×` 并记录 `mode=slower`。
- 每章超过 60 秒时至少使用 3 个可辨认的 motion family；较短章节至少 2 个。连续两个高运动负担 Scene 后安排慢镜、证据凝视或清晰 hold。
- 文字不能只做统一淡入。轮换使用逐项浮现、mask reveal、进度推进、路径/箭头绘制、数字变换、同位置替换和关键词材质化；所有文字仍以语义组为单位，不做逐字字幕跳动。

## 7. 放行证据

Styleframe 至少覆盖：开场真人说明、普通/AI 图片清晰全屏＋局部文字毛玻璃、档案/图书证据的双语来源区＋大幅清晰证据图、清晰视频全屏＋局部文字毛玻璃、正文右下小窗＋图解、低频双栏补位、结尾真人全屏＋总结。QA 至少检查 hero frame、运动峰值、原画零模糊、文字落定、字幕排除区和实际最终帧；任何一种缺失都不得标为 `PRODUCTION_RELEASED` 或 `QA PASS`。

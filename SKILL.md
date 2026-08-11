---
name: jian-ji-liu-cheng
description: 将文稿、锁定口播、SRT、中英对照稿和用户已核对素材推进为语义大纲、video-shotcraft 辅助逐镜设计、覆盖量驱动的 AI 图片/视频需求、Remotion/HyperFrames 动效、独立声音、质检与静音 H.264 Rec.709 2K60 成片。严格沿用锁定文案与素材对应；图片需求不设数量上限，AI 视频按文案规划且最多 250 条；逐镜比较候选效果，不机械套模板或强制引擎占比。用于制定剪辑 SOP、生成 video spec、素材需求、增量双语审阅、分段渲染或完成知识长视频时。
---

# 剪辑流程

把一个全新的主题素材包推进到可交付成片。每个项目只继承方法、固定视觉系统和工程规范，不继承任何旧项目的题名、台词、人物、事实、时间码、素材编号或搜索词。

## 开始前

1. 从用户当前请求、附件和目录中提取已知信息；不要重复追问已经给出的答案。
2. 读取 `references/positioning.md`，运行独立的 AI 初期定位模块。每轮只问 1–2 个最关键问题；资料足够时直接形成项目简报。
3. 读取 `references/fixed-style.md`、`references/apple-glass-style.md`、`references/visual-choreography.md` 和 `references/material-lock-media.md`。视觉主题固定为 `Soft Signal / 亲密 · 温暖`，并把 Apple 式目的、焦点层级、空间锚点、材质响应、物理连续和落定阅读写进逐镜方案；不得只贴“Apple 风/毛玻璃”标签。不得询问或替换主题、强调色和字幕色。用户明确要求本项目例外时，记录覆盖项，不改母版。
4. 读取 `references/dependency-routing.md`，只调用当前任务需要的 Skill/插件/外部运行时；缺失项先做预检，不把未安装能力写成已完成。
5. 读取 `references/remotion-library-routing.md`，确认内置 `catalog.json` 可用；需要核对时运行 `scripts/query_remotion_library.py stats`。
6. 读取 `references/chapter-motion-media-render.md`，把章节首卡、程序化动效强制段、用户核对素材指派锁、媒体自然时长、相邻去重、外挂字幕、音乐、GPU、五分钟分段和静音母版视为硬规则。
7. 若要创建项目目录，运行 `scripts/init_project.py`。它只补缺失文件，不覆盖已有内容。

## 硬边界

- 当前项目事实只来自用户输入和可核查来源。未知项写 `[待补充]` 或 `[待用户确认]`，不得编造。
- 旧项目专属内容不得进入本 Skill 或新项目母版。
- 锁定录音存在时，录音精确时长是成片总时长；中文 SRT 存在时，它是首选字幕时间骨架。
- 主交付固定为 `2560×1440`（16:9 语境的 2K/QHD）、`60fps CFR`、`H.264/AVC High`、`yuv420p`、`Rec.709`、MP4、无音频流；不使用 H.265/HEVC，不烧录连续字幕。外挂字幕、录音、音乐和 SFX 独立交付。只有用户明确要求项目例外时才覆盖，并记录批准来源。
- 动效分为 `primary / support / ambient`。主要动效可解释语义、焦点、关系、数据、操作或转场；辅助/环境动效也可只提供氛围、趣味、触感、节奏或空间层次，但不得遮挡、扭曲、误导或抢夺文字、人物、手势、数据、证据和关键 UI。
- 含文字的程序化镜头默认使用一层 Soft Signal 毛玻璃信息面；文字完全不透明，正文/字幕目标对比度至少 `4.5:1`，大字至少 `3:1`。
- 玻璃后的背景动画、图案或影像必须若隐若现：能感知方向、色块和节奏，但不与文字抢读。禁止整屏磨砂和浅玻璃叠浅玻璃。
- 真人以完整连续语义段为时间选择单位。只有总开头与实际最终结尾允许全屏；中段一律使用抬高的右下圆形小窗或撤下，底边避开 `220px` 字幕排除区。只有主体碰撞且用户批准时才换位。最终全屏必须持续到成片最后一帧，并在首帧、切换帧和最终帧逐帧验收。真人累计时长仍必须小于总时长 `20%`。
- Remotion 与 HyperFrames 同级参与程序化动效选型；逐镜先保证语义准确、层级清楚、主体安全和渲染稳定，再选择当前文案下观感更好的方案。效果接近时可优先 HyperFrames，但不设任何引擎使用比例、每章配额或上限。Remotion 只保留唯一总时间线、媒体运动、人物小窗、片段嵌入、外挂字幕时间骨架与静音终渲；不要把 SRT 烧进画面。
- 使用统一 Remotion 资料库时只迁移与当前文案匹配的运动语法、时值关系和组件结构，不照搬产品 UI、品牌皮肤、主题色或默认高能节奏；所有候选必须重新蒙皮并经过主体保护检查。
- 标题、观点、重点文字、数字、流程、时间轴、因果、逻辑关系、地图轨迹和截图讲解等适合程序化表达的内容，必须优先使用 Remotion/HyperFrames 和五源资料库；不采用时逐镜写明不可用原因。
- 用户已核对的文案顺序、文件内清单和素材对应关系是唯一素材路由；严格按清单顺序和指定语义段使用，不重新判断匹配关系、不交换、不跨段借用。文件缺失或损坏时报告阻塞，不自行重配。
- 图片单张展示 `5–10 秒`。视频源时长不少于 5 秒时完整播放一次并沿用自然时长，超过 10 秒也不裁切；不足 5 秒时只播一次并保持末帧补足 5 秒。所有视频静音、不循环。
- 同一母图片或母视频不得在相邻两个 Scene 连续出现；视频不得循环两遍填时长。相邻两个动画解说也不得使用完全相同的引擎、动效家族、构图、方向、建立顺序、缓动和速度；复用同一动效家族时必须改变至少两个可见维度，或把后一镜放慢到 `1.25–1.60×` 并延长落定。允许跨到后续章节复用，但仍执行间隔、三维变化、换前后镜和新增语义规则。
- 同一个总结页、观点页或程序化信息页不得拆成相邻两个 Scene 连播，也不得把同一页面/同一渲染片段重复两遍补时长。需要延长时，在单个 HyperFrames 段内使用新的字体状态、逐项显现、进度、箭头、路径、数字或构图阶段继续推进；否则切换到 `visual_page_id`、内容指纹和版式均不同的新页面。
- 按素材清单中的 `material_class` 分流，不依赖任何项目专属文件夹名。`archive_evidence` 与 `book_evidence` 均视为证据类素材：使用简体中文＋英文的标题/来源区和大幅清晰证据图；证据图本体 `blur=0`。证据或图书内容在屏时禁止叠加动态说理，只允许慢推、局部证据推近、聚光、圈注、来源翻译等证据支持动作。
- `ordinary_image` 与 `ai_image` 使用清晰原图全屏，图片本体 `blur=0`；按语义在缓推、横移、纵移、景深接力、2.5D 视差、遮罩揭示、局部证据推近、前后对照和空间接力中选择，不得全片只做左右放大。非 16:9 使用 `contain` 加实色衬底，不做模糊延展。视频同样保持清晰原画全屏；毛玻璃只属于媒体上方的文字承载层，不是“视频全屏毛玻璃”。
- 禁止空白页、旋转文字、把文件名或内部素材 ID 显示在成片中。屏显要点必须从当前原文归纳，可按内容选择 `1/2/3`、关键节点、路径、对照或因果链，不能把所有内容机械改成同一种卡片。
- 允许低频使用 `argument_bridge` 双栏补位：左侧双语大论点，右侧动态建立 2–4 个双语细分论点/节点/路径/箭头。仅在缺少合适图片、视频或具体动态图解时使用，目标占全片 4%–6%、硬上限 6%，每章最多一场且不得连续。
- 2560×1440 默认保留底部 `220px` 字幕排除区；任何卡片、总结、进度条、逻辑箭头、人物小窗和关键文字都必须抬到其上。正文章节/英雄标题从 `156–220px` 起调，普通解释正文从 `42–54px` 起调，辅助说明不低于 `32px`，来源元数据不低于 `26px`。
- 右上角不得常驻“历史资料”“情景演绎”“AI生成”“示意画面”等来源标签；来源边界写入 manifest 和交付文档。
- 任何自动生成都必须可重复；禁用时间随机、无限循环和运行时网络内容。

## 完整流程

### 0. 建立项目状态

- 审计文稿、录音、SRT、翻译、图片、视频、录屏、字体、品牌规范和参考片。
- 只读文件名能满足审计时，不打开图片内容；需要视觉判断时再查看。
- 创建来源清单，区分：用户提供、公开授权、官方资料、AI 生成、程序化生成。
- 记录平台、画幅、帧率、目标时长、语言、受众、核心命题、资料边界和交付格式；未指定时直接采用固定的 H.264 / Rec.709 / 2560×1440 / 60fps CFR / 无音频流主交付。

### 1. AI 初期定位

按 `references/positioning.md` 执行。产出 `01_brief/project-brief.md` 和 Gate 状态：

- `READY`：关键定位、时间基准和素材边界已清楚，可进入分镜。
- `READY_WITH_ASSUMPTIONS`：仅有低风险缺省项，明确写出假设后继续。
- `BLOCKED`：缺少会实质改变成片的选择或锁定音频/文稿，停止昂贵制作并请求用户补充。

### 2. 锁定文字、时间轴与场景类型大纲

- 先解析录音时长和中文 SRT，再把正文按语义映射到时间段。
- 英文按中文语义段配合，不因英文更长而改变录音时间；需要时压缩屏显。
- 按 `references/storyboard-assets.md` 拆分完整语义单元、章节和真人连续段。
- 先生成 `04_spec/outline-scene-types.json`：逐段判断 `章节总览 / 图表 / 截图 / 数据 / 重点文字 / 档案证据 / 地图 / 结构关系 / 环境 / 真人`，写出证据需求与观看目标；每个正文章节先插入 `chapter_title` 双语 PPT 总览，再把类型大纲转换为可执行 `video-spec.json`。禁止直接从文稿跳到镜头装饰。
- 标记原文直取、忠实压缩、编辑性总结三类屏显；编辑性总结不得冒充原话。

### 3. 文字审阅 Word 门禁

当前既有文字动效审阅全部视为通过。只有新增或改字时，才重新进入 Remotion、HyperFrames 和其他含文字画面的增量 Word 门禁；仅改版式、字号、位置、材质或运动而不改字时不重审。

1. 为所有含文字镜头建立 `03_review/text-review.json`；字段规范见 `references/text-review-gate.md`。
2. 运行 `scripts/build_text_review_docx.py`，生成带生成时间戳的 `03_review/动效文字执行手册.docx`。
3. 文档必须逐条列出时间码、原文、英文主文、中文标注、载体、内容状态、问题、建议修改、理由和用户决定栏。
4. `review_mode=delta_only`、`baseline_existing_text_approved=true`；只把 `change_kind=new|changed` 的增量行送审。若增量行存在 `必须修改`、`待确认` 或缺少批准证据，停止对应含文字画面实装。
5. 任何新增或改字都递增版本号、更新生成时间戳并重出 Word；`layout_only` 不重审，不可借排版调整静默改字。

### 4. 分镜与素材放行

读取 `references/storyboard-assets.md` 和 `references/production-workflow.md`：

- 每镜一个主要信息和一个主要动作；精确到 0.1 秒或帧。
- 每个 Scene 写齐：时间、原文范围、场景类型、功能、修辞任务、观看目标、载体、构图、视觉模式、`visual_page_id`、内容指纹、补时策略、动效意图、动效角色、引擎、动效家族、动效签名、相邻变化、Apple 逻辑、资料库候选/选中 ID、运动、文字动效、字号、屏显、材质、背景可见度、主体安全区、底部 220px 字幕排除区、可读性、工具、素材、转场、声音、复用状态。
- 每个 Scene 另写 `programmatic_opportunity`、`semantic_segment_id`、同段文字来源、用户锁定素材顺序/路径/指派状态、母素材 ID、源时长、时间线时长、播放模式、原画清晰度、局部文字覆盖层、是否章节首卡、是否烧录字幕、GPU 适用性与分段编号。
- 功能优先映射：解释因果用动态图表/结构关系；提供证据用可读史料/来源；提供氛围用环境素材；强调转折用结构变化。抽象概念先转成图形关系，不靠堆叠历史素材。
- 避免“历史人物讲话画面 + 旁白解释经济机制”等视觉与信息脱节。连续出现多个年份、人物、制度名称或多层因果时，插入时间轴、地图、结构图、数据变化或权力关系图作为视觉缓冲。
- 先读取用户已核对的素材清单，锁定清单顺序和文案对应关系，不再重判素材匹配。只有清单明确缺项时才列真实检索、AI 补缺或程序化解释；新增素材经用户核对后才写回锁定清单。
- 输出完整 video spec、精简素材目录、真人连续段清单和帧级时间轴。
- 在实装前生成覆盖量驱动的 `asset-requirements.json`：逐个语义段计算缺少实拍、史料、图书或程序化解释后的剩余视觉时长。AI 图片需求数量不设上限，不以“少做清单”为目标；按 `5–10 秒/张` 的计划展示时长，为长段落拆出主画面、细节、状态变化、转场衔接和备用变体，直至覆盖文案流程且避免重复拼凑。
- 每条 AI 图片需求必须写 `semantic_segment_id`、原文范围、时间码、叙事功能、计划展示秒数、主体/动作/环境、连续性锚点、构图与安全区、画面运动、`variant_role=primary|detail|transition|backup`、`expected_use_count=1`、中英提示词和审核状态。汇总 `planned_image_seconds`、`requested_image_coverage_seconds` 与 `unresolved_gap_seconds`；必需语义段仍无主候选、备用或明确程序化回退时不得放行。
- AI 视频也按语义缺口逐条规划，不为凑数生成；总数硬上限 `250`。每条默认 `5–15 秒`，时长取能完整表达一个主体动作、一个镜头动作并保留稳定结尾的最大合理值；写明原文、时间码、语义动作、开头/结尾状态、连续性、主体保护、中英提示词和验收点。视频在屏时减少额外动态说理，优先让昂贵视频自身承担叙事。
- 分镜、素材和文字审阅都通过后，记录 `PRODUCTION_RELEASED`。

### 5. video-shotcraft 语义逐镜与双引擎动效路由

凡有 `programmatic_opportunity=preferred|support` 的 Scene，先读取 `references/shotcraft-routing.md`，再读取 `references/remotion-library-routing.md`：

- 完成“Shotcraft pass”：把当前锁定原文转译为论点、关系、动作、证据和阅读节奏；从 video-shotcraft 及 RVE、Scenes、Curvable、Playground 中寻找多个可行语法，并与 HyperFrames 候选同场比较。video-shotcraft 是逐镜思考与动作语法库，不是必须逐卡使用的模板配额。
- 检查候选完整卡片、TSX/源码、demo/preview 和时值；记录来源、style key、语义适配、阅读负担、主体安全、视觉冲击、采用/淘汰理由。不得只看名称选卡，不得一章批量套同一模板，不得为适配模板改写原文事实。
- 动态说理不限于卡片。根据原文选择路径绘制、时间轴、关系网、空间揭示、数字建立、对照变形、材料转场、图表增长、节点接力或少量卡片；动效要覆盖缺少图片/视频的叙事区间，但同一时刻保持清晰主动作。

- 先分析完整文案段的修辞功能、观众注意点、理解目标、镜长、阅读负担、能量与主体安全区；Remotion 与 HyperFrames 同级评分，前三项合格后选更炫酷者，效果接近时选 HyperFrames。
- 运行 `scripts/query_remotion_library.py suggest`，从 464 个统一条目中取得主要候选与可选环境候选；把结果、选择理由和 catalog revision 写入 `04_spec/animation-plan.json`。
- 对前 3 候选完整读取 catalog 条目和 `source_path`；有 `demo_paths`、离线 MP4 或 GIF 时必须一起检查。Shotcraft 细节另读 `references/shotcraft-routing.md`。
- 选 1 个主要条目，可再选 1 个环境条目。保留适合当前句的动作语法、关键时值、hold 与已知坑；按 Soft Signal 与 Apple 毛玻璃规范重新蒙皮。
- 环境动效可以只服务观看体验；复杂阅读时减速、停稳或避开主体，并在背景峰值帧验证文字、人物、数据和证据仍清楚。
- 为每个程序化 Scene 写 `engine`、`motion_family`、`motion_signature`、`variation_from_previous` 和 `apple_logic`；相邻完全同签名直接淘汰。沿用同一家族时至少改变两个可见维度，或明确使用 `1.25–1.60×` 慢速变体。
- 同一种招牌动效默认只当一次主角；必要复用必须改变语义、载体、构图和动作阶段。章节超过 60 秒时至少出现 3 个可辨认的动效家族，较短章节至少 2 个。
- 每章章节首卡和章节接缝都必须有明确 Remotion/HyperFrames 候选比较与选型；章节间不得退化为裸硬切。章节首卡使用 PPT 式全屏超大双语总结，内容从本章原文归纳。
- 不以 Remotion 或 HyperFrames 的数量、占比作为质量指标；只统计动效覆盖、语义适配、主体保护、候选比较证据与观看清晰度。依赖缺失时在实现 Gate 阻塞并报告，不能静默退化成空白页或重复静态卡片。
- 章节开头以及因果、流程、制度关系、结构关系和文字说理段必须用程序化动态效果解释，不得用普通 B-roll 或静态图片替代。
- 文字动效在逐项浮现、mask reveal、进度推进、路径/箭头绘制、数字变换和同位置替换之间轮换；不允许整片只用统一淡入。
- 总结/观点信息页写 `visual_page_id` 和由已审文字/节点生成的 `content_fingerprint`；相邻值重复直接退回。`duration_fill_strategy=extend_internal_choreography` 时必须在同一 HyperFrames composition 内写出至少 3 个有新信息状态的 `internal_phases`，不得复制 Scene 或重播成片段。

同时按 `references/advanced-animation-routing.md` 选择扩展引擎：

- Lottie：确定性矢量图标、标识、轻量循环与可重着色解释件；项目局部安装 `@remotion/lottie` 与 `lottie-web`。
- Remotion + D3：GDP 排名竞赛、时间序列、台风轨迹、地图路径和其他数据关系；D3 只计算尺度、布局、路径和插值，时间统一由 Remotion 帧驱动。
- Remotion + Blender：复杂产品级 3D、真实材质、灯光与镜头运动；Blender 离线渲染，Remotion 负责合成、字幕和总时间线。
- Manim：数学、科学、科技、科普中的公式推导、几何关系、状态机和算法过程；命中时调用已安装的 `manim-video` Skill，输出独立片段再嵌入 Remotion。
- 动效不得成为无说明的填充装饰；氛围和视觉体验本身可以是明确功能，但必须写出 `visual_experience_gain`，且不得影响主体。

### 6. 实现

- Remotion 建立唯一主 Composition；总帧数由锁定音频换算。连续字幕只作为外挂时间骨架，不注册为画面层。
- Remotion 本身必须实现可见的媒体推移、人物缩窗、蒙版、标注、结构变化或空间接力，不得把所有动作外包后只做静态容器。
- HyperFrames 输出有明确入点/出点的独立信息段，再嵌入主时间线；每段先做 hero frame，再按 `build → breathe → resolve` 编排，全部可见元素有入场，使用有限、确定性的 GSAP 时间线。实装后运行 lint、validate、inspect 并审阅 animation map。
- Remotion 与 HyperFrames 共用同一材质 token；玻璃、文字和背景分层，先建立材质再完全显字，背景常态保持 faint/subtle。
- 只复制选中条目和其明确依赖，不把五个上游工程或 showcase 注册表整体并入成片；Playground 条目先移植到当前 Remotion API。
- 默认使用接近临界阻尼的 spring，入场和退场沿同一路径；只有明确惯性语义允许轻微回弹。
- 每镜完成就渲染至少两个验收静帧；每轮修改后重渲整片。
- 真实视频与 AI 视频默认静音，除非其现场声本身是证据且用户允许使用。
- 图片保持清晰原图全屏并展示 5–10 秒；非 16:9 只用实色衬底。视频保持清晰原画全屏、静音、不循环：源长不少于 5 秒完整自然播放，源长不足 5 秒只播一次后保持末帧至 5 秒；生成视频按需求单使用 5–15 秒合理时长。图片/视频本体禁止磨砂，只有上方文字可使用局部毛玻璃。证据类与图书类素材在屏时禁止动态说理。
- 不在画面时间线锁定前精钉 SFX。
- 超过 30 分钟的视频，在每 5–8 分钟设置一个 `attention_reset`：新问题、新案例、新视觉形式或新观点；不能只靠持续加信息维持观看。
- 先运行 `scripts/build_render_plan.py <project_root>`，按锁定音频和 Scene 边界生成每段不超过 300 秒的渲染计划。脚本必须探测逻辑线程、物理内存和 NVIDIA GPU，给出并发阶梯、显式媒体缓存预算和 OffthreadVideo 线程数；默认从约 75% 逻辑线程启动，只在分段之间按实测吞吐自适应升降，不在运行中的分段盲目改参。
- 每个运行中分段同时启动 `scripts/watch_render_progress.py`。无论画面是否继续推进，都必须每 `300 秒`向用户发一次固定心跳；每段完成、失败、GPU/CPU 回退或重试立即汇报。连续 `180 秒`没有帧号、日志或输出文件增长时自动生成停滞诊断；达到 `300 秒`硬停滞时立即报告并只处理当前分段。
- 资源目标是提高有效吞吐，不是追求所有占用率恒为 100%。CPU 工作区间 75–95%；GPU 适用镜头目标 65–95%；RAM 工作区间 55–78%、硬上限 85%；VRAM 工作区间 55–85%、硬上限 92%。低利用率且有内存余量时提高下一段并发；触碰软/硬上限、吞吐不再提升或解码错误时降低下一段并发。

### 7. 自动声音

读取 `references/sound-and-mix.md`，需要自动建表时运行 `scripts/build_sound_plan.py`：

- 六层：人声、BGM、环境音、转场音、拟音、情绪音。
- 人声中心、清楚、稳定；BGM 按文案和章节情绪自动设计，优先原创 AI 轻音乐或 YouTube Studio Audio Library 合规曲目，并在人声区自动 ducking，不抢字头。
- 环境音轻铺空间；转场音只强化重要切换；拟音与点击、翻页、卡片落位、数字跳动逐帧同步；riser/impact/swell 只服务高潮和转折。
- 所有声音使用中央 cue 表和相对镜头起点/拍号，不写散落的裸帧号。
- 以平台规范和实际听感定响度，制作时保留峰值余量，最终用耳机、手机扬声器和普通电脑三端试听。

### 8. 质检与交付

读取 `references/deliverables-qa.md`，运行 `scripts/validate_project.py`：

- 校验时间线连续、开场全屏不超过 15 秒、正文无全屏人物、结尾双侧总结、普通图片全屏/历史资料分流、底部 220px 字幕排除区、最小字号、相邻动效签名变化、Remotion/HyperFrames 双引擎覆盖、HyperFrames 工具检查、Apple 逻辑、文字审阅门禁、统一资料库 revision 与有效 ID、动效选择理由、主体保护、主题 token、毛玻璃材质、字体对比度、背景可见度、字幕色、素材来源、声音 cue、动态覆盖和输出规格。
- 修复项回到文字、分镜、实现或声音对应阶段，不在终检报告里掩盖。
- 终检必须回答：是否解释原因而非只讲结果、是否有逻辑跳跃、关键结论是否有依据；前 30 秒是否吸引、中段是否疲劳、结尾是否闭环；视觉是否服务内容、多语言是否方便。目标是理解效率最高，不是信息最多。
- 按 `references/delivery-documents.md` 生成：`视频剪辑执行说明书`、`图片资料搜集需求单`、`图片AI生成需求单`、`视频AI生成需求单`、`真人露脸补录台词清单`、两类补录音频切片和 `动效文字执行手册`；另交外挂字幕、AI/资料音乐来源表、stems 与审片混音。
- 结构化输入齐全后运行 `scripts/build_delivery_documents.py <project_root>`；有真人段时再运行 `scripts/build_presenter_audio.py <project_root>`。脚本生成结果仍须按 Documents 流程渲染并逐页检查。
- 终渲严格按 `references/production-workflow.md` 的固定编码段执行，并运行 `scripts/verify_master_media.py <final.mp4>`；主 MP4 中出现任何音频流都判失败。编码标签通过后仍须抽帧检查实际 Rec.709 观感、黑边、拉伸与主体清晰度。
- 交付一份无任何音频流、无烧录字幕的静音视频母版；另交外挂字幕、用户人声、BGM、环境、SFX、审片混音、工程、来源记录、文字审阅 Word、video spec 和素材清单。

## 资源索引

- `references/positioning.md`：独立 AI 追问模块与 Gate。
- `references/fixed-style.md`：Soft Signal 精确 token 与橙色字幕。
- `references/apple-glass-style.md`：Apple 式毛玻璃、字体可读性、背景显隐、spring 与验收。
- `references/visual-choreography.md`：图片全屏/历史资料分流、15 秒真人时间线、字幕排除区、大字号、双引擎覆盖、相邻动效变化和 Apple 逐镜逻辑。
- `references/material-lock-media.md`：用户核对素材清单锁、双引擎同级选型、原画保护、视频自然时长、低频双栏补位和文字增量审阅。
- `references/text-review-gate.md`：时间码文字审阅 Word 规范。
- `references/storyboard-assets.md`：语义分镜、真人、动态覆盖、素材和提示词。
- `references/chapter-motion-media-render.md`：章节首卡、程序化优先、素材贴合、5–10 秒、相邻去重、外挂字幕、音乐、GPU 五分钟分段和静音母版。
- `references/dependency-routing.md`：已安装 Skill/插件、项目级依赖和外部运行时的调用边界。
- `references/advanced-animation-routing.md`：Lottie、D3、Blender、Manim 的选型、时间线和回退。
- `references/delivery-documents.md`：六类文档、双语提示词、补录提示音与素材复用规范。
- `references/remotion-library-routing.md`：五源统一资料库、文案意图分析、候选检索、评分、主体保护和 animation plan。
- `references/shotcraft-routing.md`：Shotcraft 配方、样片与 demo 的深读规则。
- `references/sound-and-mix.md`：六层声音、ducking、钉帧与响度。
- `references/production-workflow.md`：阶段、Gate、工具边界与返工回路。
- `references/deliverables-qa.md`：目录、交付和验收。
- `assets/remotion-library/catalog.json`：464 条统一索引；不要手工改，运行 `scripts/build_remotion_library.py` 重建。
- `assets/remotion-library/sources/`：五个上游的离线源码、卡片、样片、预览与授权材料。
- `scripts/build_delivery_documents.py`：从项目 JSON 生成六类文字/Word 文档。
- `scripts/build_presenter_audio.py`：生成精确原声切片与前后 5 秒纯静音、起止双提示音 guide WAV，并用 ffprobe 验证时长。
- `scripts/build_render_plan.py`：探测硬件，按 Scene 边界生成每段不超过 300 秒的 GPU 优先、自适应并发渲染计划和缓存预算。
- `scripts/watch_render_progress.py`：每 15 秒采样 CPU/GPU/RAM/VRAM 与帧/日志/输出增长，每 5 分钟固定心跳，180 秒停滞自动诊断，300 秒硬停滞报警。
- `scripts/verify_master_media.py`：用 ffprobe 严格验收 MP4 / H.264 High / Rec.709 标签 / 2560×1440 / 60fps CFR / 无音频流。

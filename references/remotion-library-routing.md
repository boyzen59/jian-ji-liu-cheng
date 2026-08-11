# 统一 Remotion 动效资料库与文案选型

本资料库给 Remotion 与 HyperFrames 提供运动语法参考，但 catalog 本身是 Remotion 五源索引，不得因为 catalog 条目多就挤掉 HyperFrames。两个引擎同级参与动效选型：语义准确、主体安全和渲染稳定合格后选视觉冲击更强者，效果接近时优先 HyperFrames。Remotion/可迁移语法查询 catalog；HyperFrames 使用已安装技能的 GSAP、版式、转场和 QA 工作流，不能伪造 catalog ID。

## 资料库是什么

`assets/remotion-library/` 把五个来源整理为一个离线、可检索、可追溯的资料库：

| 来源 | 当前离线内容 | 最适合承担 | 接入方式 |
|---|---:|---|---|
| video-shotcraft | 104 张配方卡、161 个样式、161 条 MP4、配套 demo 与音频 | 精确镜头语法、时值、运镜、转场、交互和已知坑 | 读卡 + 看样片 + 读对应 TSX，再适配 |
| RVE | 81 个独立 TSX 模板 | 图表、文字、媒体、常用转场和轻量背景 | 复制单文件并改 props/视觉 |
| Scenes | 201 个场景 | 广覆盖的文字、数据、UI、布局、主题、粒子和液态场景 | 复制场景及它依赖的 `common` 工具 |
| Curvable | 14 个确定性组件与 GIF 预览 | 高质感文字、暖色背景、3D 合成与 frosted stats | 按组件契约接入，补齐可选 peer |
| Playground | 7 个 goo 实验 | 液态、柔软、触感和趣味视觉参考 | 从 Remotion 2.1 手工移植到当前版本 |

统一索引 `assets/remotion-library/catalog.json` 当前有 464 个可选条目。catalog 内的 `source_path`、`preview_path` 和 `demo_paths` 都以 `assets/remotion-library/` 为基准；查询器另返回可直接从 Skill 根目录读取的 `*_from_skill_root` 路径。`source-manifest.json` 记录快照提交、授权和兼容级别；`THIRD_PARTY_NOTICES.md` 记录发布前的授权检查。不要扫描 `node_modules`，资料库已刻意排除依赖、缓存和构建产物。

## 先判断程序化机会，再找动效

每个 Scene 先写 `programmatic_opportunity=preferred|support|not_suitable`。章节开头以及因果、流程、制度关系、结构关系和文字说理段固定为 `preferred`；标题、观点、数字、步骤、对照、地图轨迹、截图讲解和可结构化知识默认 `preferred`。必须让 Remotion/HyperFrames 同级候选；五源有匹配条目时先看条目和样片。只有必须凝视原始证据、完整真人表演或不可拆真实动作时才可 `not_suitable`。

对每个 Scene 的完整语义段，先写出以下判断，不从“哪个效果好看”开始：

```yaml
script_excerpt: 当前完整文案
rhetorical_function: 抛题|解释|证据|比较|关系|数据|演示|转折|章节|总结|情绪
viewer_should_notice: 观众此刻首先注意什么
viewer_should_understand: 观众在本镜结束时应明白什么
animation_intent: explain|focus|compare|relate|quantify|demonstrate|transition|identity|rhythm|atmosphere|delight
motion_role: primary|support|ambient|mixed
energy: low|medium|high
reading_load: low|medium|high
duration_seconds: 实际镜长
subject_safe_zones: [文字, 人脸, 手势, 数据, 证据原文的区域]
subtitle_exclusion_bottom_px: 220
engine: remotion|hyperframes|lottie|d3|blender|manim
motion_family: 动效家族
motion_signature: {layout: 构图, direction: 方向, build_order: 建立顺序, easing: 缓动, pace_class: 速度}
variation_from_previous: {mode: changed|slower|not_applicable, changed_dimensions: [], pace_multiplier: 1.0}
visual_page_id: 总结/观点/程序化信息页的全片唯一 ID
content_fingerprint: 已审标题、要点、节点、结论的稳定指纹
duration_fill_strategy: not_needed|extend_internal_choreography|new_semantic_page
repeat_page_to_fill_duration: false
internal_phases: [同一 composition 内的状态推进]
apple_logic: {purpose: 目的, focal_hierarchy: 注意点顺序, spatial_origin: 空间锚点, material_response: 材质层级, continuity: 前后接力, settle_state: 落定阅读, delight: 克制增益或 none}
```

常见文案信号：

| 文案信号 | 首选意图 | 常见动效语法 |
|---|---|---|
| “为什么/因此/导致” | explain + relate | 节点汇入、线条接力、阶段建立、原因到结果 |
| “以前…现在…” | compare + quantify | 同尺度前后对照、数字变换、双列或滑杆 |
| “关键是/唯一/最重要” | focus | 其他层降权，主证据抬起、圈注或聚光后落定 |
| 三项以上步骤/时间 | relate + rhythm | 进度步、时间线、逐项落位；结束后留读 |
| 点击、输入、发送、拖拽 | demonstrate | 光标与 UI 状态一一回执，不用抽象粒子代替操作 |
| “但是/然而/接下来” | transition | 语义硬切、形状接力、短推移或藏切 |
| 开场、章节、总结、行动句 | identity | 全屏超大双语标题、章节总览、品牌收束，保持明确 hold |
| 情绪铺垫、呼吸、期待、轻松 | atmosphere / delight | 低权重渐变、光斑、粒子、goo 或材质流动 |

同一句可能同时触发多个意图。先决定主意图，再决定是否需要一个辅助意图和一个可选的视觉体验层。

## 调用方法

从 Skill 根目录运行：

```bash
python scripts/query_remotion_library.py stats
python scripts/query_remotion_library.py suggest --text "以前要十分钟，现在只要三十秒" --task "数据对比" --energy medium --limit 5
python scripts/query_remotion_library.py search "timeline warm" --layer primary --limit 10
python scripts/query_remotion_library.py show "rve:comparison-chart"
```

`suggest` 会返回两组候选：

- `primary_candidates`：供 `primary_selection` 选择的主条目候选；这里的 primary 表示“本镜主选条目”，不要求 catalog `layer_fit` 必须含 `primary`。例如承包整个接缝的 transition/support 条目仍可成为主选动作，但不能因此把它误当成主体内容层。
- `ambient_candidates`：氛围、节奏、趣味、触感和深度候选，可增强观看体验，但必须服从主体保护。

检索结果只是短名单，不是自动批准。对排名前 3 的条目执行：

1. 用 `show <id>` 读取完整元数据。
2. 完整读取 `source_path`；若有 `demo_paths`，只读取与 style-key 对应的实现；若有 `preview_path`，按正常速度观看并抽查开始、峰值、落定帧。
3. 检查依赖、Remotion 版本、字体、图像、CanvasKit/WebGL 和随机实现。Playground 一律按旧版移植处理。
4. 把上游的内容、品牌、颜色、字体和产品 UI 替换为当前项目内容与 Soft Signal token；保留真正有价值的运动语法、时值关系和物理手感。
5. 记录首选、备选和未选理由，不能只写“更好看”。

每个正文章节至少要有两类明确选择：`chapter_title` 的全屏 PPT 式动态总览，以及进入正文的章节接缝动作。章节标题用 156–220px 起调并铺满主视觉区；章节接缝不得退化为裸硬切。普通内容切换也优先内容内接力、短叠化、推移、遮挡藏切或形状接力。

## HyperFrames 强制路由

以下镜头必须把 HyperFrames 作为同级候选，并在效果接近时优先其 recipe：

- 开场 15 秒以内全屏真人的左右说明组件；
- 清晰图片/视频全屏后逐项 materialize 的局部文字毛玻璃；
- 章节总览、清单、因果、进度、逻辑箭头、数字对照和观点推进；
- 最终全屏真人左右的 2–4 个总结组件与闭环路径。

不设 Remotion/HyperFrames 的使用占比、每章配额或上限。每个程序化 Scene 先完成 Shotcraft pass，并对 Remotion、HyperFrames 与五源候选同场比较；效果接近时可优先 HyperFrames。选中 HyperFrames 时填写 `hyperframes_recipe`、hero frame、入场顺序、转场、build/breathe/resolve 时值、落定帧、嵌入时间码和 fallback，并运行 lint、validate、inspect。Remotion 始终拥有总时间线和最终合成，但不因此获得动效选型优先级。

HyperFrames 主选可在 `primary_selection.id` 使用 `custom`，但 `custom_reason` 必须写明为何采用 HyperFrames，`motion_grammar` 必须写清 GSAP 属性、空间锚点和时值；不要把 `custom` 写成“没有找到模板”。

如果某个效果的识别机制依赖暗场、霓虹原色、强反差、全屏频闪或上游品牌材质，换成 Soft Signal 后机制失效，就直接淘汰；不得为了“已经入选”而强行换肤。

上游更新后，用 `scripts/build_remotion_library.py` 重建索引；它会校验 104/161/161、81、201、14、7 的当前快照完整性，并生成新的 `catalog_revision`。

## 选型评分

人工复核按 22 分制：

| 维度 | 分值 | 判定 |
|---|---:|---|
| 文案/语义贴合 | 0–5 | 动作是否表达当前句的重心或观看任务 |
| 出现时机与节奏 | 0–4 | 是否适合实际镜长、语速、停顿和章节位置 |
| 主体保护 | 0–5 | 是否始终保护文字、人脸、手势、数据和证据 |
| Soft Signal 适配 | 0–3 | 能否换肤为温暖、亲密、Apple 式毛玻璃且不失真 |
| 视觉体验增益 | 0–3 | 是否提供氛围、层次、触感、期待或节奏愉悦 |
| 工程可控性 | 0–2 | 依赖、版本、确定性和渲染成本是否可接受 |

主体保护低于 4 分直接淘汰；总分相同时，优先依赖少、预览完整、容易降级的候选。视觉体验增益可以成为选择理由，但不能用它抵消主体保护失败。

## 装饰与视觉体验的新规则

动画可以只承担氛围、趣味、触感、节奏或空间层次，不要求每一个运动都解释事实。它必须被声明为 `support` 或 `ambient`，并满足：

- 主体层永远更清楚：文字完全不透明；人物、人脸、手势、数据、证据原文和关键 UI 不被遮挡、扭曲或误导。
- 毛玻璃后的运动常态可感知但不抢读，遵守 `apple-glass-style.md` 的 opacity、blur、对比和安全区；复杂阅读期间减速、停稳或移出文字背后。
- 不用强闪、快速高对比扫光、密集粒子或大幅视差穿过主体；不制造新的事实重音或把次要信息变成主角。
- 每镜默认最多一个主要动作族和一个环境动作族；主条目自身已有粒子、辉光、漂移、动态背景或环境光时，视为已经占用 ambient 名额，不再叠第二个环境条目。环境动作可持续，但必须由帧驱动、可复现、可停止，并在落定帧接受检查。
- ambient 初始值始终是 `null`，不是每镜默认配置。只有能具体写出 `visual_experience_gain`（氛围/期待/触感/节奏/空间深度之一）和 `why_keep` 时才加入。若只剩“画面不空”或“更炫”，保持 `null`。
- 若去掉环境动作后内容仍清楚，并不构成删除理由；判断标准是“是否带来可命名的观看体验增益且不影响主体”。一旦影响阅读、识别、证据或节奏，就降低强度、改位置、暂停或替换。
- QA 分开报告 `semantic_motion_coverage` 与 `experiential_motion_coverage`。ambient 可以增加后者，但不能替代缺失的解释、证据、比较或操作，也不能用来单独凑动态覆盖目标。

推荐分层：`ambient 背景 → 真实/程序化主体 → glass material → fully opaque text/labels → subtitle/QA overlays`。背景是证据时，不把它降成装饰；把文字移到独立安全区。

## 五源组合纪律

- 同一 Scene 默认选 1 个主条目，可再选 1 个 ambient 条目；不要把五个库的效果全部叠在一镜。
- 优先使用不等于强行使用：真实证据可保持主体，但应评估圈注、框架、关系线、局部放大或双语说明等 Remotion/HyperFrames 辅助层；拒绝程序化辅助时记录原因。
- 同一观看任务优先复用一个适配后的基础组件，避免相邻镜头的物理规律互相打架。
- Shotcraft 负责经过说明的镜头语法；RVE 负责小而清楚的原子组件；Scenes 负责广覆盖场景；Curvable 负责高完成度、确定性的复合组件；Playground 只提供液态实验语法。
- 如果候选需要改变文案、延长锁定音频、牺牲字幕或隐藏证据才能成立，换候选，不改内容迁就效果。
- 不直接复制 ThemeAnimations、产品 UI 或上游品牌皮肤。主题类条目只提取布局、层级、材质或动作结构，再回到固定 Soft Signal 色调。
- 一个章节至少明确标出 ambient 的 `off / low / medium` 节奏，不允许所有 Scene 无差别常开同一种漂移；两个高运动负担 Scene 后优先安排 `off` 或静止落定，给内容与视觉同时呼吸。
- 相邻两个程序化 Scene 不得拥有完全相同的 `engine + motion_family + motion_signature`。同一家族连续出现时，至少改变两个可见维度；若选择慢速变体，后一镜动作与 hold 必须为前一镜的 1.25–1.60 倍并记录 `variation_from_previous.mode=slower`。
- 相邻总结/观点/信息页不得重复 `visual_page_id` 或 `content_fingerprint`，也不得连续播放同一 composition、MP4 或页面两次补时长。需要延长时，使用一个 HyperFrames composition 的至少 3 个 `internal_phases` 继续推进字体、要点、进度、箭头、数字或构图；否则建立内容与主版式都不同的新页面。
- 超过 60 秒的章节至少使用 3 个 motion family，较短章节至少 2 个。动画丰富度来自清晰的家族轮换、空间接力和时值变化，不来自把多个效果叠在同一镜。
- 文字动效在逐项浮现、mask reveal、进度推进、路径/箭头绘制、数字变换和同位置替换之间轮换；连续两次使用相同文字动画仍按相邻去重处理。

## `animation-plan.json`

所有 Remotion/HyperFrames 程序化 Scene 在实装前写入 `04_spec/animation-plan.json`：

```json
{
  "catalog_revision": "从 catalog.json 复制",
  "scenes": [
    {
      "scene_id": "S012",
      "engine": "hyperframes",
      "engine_selection": {
        "semantic_accuracy": 5,
        "subject_safety": 5,
        "render_stability": 4.5,
        "visual_impact": 5,
        "near_tie": true,
        "selected_engine": "hyperframes",
        "reason": "两种实现均稳定且语义准确，HyperFrames 的路径与文字建立观感更强，因此按近似优先规则选择"
      },
      "script_excerpt": "当前完整文案",
      "rhetorical_function": "compare",
      "viewer_should_notice": "旧值与新值的数量差",
      "viewer_should_understand": "自动化缩短了处理时间",
      "animation_intent": ["compare", "quantify"],
      "motion_role": "mixed",
      "programmatic_opportunity": "preferred",
      "duration_seconds": 5.0,
      "reading_load": "medium",
      "subject_safe_zones": ["中央数据卡", "底部字幕"],
      "subtitle_exclusion_bottom_px": 220,
      "visual_page_id": "summary-automation-time-01",
      "content_fingerprint": "compare-old-10m-new-30s",
      "duration_fill_strategy": "extend_internal_choreography",
      "repeat_page_to_fill_duration": false,
      "internal_phases": ["标题材质化", "旧值与新值依次落位", "进度线推进", "结论放大并停留"],
      "motion_family": "progress_build",
      "motion_signature": {
        "layout": "vertical_logic",
        "direction": "left_to_right",
        "build_order": "title_then_points_then_path",
        "easing": "spring_gentle",
        "pace_class": "slow"
      },
      "variation_from_previous": {
        "mode": "changed",
        "changed_dimensions": ["layout", "direction"],
        "pace_multiplier": 1.0
      },
      "apple_logic": {
        "purpose": "让观众看清旧值到新值的推进",
        "focal_hierarchy": ["主结论", "两组数据", "推进线"],
        "spatial_origin": "从前一镜的结论词向右延伸",
        "material_response": "主数据使用 regular，来源标签使用 thin",
        "continuity": "推进线接到下一镜路径",
        "settle_state": "完整落定后停留 1.2 秒",
        "delight": "数字落位与进度线同帧回执"
      },
      "hyperframes_recipe": "vertical-progress-logic",
      "candidates": ["rve:comparison-chart", "video-shotcraft:before-after-slider-scrub:before-after-slider-scrub"],
      "primary_selection": {
        "id": "custom",
        "custom_reason": "用 HyperFrames 建立竖向进度逻辑，并从候选中借用同尺度对照语法",
        "motion_grammar": "GSAP 路径先伸展，旧值与新值依次落位，结论材质化并停留",
        "why_now": "同尺度展示旧值与新值，正好对应句内对比",
        "includes_ambient_motion": false,
        "keep": ["双列建立", "数值同步落定", "末帧停留"],
        "reskin": ["颜色", "字体", "卡片", "阴影"],
        "timing": "动作 2.2s，阅读 hold 1.0s"
      },
      "ambient_selection": {
        "id": "rve:gradient-shift",
        "why": "为转折后的轻快感提供温暖层次",
        "visual_experience_gain": "空间深度与轻快期待",
        "why_keep": "渐变在数据建立前提供方向，数据落定时停止，不与数值竞争",
        "subject_protection": {
          "safe_zones": ["中央数据卡", "底部字幕"],
          "max_opacity": 0.14,
          "reading_behavior": "数值开始变化后减速，落定后停止位移",
          "qa_frame": "背景峰值且正文完整显示的帧"
        }
      },
      "compatibility": "当前 Remotion 版本已验证",
      "fallback": "静态双列 + 数字淡入",
      "qa_frames": ["进入中", "运动峰值", "完整落定"]
    }
  ]
}
```

没有合适条目时允许 `primary_selection` 使用 `custom`，但必须写 `custom_reason`、运动语法、确定性方案和 fallback；不能虚构 catalog ID。

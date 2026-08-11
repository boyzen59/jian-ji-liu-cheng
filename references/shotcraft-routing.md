# video-shotcraft 路由

上游仓库：[Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)。本 Skill 已在 `assets/remotion-library/sources/video-shotcraft/` 内置当前快照：104 张配方卡、161 个 style-key、161 条离线 MP4、对应 demos、template、可复用 helpers 和音频资产；统一条目位于 `assets/remotion-library/catalog.json`。数量以 `scripts/build_remotion_library.py` 的实际校验为准，上游更新后必须重建 catalog，不手改数字或 ID。

本文件把锁定原文转成逐镜动作语法，并指导 Shotcraft 深读。它不授予模板配额，也不要求逐卡使用；跨五源选型仍按 `remotion-library-routing.md` 取得候选。

## Shotcraft pass 门禁

在锁定文稿、SRT 时间骨架和场景类型大纲完成后，对每个 `programmatic_opportunity=preferred|support` 的语义段执行一次 Shotcraft pass，再写最终分镜：

1. 原文拆解：记录 `semantic_segment_id`、时间码、原句范围、核心论点、证据、因果/对照/阶段关系、情绪转折和观众阅读负担。
2. 动作翻译：用动词描述画面应完成的认知动作，例如“从总论点展开三条原因”“让年份沿路径建立”“把证据局部放大后归位”。不要先选卡再把文案塞进去。
3. 候选扩散：同时检索 video-shotcraft、RVE、Scenes、Curvable、Playground、HyperFrames 和原生 Remotion。至少保留两个真正不同的候选；无合适候选时记录自定义实现或拒绝原因。
4. 完整检查：阅读候选卡全文、TSX/源码、demo/preview、依赖和时值。只看卡名、截图或短摘要不得放行。
5. 同场比较：按语义准确、层级清楚、主体保护、阅读负担、视觉冲击、实现稳定和前后镜差异评分。选择当前文案下效果最好的实现；Remotion 与 HyperFrames 不设占比，效果接近时可优先 HyperFrames。
6. 分镜固化：只迁移动作语法、空间关系、关键时值和落定方式；替换示例产品、品牌、默认文案和皮肤。不得为适配模板改写事实，不得把一章批量套成同一模板。

每次 pass 写入：

```yaml
shotcraft_pass:
  semantic_segment_id: SEG-000
  source_range: 原文起止
  cognitive_action: 从总论点建立三个因果节点并闭环
  candidate_sources: [video-shotcraft, hyperframes, scenes]
  candidates:
    - id: source:card-or-style
      demo: path-or-url
      semantic_fit: 0-5
      hierarchy_clarity: 0-5
      subject_safety: 0-5
      visual_impact: 0-5
      reading_load: low|medium|high
      decision: selected|rejected|backup
      reason: 采用或淘汰理由
  selected_engine: remotion|hyperframes
  selected_grammar: path_draw|timeline|relationship_map|number_build|spatial_reveal|comparison_morph|material_transition|cards|custom
```

动态说理不等于卡片。根据原文选择路径、时间轴、关系网、节点接力、数字建立、空间揭示、证据推近、对照变形、材料转场或少量卡片；同一段可有 `1/2/3`，也可只有关键节点，取决于原文逻辑。

## 选择顺序

1. 把 Scene 翻译为一个语义动作：宣告、点名证据、比较、连接因果、跨越时间、建立空间、定格、归位、收束。
2. 从统一 catalog 的 `video-shotcraft:*` 条目按用途、能量、时长、限制和所需素材筛选；再回到 `gallery/api/library.json` 和镜头卡 frontmatter 复核。
3. 为每个需要程序化镜头的 Scene 选一个首选和一个备选；不把所有 Scene 都强行配卡，也不按目录顺序机械轮用。
4. 完整读取首选卡片。
5. 按卡片“参考实现”读取准确 demo TSX 全文，并查看条目 `preview_path` 指向的离线动态样片或抽帧。
6. 记录卡名、style-key、demo 路径、保留的动作语法、要替换的外观和已知坑。
7. 用 Soft Signal 与 `apple-glass-style.md` 重新蒙皮后实现；卡片的命门参数和关键时值不降档。

若卡片标为“仅供参考/需自定义”或缺少预览，不得声称已复刻动态样片；可降级为自定义 Remotion 动画并标注验证风险。

## 语义到候选族

下列名称仅作候选，运行时必须重新校验：

| 语义 | 候选动作/卡 | 使用纪律 |
|---|---|---|
| 章节宣告 | `paper-title-card`、`title-demote-to-label` | 大标题落为章节标签，不重复重新出现 |
| 关键词强调 | `marker-underline-title`、`draw-svg-trace` | 一屏只点一个词或证据 |
| 静态资料 2.5D | `depth-layer-moves` | 阅读层保持锐利，视差克制 |
| 流动后定格 | `speed-ramp-freeze` | 定格必须服务圈注/解释 |
| 论点与证据接力 | `word-relay-filmstrip` | 步进而非无尽滚动 |
| 前后对照 | `before-after-slider-scrub` | 必须同机位/同尺度，慢扫证明差异 |
| 唯一主证据 | `spotlight-hero-card` | 全片 1–2 次，只给真正主角 |
| 时间/阶段 | `timeline-travel` | 三项以上才用，停在当前节点 |
| 因果/图形接力 | `line-carry-transition` | 线条必须由上一语义自然产生 |
| 无痕换景 | `transition-hidden-cut / invisible-cut` | 切点必须完全遮挡 |
| 温暖章节切换 | `transition-hidden-cut / light-leak` | 全片最多 1 次为宜 |
| 纸墨过渡 | `print-texture-transitions` | 只有资料/出版语义成立时使用 |
| 资料实体化 | `paper-craft-moves` | 单卡、单动作，不做纸片雨 |
| 情绪压迫/收束 | `tension-camera-moves` | 慢推或后拉只在重要段落一次 |

## 适配规则

- 保留：相机路径、关键帧比例、缓动性格、遮罩摘除时机、落定方式、hold 和已知坑。
- 替换：产品 UI、按钮、仪表盘、默认文案、品牌、颜色、字体、纹理、玻璃材质、阴影和数据。
- 全部外观服从 `fixed-style.md`；真实素材可保留原貌。
- 含文字卡默认用一层 Soft Signal 毛玻璃信息面；背景动作降为 faint/subtle，文字必须在背景最繁忙帧仍清晰。
- 每镜一个主要运动。同一套动画手法全片只当一次主角。
- 招牌镜头后必须有阅读/呼吸，不要连续堆招牌卡。
- 重要标题/字标落定 hold 至少 1 秒；批量动作结束后至少 0.5 秒稳定。
- 相机、光线、节奏和声音共同形成质感；不靠堆特效。

## 复用而不重复

镜头卡代码可以复用，观看体验不能复刻粘贴：

- 同一卡作为主角默认最多 2 次；第二次必须属于不同章节和不同语义任务。
- 至少改变：内容载体、构图、动作阶段三项；另可改变入/出点、尺度、焦点、前后语境和声音。
- 不用改颜色、镜像或变速伪装重复。
- 同一章节不连续使用同卡；相邻两镜不使用同方向、同时值、同落定方式。

## 声音库接入

若本地 video-shotcraft 音频库可用：

- 先按类别找，再逐个试听；记录来源和授权。
- 运镜查 transition，落地查 impact，铺垫查 riser，光效查 light，打字查 text，翻页查 paper，计数查 counter。
- UI 目录含真实开关和合成提示音，不能整目录放行；默认避开 tone/bleep/notification 的游戏/系统反馈质感。
- 新音频入库先按内容哈希去重，并记录时长、峰值、来源 URL 和授权。

## 制作记录

```yaml
scene: S012
semantic_segment_id: SEG-012
source_range: 锁定原文起止
semantic_action: 点名唯一证据
candidate_comparison: [video-shotcraft候选, HyperFrames候选, 其他源候选]
card: spotlight-hero-card-or-custom
style_key: 运行时校验
demo: 运行时校验路径
keep: [聚光, 缓推, 抬起, 归位, hold]
replace: [UI外观, 配色, 字体, 文案]
known_pitfalls: [来自卡片全文]
qa_frames: [运动峰值帧, 落定后帧]
sound_trigger: 主体落定
```

若 Scene 正在播放昂贵 AI/实拍视频，降低额外动态说理密度；若 Scene 展示 `archive_evidence` 或 `book_evidence`，禁止动态说理，仅保留证据支持动作与双语来源解释。

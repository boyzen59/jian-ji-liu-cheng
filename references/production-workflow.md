# 生产流程与放行 Gate

## 事实源与优先级

用户本项目新指令 > 本项目正文/锁定录音/已确认文字审阅 > 本 Skill > Remotion、HyperFrames 或镜头卡默认值。

同一事实只保留一个真本：

- 时间：`timeline.json` / 锁定音频
- 分镜：`video-spec.json`
- 动效选型：`animation-plan.json` + 内置 `catalog.json` revision
- 屏显文字：既有文字基线已放行；仅新增/改字进入 `text-review.json` 增量门禁
- 主题：Soft Signal token + Apple 毛玻璃规范
- 素材：`source-manifest.csv`
- 声音：`sound-plan.json`
- 输出规格：`project.json.spec`，固定 H.264 / Rec.709 / 2560×1440 / 60fps CFR / 无音频流 / 无烧录字幕

不要在多个组件里复制时间和文字常量。

## 阶段与 Gate

| 阶段 | 工作 | 产出 | 放行条件 |
|---|---|---|---|
| 0 定位 | AI 追问、素材审计、风险 | project-brief | READY/低风险假设 |
| 1 时间与类型 | 音频/SRT/正文对齐、先判场景类型、为每章插入全屏大字总览 | transcript-map、timeline、outline-scene-types | 时长连续、每段类型与功能明确、每章有 chapter_title |
| 2 文字 | 双语屏显与压缩 | text-review JSON + Word | 无必须修改/待确认 |
| 3 设计 | 固定 Soft Signal、Apple 毛玻璃、叙事、文案动效意图和节奏 | styleframe、video spec、animation plan | 色调、材质层级、主体保护与可读性通过 |
| 4 素材 | 已有、检索、AI、程序化 | 素材目录与 manifest | 每镜有可行来源 |
| 5 实现 | Remotion + HyperFrames + 五源统一动效资料库、GPU 预检 | 可预览工程、静帧、render-plan | 每镜静帧与运动峰值通过、每段 ≤300 秒 |
| 6 声音 | 六层音轨、AI/YouTube Audio Library 音乐、ducking、cue | sound-plan、stems、审片混音 | 画面已锁、音画同步、人声绝对优先 |
| 7 终检与文档 | 分段渲染、拼接、抽帧、看片、三端试听、六类文档 | QA 报告、静音终渲、独立音频、10_deliverables | 所有阻塞项关闭 |

Gate 通过后才进入下一昂贵阶段。后续发现上游问题，回到对应 Gate 修复并更新版本；不要在下游打隐藏补丁。

## 工具职责

### Remotion

- 唯一总时间线、锁定音频时间骨架、媒体裁切和速度
- 开场人物全屏到小窗的 15 秒内空间转换、正文内容感知小窗、最终总结全屏、双语解释图、地图覆盖、全屏大字章节总览和章节拼装
- 清晰图片/视频全屏舞台的缓推、横移、焦点、视差、人物缩窗、结构接力和 HyperFrames 片段嵌入；Remotion 自身必须产生可见运动，不得只做静态容器或对媒体本体加模糊
- 毛玻璃面板、背景显隐、系统排版、材质建立和降级模式
- 音轨、SFX cue、审片混音、stems 与不带任何音频流的静音终渲
- 动画由帧、interpolate、Easing 或 spring 驱动

不做：运行时 CSS animation、不可复现随机、网络内容、一个巨型组件塞全部场景。

### 统一 Remotion 动效资料库

- 入口：`assets/remotion-library/catalog.json`；来源：video-shotcraft、RVE、Scenes、Curvable、Playground。
- 文案分析、候选检索、评分和主体保护按 `references/remotion-library-routing.md`。
- 每个程序化 Scene 在 `04_spec/animation-plan.json` 记录 catalog revision、候选、首选/备选、出现时机、保留语法、换肤项、fallback 和 QA 帧。
- 主要层负责内容观看任务；辅助/环境层可以提供氛围、趣味、触感和节奏体验，只要不影响主体。
- 只复制选中条目及明确依赖。上游 showcase、主题皮肤、产品文案和整套注册表不进入生产工程。

不做：只凭缩略图选型、虚构 catalog ID、把候选排名当最终批准、在复杂阅读帧让环境动效穿过主体。

### HyperFrames

- 与 Remotion 同级参与动效选型；前三项合格后选择视觉冲击更强者，效果接近时优先 HyperFrames
- 高频承担开场真人左右说明、清晰图片/视频上方的局部文字毛玻璃、全屏章节总览、标题、观点、流程、因果链、清单、对照、图表、数字、进度/逻辑箭头、章节接缝和最终真人左右总结
- 每个程序化 Scene 先做 video-shotcraft 语义 pass，再比较 Remotion、HyperFrames、RVE、Scenes、Curvable 与 Playground；不设引擎占比或每章配额
- 每段必须有确定的总时长、入点、出点和静态落定帧
- 先构建 hero frame，再按 `build → breathe → resolve` 编排；每个可见元素都有入场，使用转场承担前一 Scene 退出
- 时间线 paused 并可由外层控制；视频 muted/playsinline；禁无限循环和异步构建；完成后运行 lint、validate、inspect 并审阅 animation map

不做：管理全片主音频或成为第二条总时间线。

### Lottie / D3 / Blender / Manim

- 按 `advanced-animation-routing.md` 选型；每个片段固定入点、出点、帧率、文字审阅 ID 和回退。
- Lottie 与 D3 运行在 Remotion 帧时钟下；Blender 与 Manim 离线出独立片段，再回到 Remotion 合成。
- 任何扩展引擎不得形成第二条总时间线，也不得绕过 H.264/Rec.709/2K60 主交付与文字门禁。

### video-shotcraft 子库

- 镜头配方、运动语法、关键时值、2.5D 相机和经调参数
- 作为候选库，不是固定外观模板

不做：自动决定题材视觉、复制产品 UI、为了展示卡片而改变内容。

### RVE / Scenes / Curvable / Playground 子库

- RVE：首选轻量单文件组件；复制后统一 props、字号、颜色、spring 和安全区。
- Scenes：从 201 场景中提取一个具体 scene 与所需 `common`，不加载全库 Showcase。
- Curvable：利用确定性组件契约；接入前确认 `ogl`、Google Fonts、CanvasKit 等可选依赖，并用 Soft Signal `primary` 与材质 token 重新蒙皮。
- Playground：仅作 goo/液态运动研究；先从 Remotion 2.1 / React 17 移植到当前 API，移除旧锁文件依赖和不确定性。

## 实装顺序

1. 建立主 Composition、精确总帧数、章节/Scene 注册表；明确连续字幕只外挂，主画面 `burned_in_captions=false`，并在 2560×1440 保留底部 220px 字幕排除区。
2. 先完成场景类型大纲，为每个正文章节建立超大双语标题铺满主视觉区的 `chapter_title`，再转换为 video spec；接入锁定人声时间骨架和已放行解释文字，不做声音设计。
3. 先做每章关键 styleframe、背景最繁忙帧和最复杂信息帧，检查玻璃层级与文字对比度。
4. 对每个 Scene 先判 `programmatic_opportunity`；章节开头、因果、流程、制度关系、结构关系和文字说理固定为 `preferred`。对每个程序化 Scene 让 Remotion/HyperFrames 同级比较语义准确、主体安全、渲染稳定和视觉冲击，写 `engine_selection`、`engine`、`motion_family`、`motion_signature`、`variation_from_previous`、`apple_logic` 和 `animation-plan.json`；效果接近时选 HyperFrames。
5. 逐镜实现：读取选中源文件、demo/预览和依赖，适配 Soft Signal，保留语义与视觉体验价值。
6. 每镜记录至少三个 QA 帧：背景/环境最繁忙、主要运动峰值、文字或证据完整落定；有玻璃时另查材质建立帧。额外制作七类 styleframe：开场真人说明、普通/AI图片清晰全屏＋局部文字毛玻璃、档案/图书证据双语来源区＋大幅清晰证据图、清晰视频全屏＋局部文字毛玻璃、双栏补位、正文右下小窗＋图解、最终真人全屏总结。
7. 每轮修改后先用 `scripts/build_render_plan.py` 探测硬件并生成自适应并发、显式缓存预算和 ≤300 秒段落，再为当前段启动 `scripts/watch_render_progress.py`；每段检查接缝、双语解释文字、左右择位且抬高的圆窗、字幕排除区、时间漂移和资源采样，最后拼接后整片抽查。
8. 时间线锁定后生成/更新 sound-plan；按文案生成 AI 轻音乐需求或筛选 YouTube Studio Audio Library 合规曲目，再铺 BGM、环境和 SFX。
9. 输出审片混音和各层 stems，检查峰值、响度、音画同步和三端听感；静音视频母版不写入任何音轨。

## 固定终渲与媒体验收

Remotion 主合成使用 `width=2560`、`height=1440`、`fps=60`，输出 MP4 时显式使用 `--codec=h264 --muted`；不要使用 `--enforce-audio-track`，也不要依赖扩展名暗示或使用 `h265` / `hevc`。先按锁定音频每 300 秒以内并吸附 Scene 边界分段渲染，再拼接。若需统一素材、色彩标签或 CFR，使用 FFmpeg 做一次最终规范化：

```powershell
ffmpeg -i master_input.mp4 -map 0:v:0 -an -vf "scale=2560:1440:flags=lanczos:force_original_aspect_ratio=decrease,pad=2560:1440:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709" -r 60 -fps_mode cfr -c:v libx264 -profile:v high -level:v 5.1 -preset slow -crf 17 -pix_fmt yuv420p -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart master_h264_rec709_2k60_silent.mp4
```

`setparams` 与输出 metadata 只能声明标签，不能把错误的源色彩真正变成 Rec.709。先用 `ffprobe` 检查每个来源；只有来源本来就是 Rec.709 或已按其真实输入 primaries/transfer/matrix 完成色彩转换后，才进入上述最终规范化。HDR、Display-P3、BT.2020 或标签缺失素材不得靠强贴 `bt709` 过关，必须先做有依据的 tone-map/色彩转换并抽帧复核。

终渲后执行：

```powershell
python scripts/verify_master_media.py master_h264_rec709_2k60.mp4 --ffprobe "C:\path\to\ffprobe.exe"
```

脚本严格验收 MP4、H.264 High、2560×1440、yuv420p、60fps CFR、limited range、三项 bt709 标签以及“没有任何音频流”。它只验证编码与标签；实际色彩、黑边、拉伸、双语图解、圆窗和画面内容仍需抽帧观看。

## GPU 与分段

- 先读取当前 Remotion 版本的官方渲染文档。Remotion 5 通常让 `angle` 自动选 GPU/软件回退；Remotion 4 的桌面 WebGL/Three 内容先试 `--gl=angle`。WebGL、Three、Skia、Canvas、blur、shadow、transform 和视频解码是 GPU 优先候选。
- H.264 硬件编码使用 `--hardware-acceleration if-possible`；Windows/Linux 只有在兼容 NVIDIA GPU、驱动和含 `h264_nvenc` 的 FFmpeg 下才会使用 NVENC。硬件编码使用 `--video-bitrate`，不能和 CRF 同用；硬件不可用时自动回退软件 H.264。
- 先对 10–30 秒代表段 A/B 测试 GPU 与 CPU；玻璃、色彩、透明、帧一致性或稳定性异常时回退。
- 运行 `scripts/build_render_plan.py <project_root>`；脚本探测逻辑线程、物理内存与 NVIDIA GPU，初始并发约为逻辑线程 75%，候选约 50% / 75% / 90%。每个渲染段不得超过 300 秒，尽量在 Scene/章节边界切分。GPU 的 `angle` 存在长片内存泄漏风险，因此不要一次渲染整部长片。
- 显式限制两个 Remotion 媒体缓存并设置 OffthreadVideo 线程，避免默认缓存把 RAM 推到 80% 以上。默认保持并行编码；只有代表段证实内存故障时才降低并发或使用更保守恢复路径。
- 每段同步运行 `scripts/watch_render_progress.py`。监控每 15 秒采样 CPU/GPU/RAM/VRAM、帧号、日志和输出增长；无论有没有进度，每 300 秒向用户固定汇报。连续 180 秒无变化时自动写停滞诊断，300 秒无变化时立即报告硬停滞；每段完成或失败立即报告。
- 调参只发生在分段之间：CPU 低于 75%、GPU 适用场景低于 65% 且 RAM 低于 70% 时提高下一段并发；RAM 达到 78%、VRAM 达到 85%、CPU 长期高于 95%却无吞吐提升或出现解码错误时降低。RAM 85% 与 VRAM 92% 是硬上限。目标是单位时间有效帧数，不是让资源读数无条件满载。

## 视觉节奏

- 用户核对的素材按清单顺序和指定语义段原样使用，不重新匹配、交换或跨段借用。图片展示 5–10 秒；视频源长不少于 5 秒时完整自然播放，源长不足 5 秒时播放一次后保持末帧到 5 秒，超过 10 秒不得裁切。
- 普通/AI图片和视频保持清晰原画全屏、`blur=0`；非16:9图片使用实色衬底。只有上方文字使用局部毛玻璃。`archive_evidence`与`book_evidence`采用简中＋英文来源区＋大幅清晰证据图，在屏时禁止动态说理。
- `argument_bridge` 仅在缺少合适媒体或具体动态图解时使用：左双语大论点、右 2–4 个双语动态细分论点；目标占比 4%–6%、硬上限 6%，每章最多一场且不得连续。
- 开场真人全屏最多 15 秒并由 HyperFrames 在左右解释；之后到最终总结前只用抬高小窗或撤下；最终总结再次全屏时必须有 HyperFrames 双侧总结、进度或逻辑箭头。
- 相邻程序化 Scene 的 `engine + motion_family + motion_signature` 不得完全相同。同一家族连续时至少改变两个可见维度，或让后一镜动作与 hold 放慢到 1.25–1.60 倍。超过 60 秒的章节至少 3 个 motion family，较短章节至少 2 个。
- 相邻总结/观点/程序化信息页的 `visual_page_id` 或 `content_fingerprint` 不得重复；同一 composition/MP4/Scene 不得连续播放两遍补时长。需要延长时在一个 HyperFrames composition 内使用至少 3 个新的字体、要点、进度、箭头、数字或构图阶段，否则换到内容和版式都不同的新页。
- 文字不连续使用同一种淡入；逐项浮现、mask、进度、路径/箭头、数字变化和同位置替换按语义轮换。右侧信息面使用竖排结构，正文/卡片 42–54px，辅助文字至少 32px。
- 普通内容切换优先短叠化、焦点接力、推移、遮挡藏切、形状接力或同位置内容替换；裸硬切只保留给刻意语义撞击并写理由。
- 每个章节先用全屏超大双语标题总览，再用明确章节动态转场进入正文；章节接缝不能裸硬切。
- 反白/强转场不能成为日常标点；同一接缝不叠两个转场。
- 毛玻璃是局部文字信息层，不是媒体滤镜；图片、视频和历史证据图本体始终清晰且 `blur=0`。同屏最多两个半透明文字平面，必须遵守主体安全区和阅读期减速/停稳规则。
- 长片按不超过 5 分钟的时间窗口拆为可独立渲染段，优先吸附章节/Scene 边界，统一主题和总时间线，不因工程拆分改变观众体验。
- 超过 30 分钟的长片每 5–8 分钟至少一个注意力重置点，类型必须是新问题、新案例、新视觉形式或新观点，并在 spec 中写 `attention_reset`。

## 画面锁定与声音锁定

精钉 SFX 的前置条件是：镜头顺序、时长、主要动作帧和字幕入出已稳定。画面在声音后改变时，自动使所有受影响 cue 标记为 `STALE`，重新计算相对帧并复听。

## 版本与返工

- 项目简报、文字审阅、video spec、sound plan 和成片各自有版本号与生成时间。
- 文案改动回文字 Gate；内容/结构改动回分镜；视觉实现问题回镜头；声音问题回混音。
- 删除素材时保留编号并标为取消，不重排后续编号。
- 每个版本保存变更摘要，不把“应该通过”写进 QA 证据。

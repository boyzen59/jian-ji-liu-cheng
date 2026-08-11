# 素材锁定、原画保护与增量审阅

## 用户核对清单是唯一素材路由

- 用户已核对的文案顺序、文件内清单和素材对应关系拥有最高优先级。按 `manifest_order` 顺序使用 `assigned_asset_path`，并与 `assigned_script_segment_id` 一一对应；不得重新判断语义匹配、交换镜头、跨段借图或用搜索结果替换。
- 每条已锁素材写 `user_verified=true`、`assignment_locked=true`、`assignment_reassessed=false`。发现文件缺失、损坏或时长不可读时只报告阻塞，不自行重配。
- 新检索或新生成素材只有在用户明确补充并核对后才进入锁定清单。`semantic_match` 与 `visual_review_status` 只服务尚未核对的候选，不得覆盖用户已锁映射。
- 所有含文字画面写 `semantic_segment_id`、`source_text_ids`、`text_provenance`、`new_claims_added=false`、`cross_chapter_merge=false`。标题、要点、箭头和总结必须来自同一语义段；不得新增观点或跨章节拼接。

## Remotion / HyperFrames 同级选型

- 两个引擎同级进入程序化动效候选。依次比较语义准确、主体安全、渲染稳定、视觉冲击；前三项合格后再选择观感更炫酷的方案，效果接近时优先 HyperFrames。
- Remotion 仍负责唯一总时间线，但该工程职责不构成动效选型优先级。每个程序化 Scene 写 `engine_selection` 四项评分、近似判断、选中理由和回退。
- 不设 Remotion/HyperFrames 使用占比、每章配额或上限；逐镜记录候选比较，选择当前原文下语义更准、层级更清楚、主体更安全且观感更好的实现。
- 章节开头以及因果、流程、制度关系、结构关系和文字说理段必须使用程序化动态效果，不得用普通 B-roll 或静态图片代替解释。

## 证据类资料分屏

- 以 manifest 的 `material_class` 为准；`archive_evidence` 和 `book_evidence` 使用 `historical_evidence_split_title_source_plus_large_image`，不依赖项目专属文件夹名。
- 分屏由简体中文＋英文标题/来源说明区和大幅清晰证据图组成。证据图不得磨砂或整图模糊；翻译忠实于文件内容，不补造来源。
- 证据类资料在屏时禁止动态说理，只允许慢推、证据局部推近、聚光、圈注、来源翻译和阅读停留。

## 普通图片

- `ordinary_image` 与 `ai_image` 以清晰原图全屏呈现。16:9 可铺满；非 16:9 使用 `contain` 加纯色/暖白实色衬底，不使用模糊延展。
- 图片本体固定 `media_body_blur_px=0`、`original_media_clear=true`；按语义选择缓推、横/纵移、焦点接力、2.5D 视差、遮罩揭示、局部推近或前后对照。单张展示 5–10 秒。
- 标题、要点和说明文字使用局部 Soft Signal 毛玻璃框；玻璃只包裹文字，不覆盖整图。文字载体引擎由逐镜比较决定，不固定为 HyperFrames。

## 视频

- 视频保持清晰原画全屏、静音、只播放一次；本体固定 `media_body_blur_px=0`，禁止整屏毛玻璃、模糊、循环或重复拼接。
- 源时长不少于 5 秒时，`timeline_duration_seconds=source_duration_seconds`，完整沿用自然时长；超过 10 秒也不得裁切。
- 源时长不足 5 秒时，先完整播放一次，再保持末帧至总长 5 秒；不得减速、循环或重播。
- 只有视频上方的标题、要点和说明文字可用 HyperFrames 局部毛玻璃特效；无文字时不强加玻璃层。

## 低频双栏补位画面

- 仅在缺少合适图片、视频或具体动态图解时，允许 `argument_bridge`：左侧为当前语义段总结出的双语大论点，右侧由 HyperFrames 动态建立 2–4 个双语细分论点、节点、路径或箭头。
- 左侧中英主论点至少 88px，右侧中英细分论点至少 48px；该画面必须绑定当前单一语义段及其文字来源 ID，禁止跨章拼接或补写新观点。
- 中英文都使用醒目大字号，并保留底部字幕区。不得新增观点；左右全部引用同一 `semantic_segment_id`。
- 目标占全片 4%–6%，硬上限 6%；不需要时不为凑下限强行使用。每章最多一场，不得相邻出现。每场必须记录具体 `insufficiency_reason`。

## 文字增量审阅

- 当前已有文字动效审阅视为全部通过，项目使用 `review_mode=delta_only` 与 `baseline_existing_text_approved=true`。
- 未新增、未改字的既有屏显直接继承批准，不重复生成审阅任务。只有 `change_kind=new|changed` 的行进入 Word 门禁；这些增量行全部批准后才放行。
- 版式、位置、字号、材质或不改字的运动调整属于 `layout_only`，不重新触发文字审阅。

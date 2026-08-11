# 自动声音与混音

声音是时间线级系统。画面结构锁定后，依据 video spec 自动生成 cue，再人工在成片语境中试听和调整。不能凭关键词把音效散落进组件。

## 六层音轨

1. **VOICE**：中心、清楚、稳定，是绝对优先级。
2. **BGM**：建立情绪、章节和能量曲线，不抢字头；口播区自动 ducking。
3. **AMBIENCE**：建立空间，可很轻；同一空间保持连续，不随每个剪切重启。
4. **TRANSITION**：只强化重要切换，普通语义硬切默认无音效。
5. **FOLEY**：点击、翻页、卡片落位、数字跳动、书写等，与可见动作逐帧同步。
6. **EMOTION**：riser、impact、swell 服务高潮、转折和收束，不作为日常背景。

输出独立 stems：`voice.wav`、`bgm.wav`、`ambience.wav`、`sfx.wav`、`review_mix.wav`。最终视频母版不含任何音频流；`review_mix.wav` 只用于审片和用户后续合成。

## 自动 cue 生成

`scripts/build_sound_plan.py` 读取 video-spec JSON。每个 Scene 至少包含：id、start/end、carrier、transition_in、motion、emotion、space、importance。

触发逻辑：

- Scene 首次进入新空间且 `space` 非空：建立 AMBIENCE bed，延续到空间变化。
- `transition_in` 为 hard cut：默认不加转场音；重要度 3 且语义大转折时才可短 impact。
- crossfade/push/hidden cut/chapter 且重要度 ≥2：给一个匹配时长的 transition/whoosh 候选。
- 每个 `chapter_title` 必须给一条独立强化声音候选：克制 riser、impact、page settle 或短音乐重音；同一章节只设一个主声音落点，不叠加成噪声。
- motion 含 click/switch：FOLEY click；page/flip：paper；card/land/stamp：settle/impact；number/counter：tick；draw/write：pencil/marker。
- emotion 为 rise：在落点前 0.8–2.5 秒布 riser；climax：落点 impact；resolution：轻 swell 或余韵，三者不必全用。
- 连发动作生成序列 cue，但密到无法逐个分辨时从逐个拟音过渡为单条 swoosh。

自动结果是建议表，不是“已经有声音”。每条 cue 必须绑定实际音源、来源授权和试听状态后才可标为 READY。

## 人声处理

- 单声道人声置中；双声道口播先检查相位，避免伪立体声漂移。
- 先做剪辑和补房间底噪，再按需要轻量去噪、去爆音、EQ、压缩、齿音控制和限幅。
- 不为追求“大声”先压爆；保留自然呼吸、字头和句尾。
- 同一讲者跨段匹配响度、音色和底噪；补录段不得忽明忽暗。
- 所有效果以可懂度为准；过度去噪的水下感、过度压缩的抽吸感都要回退。

## BGM 与 ducking

先按章节情绪曲线选音乐，再垫进成片试听。单听“好听”不等于适合口播。

音乐来源优先级：

1. 按整篇文案和各章情绪曲线生成原创 AI 轻音乐；记录生成平台、模型/版本、完整提示词、生成日期、文件哈希和使用权声明。
2. 从 YouTube Studio Audio Library 搜索气质、流派、情绪、时长和署名条件相符的音乐。记录曲名、作者、Audio Library 页面、许可证类型、是否要求署名、署名原文、下载日期和允许用途。
3. 不从普通 YouTube “免费音乐”频道抓取或转录。YouTube 官方只确认 Audio Library 内资源为其已知的 copyright-safe 来源；第三方频道标题里的 free/no copyright 不等于可用授权。

每章建立 `music_brief`：`narrative_role｜mood｜energy｜tempo｜mode｜instrumentation｜density｜start/end｜voice_risk｜loop_strategy｜source_type｜license_status`。AI/资料音乐授权无法确认时保持 `PENDING`，不得进入 READY。

自动 ducking 建议起点：

- 从最终人声音轨检测语音活动，而不是用字幕粗略代替。
- 在词头前约 80–150ms 开始降低 BGM，避免第一个辅音被盖。
- attack 约 50–100ms；release 约 250–500ms，句间短停不反复抽吸。
- 普通口播下降约 6–10dB；密集或轻声段可到 10–12dB；最终以听感调整。
- 环境音在人声下通常再降 2–4dB；重要拟音若撞字头，优先挪时或缩短，而不是硬抬音量。
- BGM 切换放在章节、情绪反转或呼吸位；长片避免同一短循环反复暴露。

若用户已选强鼓点音乐，先测真实 BPM 和相位，把关键切点写成拍号；大 slam 全片只给少数结构峰值。渲后从成片音轨回测切点，偏差大于约 3 帧必须修正。

## 环境音

- 只回答“观众现在在哪”，不抢叙述：室内气流、街道远声、档案室纸张、机房低频等。
- 同一空间跨 B-roll 保持连续；空间改变时做短交接，不每镜淡入淡出。
- AI/素材视频默认静音；只有现场声是证据且授权清楚时才保留。
- 环境音没有明确空间意义时宁可不用。

## 转场音

- 普通硬切无音效。
- 章节、重大观点转折、空间跃迁和招牌运镜才使用 transition/whoosh。
- 音效长度跟随可见运动；不能运动结束后还拖着响。
- 不同卡片不要都配同一 whoosh；同类动作保持同类材质，形成有限词汇表。

## 拟音

- 必须有可见动作：点击、翻页、卡片落定、数字跳动、画线、锁定。
- 使用相对表达：`SHOTS.S001.from + offset` 或 `beatF(n)`；禁裸帧号散落。
- 长样本用时间线截断到动作长度；带自然混响尾的 impact 保留合理衰减。
- 连发防机枪感：两个不同近似样本交替、音量阶梯递减、间隔跟随动画加速；不要只靠变调。
- 素材过轻时优先换录制良好的同类音，或预归一化；抬增益会同时抬底噪，必须以渲染产物验峰。

## 情绪音

- riser：进入高能段前建立预期。
- impact：核心词、主证据或结论落定的一拍。
- swell：转折后托住情绪或收尾余韵。
- 可复用三拍句式：`riser → impact → sparkle/swell`，只用于真正的高潮/收束。
- 情绪音和强鼓点 BGM 重叠时做减法；不让每章都用同一套峰值句式。

## 中央 cue 表

```json
{
  "scene_id": "S012",
  "timecode": "00:03:12.400",
  "relative_to": "SHOTS.S012.from + 18",
  "bus": "FOLEY",
  "trigger": "card_land",
  "action": "主证据卡落定",
  "source": "assets/audio/sfx/card-settle.wav",
  "duration_frames": 24,
  "gain_db": -8,
  "duck_under_voice_db": 3,
  "license": "source-manifest:SFX-021",
  "status": "READY"
}
```

画面时间线变化后，把受影响 cue 标为 `STALE` 并重新生成相对时间；不得只平移一部分。

## 响度与峰值

平台规范优先；未指定平台时仅用下列作为知识类网络视频的起始范围，而不是硬性万能值：

- 48kHz 音频；制作/分轨阶段保留约 6dB 峰值余量。
- 最终综合响度可从约 -16 至 -14 LUFS-I 试听起步。
- 最终 true peak 通常不高于 -1dBTP；平台有更严格要求时服从平台。
- 不靠主限幅器救失控的 BGM 或 SFX；先修各层平衡。

需要用响度扫描和 true-peak 测量验证，但数字不能替代听感。

## 三端试听

1. 耳机：齿音、底噪、空间、左右平衡、SFX 错帧。
2. 手机扬声器：人声是否仍清楚，BGM 是否盖字，低频是否消失后只剩刺耳中高频。
3. 普通电脑扬声器：章节切换、整体能量和长时间观看疲劳。

三端任一端需要费力听懂人声即失败。记录设备、版本、时间和问题，修复后复听。

三端通过的是审片混音，不改变主交付静音规则。最终再用 ffprobe 确认视频没有音频流；声音 stems 与外挂字幕单独交付。

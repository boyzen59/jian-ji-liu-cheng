# 固定视觉系统：Soft Signal / 亲密 · 温暖

这是母版硬约束。新项目不再选择主题或强调色。真实资料和原始视频保留自身色彩，只把包装、信息图、双语解释文字和程序化段统一到本系统。最终视频不烧录连续字幕；外挂字幕若需样式参考仍沿用固定橙色。默认设计语言升级为温暖、亲密的 Apple 式空间层级：保留全部 Soft Signal 色调，用毛玻璃、清晰排版、克制深度和物理运动完成苹果化。详细规则见 `apple-glass-style.md`。

## 精确 Design Tokens

```ts
export const softSignal = {
  name: 'Soft Signal',
  designLanguage: 'Apple-inspired warmth',
  materialLanguage: 'frosted-glass',
  colors: {
    background: '#FFF8F0',
    surface: '#FFFFFF',
    elevated: '#FFF5EA',
    foreground: '#3D3028',
    foregroundSecondary: 'rgba(61,48,40,0.66)',
    foregroundMuted: 'rgba(61,48,40,0.42)',
    foregroundFaint: 'rgba(61,48,40,0.18)',
    accent: '#E8734A',
    accent2: 'rgba(232,115,74,0.40)',
    accent3: 'rgba(232,115,74,0.14)',
    line: 'rgba(61,48,40,0.08)',
    lineStrong: 'rgba(61,48,40,0.16)',
    lineStrongest: 'rgba(61,48,40,0.28)',
    flash: '#3D3028',
    green: '#6BAA6B',
    red: '#CC6B6B',
    yellow: '#C4A646',
  },
  typography: {
    displayFont: '"SF Pro Display", -apple-system, BlinkMacSystemFont, "Helvetica Neue", "PingFang SC", sans-serif',
    sansFont: '"SF Pro Text", -apple-system, BlinkMacSystemFont, "Helvetica Neue", "PingFang SC", sans-serif',
    monoFont: '"SFMono-Regular", "SF Mono", "IBM Plex Mono", "Menlo", monospace',
    chineseFont: '"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif',
    serifFont: '"Lora", "Georgia", serif',
    scale: {chapterDisplayMin: 156, chapterDisplayMax: 220, display: 128, conclusion: 112, h1: 96, h2: 72, h3: 56, body: 46, small: 34, cap: 30, meta: 26},
    minimum: {body: 42, support: 32, sourceMeta: 26},
    weight: {regular: 400, mid: 600, bold: 700, heavy: 800},
    letterSpacing: {display: '-0.025em', h1: '-0.018em', h2: '-0.01em', body: '0', small: '0.01em', caps: '0.08em', meta: '0.12em'},
    lineHeight: {display: 1.02, heading: 1.1, tight: 1.25, body: 1.55},
    opticalSizing: 'auto',
  },
  spacing: {s1: 8, s2: 16, s3: 24, s4: 40, s5: 56, s6: 80},
  borderRadius: {none: 0, sm: 10, md: 18, lg: 28, xl: 40},
  materials: {
    glassThin: {
      background: 'rgba(255,255,255,0.56)', blur: 18, saturate: 1.25,
      border: 'rgba(255,255,255,0.64)', shadow: '0 8px 24px rgba(61,48,40,0.08)',
    },
    glassRegular: {
      background: 'rgba(255,248,240,0.70)', blur: 26, saturate: 1.35,
      border: 'rgba(255,255,255,0.72)', shadow: '0 16px 48px rgba(61,48,40,0.12)',
    },
    glassThick: {
      background: 'rgba(255,248,240,0.84)', blur: 36, saturate: 1.20,
      border: 'rgba(255,255,255,0.82)', shadow: '0 24px 64px rgba(61,48,40,0.16)',
    },
    backgroundPatternOpacity: {min: 0.08, default: 0.14, max: 0.24},
    textScrim: 'rgba(255,248,240,0.88)',
  },
  accessibility: {contrastBody: 4.5, contrastLarge: 3, reducedMotion: true, reducedTransparency: true, highContrast: true},
  motion: {
    easeOut: 'cubic-bezier(0.22, 1, 0.36, 1)',
    easeIn: 'cubic-bezier(0.55, 0, 1, 0.45)',
    easeSoft: 'cubic-bezier(0.4, 0, 0.2, 1)',
    durationFast: 250,
    durationNormal: 500,
    durationSlow: 1000,
    durationHero: 1200,
    springGentle: {mass: 1, stiffness: 130, damping: 23},
    springStandard: {mass: 1, stiffness: 170, damping: 26},
    springSnappy: {mass: 1, stiffness: 220, damping: 30},
    springMomentum: {mass: 1, stiffness: 170, damping: 21},
  },
  decoration: {
    density: 'restrained-experiential',
    cornerCross: false,
    tickRow: false,
    hairline: false,
    backgroundTexture: 'subtle-through-glass',
  },
  subtitleSafe: {bottomExclusion: 220, minHeightRatio: 0.15, horizontalInset: 120},
  presenterPip: {shape: 'circle', diameter: 360, minDiameter: 340, maxDiameter: 380, borderWidth: 2, defaultAnchor: 'lower-right-raised', alternateRequiresApproval: true},
} as const;
```

## 视觉语法

- 亲密来自暖白空间、近距离证据、柔和速度和克制停顿；Apple 感来自清晰层级、轻盈材质和物理落定，不来自复制系统 UI。
- 画面保持一个主窗口、最多两个辅助层；拒绝等权宫格和卡片海。
- 简洁不等于空。真人全屏、图片全屏和总结帧必须有第二焦点与可读路径；最重要对象先响应，其他内容从它或前一镜的可见锚点建立。
- 真实资料先建立完整身份，再推近局部证据；不得把 AI 情境图包装成真实史料。
- 普通/AI 图片和视频保持清晰原画全屏，媒体本体固定 `blur=0`；非 16:9 图片使用实色衬底，不做模糊延展。只有上方文字使用局部毛玻璃。`archive_evidence` 与 `book_evidence` 使用简中＋英文标题/来源区＋大幅清晰证据图，并禁止证据在屏时叠加动态说理。
- 标题、正文和字幕默认使用系统无衬线字族；Lora/Georgia 只保留给短引文和编辑性章节字样。
- 含文字的程序化镜头默认使用一层局部毛玻璃信息面；文字完全不透明。毛玻璃不得扩展成媒体本体滤镜，图片、视频和证据图始终清晰。
- 动作遵循“建立—阅读—收束”。关键内容落定后保留 0.5–1 秒稳定帧。
- 一镜只有一个主要运动；推、拉、移、圈注、逐项建立、数字变化和转场不同时抢主角。
- 相邻动画解说不得使用完全相同的动效签名；沿用同一动效家族时改变至少两个可见维度，或把后一镜动作与 hold 放慢到前一镜的 1.25–1.60 倍。

## 固定橙色解释文字与外挂字幕参考

最终视频不实装逐句连续字幕。需要橙色强调的双语解释文字、或用户后续制作外挂字幕时，沿用强调橙，不另选主题色：

- 英文主解释文字/外挂字幕参考：`#E8734A`，推荐 54–72px，600–700 weight。
- 中文标注：`rgba(232,115,74,0.82)`，推荐 32–40px，500–600 weight。
- 单语外挂字幕参考：`#E8734A`，按主字幕规格。
- 浅色画面：放在 `glassRegular` 上；若底图细节密集，升级到 `glassThick`，不允许降低文字 opacity。
- 深色或复杂实拍：使用 `glassThick` 和 16–24px 内边距；不要用高强度黑色粗描边破坏温暖感。
- 字幕排除区：2560×1440 底部固定 `220px`，其他尺寸至少保留画面高度 `15%`；不得放入卡片、进度条、逻辑箭头、脸、手势、资料原文、图表结论或小窗。
- 直径约 360px 的圆形人物小窗默认固定右下并整体抬到字幕排除区之上；只有主体碰撞且用户批准时换位。双语解释文字、主证据和小窗不能争夺同一区域。

双语布局：

- 空间足：上下排列，英文在上、中文在下，字号约 2:1。
- 空间不足：横向排列，英语和中文约 1:1；控制总宽并保持自然语组。
- 一次只显示一个主要解释文字组；按语义组建立，不逐字模拟字幕跳动。
- 只对极少量数字、专名或结论词加粗；橙色已是强调，不再叠第二套彩色高亮。
- 右侧承载说明时使用竖向层级：标题 → 逐项要点 → 进度/箭头 → 来源；不把文字横向压成小号表格。
- 总结文字轮换使用逐项浮现、mask reveal、进度推进、路径/箭头绘制、数字变化或同位置替换；禁止全片只有统一 opacity 淡入。

## 程序化段落适配

- Remotion 和 HyperFrames 共用同一 token 文件或序列化 JSON；禁止各自维护近似色。
- 统一 Remotion 资料库条目只继承当前文案需要的运动、时值和组件结构；上游表面、线、文字、阴影、字幕、主题色和材质必须替换为本 token 与 `apple-glass-style.md`。真实证据素材保持原貌。
- 真实视频不强制套暖色滤镜；需要统一时只做轻微曝光、白平衡、对比与肤色匹配。

## 禁用项

- 默认蓝、默认 Roboto、霓虹渐变、冷色玻璃、HUD、无意义故障和循环漂浮
- 多层浅玻璃相叠、整屏磨砂、玻璃卡片海、只为装饰而存在的毛玻璃
- 玻璃后的背景完全消失，或清晰到与正文抢读；半透明文字和低对比小字
- 每张卡都扫光、每个切点都 whoosh、所有元素同方向同缓动
- 将橙色同时用于背景、正文、线条和字幕，造成没有层级
- 为了“温暖”伪造旧纸、胶片、档案磨损或历史证据

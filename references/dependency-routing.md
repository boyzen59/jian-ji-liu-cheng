# 支持库、Skill、插件与运行时路由

先区分四类依赖，不要把它们混称为“插件”：

1. **Codex Skill/插件能力**：负责工作方法、文档、动画或资料搜集。
2. **项目级 JavaScript 包**：只安装到当前视频工程，不写入本 Skill，也不全局安装。
3. **外部桌面/命令行运行时**：Blender、Manim、LaTeX、FFmpeg 等；命中具体镜头时才预检。
4. **内置离线资料**：五源 Remotion catalog，不需要联网安装。

## 能力基线

| 能力 | 调用对象 | 用途 | 缺失时 |
|---|---|---|---|
| 总时间线与终渲 | Remotion 系列 Skill/插件 | Composition、外挂字幕时间骨架、媒体动态、抬高圆形小窗、片段嵌入、H.264 静音终渲 | 停止实现，保留 video spec |
| 同级高频程序化动效段 | HyperFrames 系列 Skill/插件 | 与 Remotion 同级选型；HTML/CSS/GSAP 开场双侧说明、清晰媒体上方局部文字毛玻璃、章节信息、进度/箭头和结尾总结；效果接近时优先 HyperFrames | 标记 `runtime_missing` 并阻塞实现 Gate，不静默退化为静态 PPT |
| Word 文档 | Documents Skill | 六类交付文档的 DOCX 构建与渲染验收 | 先交 UTF-8 文本/JSON，不伪造 Word |
| 实际 AI 图片 | ImageGen Skill | 仅在用户要求真正生图时调用 | 仍可生成双语需求单 |
| 设计系统 | Apple Design Skill | Soft Signal 毛玻璃、目的/层级/空间锚点、物理连续、大字号与无障碍 | 使用本 Skill 固定 token 与 `visual-choreography.md` |
| 商业素材库检索/下载 | `shi-ping-zi-liao-cai-ji` Skill | Pexels、Pixabay、Coverr、Unsplash、Freesound 的文字关键词检索、下载、去重 | 输出检索清单，等待安装/密钥 |
| 数学/科技动画 | `manim-video` Skill | 公式、几何、算法、状态机、科学可视化 | 改用 Remotion + SVG/D3 解释 |

新安装 Skill 通常要重启 Codex，才会进入新任务的自动发现列表。当前任务若尚未发现，仍可先完成路由和数据规范，不宣称已运行该 Skill。

## 资料研究与下载边界

`shi-ping-zi-liao-cai-ji` 默认只按文字关键词搜索和下载，不观看、不理解候选图片；它的支持范围不是维基百科、Wikimedia Commons、博物馆或通用公开数据库。

因此《图片资料搜集需求单》分两层：

- **研究层**：使用联网检索查找 Wikimedia Commons、官方数据库、图书馆、档案馆、博物馆和大学数字馆藏；记录标题、藏品号、机构、页面 URL、原文件 URL、作者/年代、授权、署名、访问日期和画面用途。
- **采集层**：对 Pexels/Pixabay/Coverr/Unsplash/Freesound 调用资料采集 Skill；对开放档案按已核验的原文件 URL 下载。下载不等于审片，必须另做可读性、史实和授权复核。

不得要求文字检索 Skill“识别这张图里是什么”。需要判断画面时，由当前模型查看候选缩略图或原图。

音乐检索只把 YouTube Studio Audio Library 当作 YouTube 官方免费音乐来源。普通 YouTube 频道标题中的 free/no copyright 不等于授权；必须记录 Audio Library 曲目、作者、许可证类型、署名要求和下载日期。AI 音乐另记录平台、模型、提示词、生成日期、哈希和使用权。

## 项目级包

只在命中对应镜头后，在项目工程局部安装：

```text
Lottie: @remotion/lottie + lottie-web
D3: d3（或按需 d3-scale、d3-array、d3-shape、d3-geo）
Remotion 3D 合成: three + @react-three/fiber + @remotion/three
```

Remotion 官方 Lottie 文档要求同时安装 `@remotion/lottie` 和 `lottie-web`：<https://www.remotion.dev/docs/lottie>。D3 官方入口：<https://d3js.org/getting-started>。

不要把 `node_modules`、包缓存或整个上游 showcase 放进本 Skill。安装前读取当前 Remotion 项目的确切版本，所有 `remotion` 与 `@remotion/*` 包保持同版本。

## 外部运行时预检

命中具体镜头后，依次检查：

- `ffmpeg` / `ffprobe`：音频切片、合成、探测和最终交付需要。
- `blender --version`：仅复杂真实材质、灯光、镜头或产品级 3D 需要。
- `manim --version`、Python 3.10+、FFmpeg；含公式时再查 LaTeX/MiKTeX。
- Node.js 与项目包管理器：Remotion、HyperFrames、Lottie、D3 需要。
- GPU：探测显卡、驱动、VRAM、Chromium GL 后端和 FFmpeg 编码器；在 Windows/Linux 需要兼容 NVIDIA GPU、驱动和含 `h264_nvenc` 的 FFmpeg 才能使用 Remotion H.264 硬件编码。不可用时回退软件 H.264，不虚报 GPU。

缺少大型运行时时不要在 intake 阶段强装。先把镜头标为 `runtime_missing`，给出静态/Remotion 回退；只有项目真正选中该镜头后再安装或请求用户授权。Manim 官方安装入口：<https://docs.manim.community/en/stable/installation.html>。

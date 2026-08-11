# 第三方来源与使用边界

本目录是五个上游 Remotion 资源的离线工作快照。`source-manifest.json` 记录仓库、提交、授权声明、兼容状态和预期数量；每个来源自己的 README、LICENSE、package manifest 与音频归因文件仍保存在 `sources/` 内。

- video-shotcraft：Apache-2.0。其 `assets/audio/` 中不同音频可能有各自授权条件，使用前必须读取 `sources/video-shotcraft/assets/audio/ATTRIBUTION.md` 并把实际使用项写入项目来源清单。
- RVE Remotion Templates：上游 README 声明 MIT；当前快照没有独立 LICENSE 文件，发布前按项目风险要求复核上游授权状态。
- Remotion Scenes：MIT。
- Curvable Motion：MIT；个别组件有可选运行依赖。
- Remotion Playground：package.json 声明 MIT，README 声明可自由使用；这是 Remotion 2.1 / React 17 的旧实验代码，只作为移植参考。

Remotion 本身及其他依赖仍受各自许可证约束。本资料库允许分析、选型和适配，不代表可以忽略第三方素材、字体、音频、人物肖像或产品截图的授权。

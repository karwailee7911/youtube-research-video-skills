# YouTube Research Video Skills

面向中文研究型 YouTube 长视频的两个 Codex skills，适用于医学、经济、科技、文学、历史及其他证据型选题。

## Skills

### `youtube-topic-search-gate`

在写稿前验证搜索需求、竞争差异、证据强度和视觉可行性，输出 `GO`、`REWORK` 或 `PARK`。

### `youtube-research-video-production`

完成研究、单人或多角色口播稿、视觉素材、最终音频对齐、字幕、剪映草稿直写、封面和发布资料。

关键规则：

- 最终音频是字幕、画面和章节的唯一主时钟。
- 禁止用低质量 ASR 或少量人工锚点强行拉伸字幕。
- 禁止桌面或 GUI 自动化操作剪映。
- 剪映草稿写入前必须备份，写入后必须解密回读。
- 古籍只是可选的原始资料类型，不是流程前提。
- 支持单人口播、双人问答和多角色稿件。

## 安装

把需要的 skill 目录复制到 `~/.codex/skills/`：

```bash
cp -R skills/youtube-topic-search-gate ~/.codex/skills/
cp -R skills/youtube-research-video-production ~/.codex/skills/
```

重新开始一个 Codex 任务后即可触发。

## 目录

```text
skills/
├── youtube-topic-search-gate/
└── youtube-research-video-production/
```

制作 skill 中的剪映脚本需要用户已有且已验证的本地草稿加解密工具。脚本不会启动或控制剪映界面。

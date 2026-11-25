---
name: pixel-science-studio
description: 为原创科学科普动画复用像素植物机器人、情绪面屏、嫩芽动画及身体动作。
---

# Pixel Science Studio 角色演出

以仓库根目录的 `character.py` 和 `expressions.py` 为角色资产和行为来源。使用现有 80 × 76 RGBA 逻辑格与固定配色，整像素定位，预览和成片使用最近邻整数倍放大。标准角色使用 01 基础款，场景装扮通过配饰图层叠加。

```python
from character import Robot

robot = Robot(outfit="base")
robot.set_expression("surprised")
frame = robot.render("walk", frame=3, emotion_frame=8)
frame = robot.render("read", frame=2, seated=True, emotion_frame=9, page_turn=3)
```

身体帧 `frame` 和情绪帧 `emotion_frame` 可独立推进。后者省略时使用身体帧计数。使用 `set_expression("default")` 回到中性状态。单帧和批量合成可直接调用 `sprite(..., expression="focused")`。需要透明图层时，用同样参数调用 `sprite_layers` 并按返回顺序合成。实验动作可使用 `microscope`，表情和科研装扮可分别指定。

| 表情键 | 含义 | 嫩芽 |
| --- | --- | --- |
| default | 默认 | 摇摆 |
| happy | 开心 | 摇摆 |
| excited | 兴奋 | 竖直 |
| confused | 疑惑 | 合拢 |
| surprised | 震惊 | 竖直 |
| focused | 认真 | 竖直 |
| sad | 难过 | 下垂 |
| scared | 害怕 | 颤抖 |
| smug | 得意 | 摇摆 |
| unamused | 无语 | 下垂 |
| shy | 害羞 | 合拢 |
| sleepy | 困倦 | 下垂 |
| dizzy | 眩晕 | 颤抖 |
| inspired | 灵感 | 竖直 |
| laughing | 大笑 | 摇摆 |
| angry | 生气 | 竖直 |

震惊使用睁大的金色像素眼、竖直嫩芽和空嘴巴层。道具要落入短手可及的范围，阅读翻页优先让纸靠近身体，用同一只短手随纸移动。场景家具按前后顺序独立合成。逐段检查接触帧和轮廓遮挡，包括坐下瞬间、翻页最高点和表情出现的第一帧。

运行 `python render.py` 重新导出透明图层、表情预览、基础动作和无声样片。参考 `README.md` 中的角色尺寸和色值。

## 节目模板

统一使用三个段落。开头和结尾复用 `studio.renderer.brand_room()` 的固定科研小屋，镜头、家具与基础款主持人由品牌代码控制。每集把标题、台词、科学故事绘图函数、时长、动作、表情和论文元数据写进 `episodes/` 下的独立模块，并公开 `EPISODE`。

1. **科研小屋·故事导入**。用角色动作、已有道具和中文对话引出问题。导入和总结使用贴底的描边字幕，沿用固定主持人位置。台词每个框最多两行，长句拆成多个节拍提示。
2. **科学故事**。用 `story_scene(local_beat, pulse)` 返回原生 320 × 180 的 RGBA 场景。主要事件、实验步骤、分子机制、坐标轴、数据和图例放在 y=0–123。主持人按原图 50% 最近邻缩放，在左下角，台词放在右侧的紧凑对话框内。底部 y=124–179 为主持区。在镜头需要完整画幅时，将该提示的 `visible` 设为 `False`，主持人与对话框会一起隐藏。示意图注明性质，数据图标注来源、单位和条件。
3. **科研小屋·总结**。回到同一小屋，总结研究发现和意义。论文集使用 `Paper(title, authors, journal, year, doi)`，并指定 `paper_start` 和 `farewell_start`。论文卡出现在总结之后，停留到挥手告别开始。核对论文元数据原文，给卡片保留读完所需时间。非论文集可直接挥手。

### 参数与可复用模块

- `studio.timeline.Cue(beat, dialogue, expression="default", action="idle", visible=True)` 定义绝对拍号上的演出提示。每段首条提示的拍号等于其边界，段内拍号严格递增。动作、表情和台词分别配置。
- `studio.timeline.Episode(..., story_start, summary_start, end, story_scene, bpm=120)` 配置故事入点、返回小屋入点、结束拍号、故事场景和节拍。拍号从零开始，120 BPM 时每拍 0.5 秒。镜头过渡由 `studio.graphics.curtain` 生成，转场遮挡最满时切换场景。
- `studio.graphics` 包含两行中文对话框、底部字幕、转场和可单独导出的 `paper_card`。默认使用 Noto Sans CJK SC Bold，用双分辨率栅格和轻度抗锯齿保留像素风格与可读性。默认字体路径为 Debian 系统的 `fonts-noto-cjk`，使用简体中文索引 2。可通过 `STUDIO_CJK_FONT` 和 `STUDIO_CJK_FONT_INDEX` 换成可用的简体中文字体，单字体文件通常用索引 0。
- `studio.timeline.BeatClock` 将拍号换算成秒，并提供画面重音 `pulse`。`--demo-music` 使用同一个时钟生成无歌词配乐。外部配乐先剪到第一拍正好落在文件起点，将 `bpm` 设为音轨的实测恒定 BPM，再用 `--music` 输入。渲染器从零时刻同步，按片长截断或补静音。省略音乐参数导出无音轨视频。流程样片使用字幕对话，角色语音可独立试听与制作。
- `studio.renderer.Program.frame(seconds)` 可独立生成检查帧。`render_episode.py` 渲染整集，使用 320 × 180 原生画布、4 倍最近邻放大及 24 fps 输出。

### 制作与检查

先核对科学来源和引用字段，再写三段脚本与拍点；随后制作故事镜头并用安全区摆放图解或数据。渲染后抽查开场提问、两次转场、主持人显隐、总结、论文卡（适用时）及挥手镜头。检查台词截断、播放时长、节拍落点和最后一帧。使用全片解码检查输出文件。

```bash
python render_episode.py --episode episodes.light_demo --demo-music \
  --output output/program-test.mp4 --previews output/program-previews
```

## 角色语音

当前没有选定角色音色。六份试听均使用同一段文字、Kokoro v1.1-zh INT8 模型和 1.0 语速。保留原文的 DNA，合成词典按 D、N、A 发音。试听使用原音，待选定后再审听轻微机器人质感的后处理。

首选离线 Kokoro + sherpa-onnx，便于固定版本、批量调用并控制成本。模型包与引擎分别提供 Apache 2.0 许可。离线推理没有按字符计费，适合商业制作。若分发软件或模型本身，随包保留适用许可和版权声明。备选为正式 Azure AI Speech 神经语音 API。切换前核对官方服务条款、当前定价和所选语音用途，并保留服务配置与结算记录。

### 复现试听

在项目根目录安装 `requirements-voice.txt`（另需 FFmpeg）。模型权重另行下载并校验发布者提供的 SHA-256。

```bash
mkdir -p .voice-models
curl -fL -o .voice-models/kokoro.tar.bz2 \
  https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-int8-multi-lang-v1_1.tar.bz2
printf '%s\n' '259c9c8bc906d6078e4e0570421885dabb68b539c2f970fcbb890a58eeaf3e9c  .voice-models/kokoro.tar.bz2' | sha256sum -c -
tar -xjf .voice-models/kokoro.tar.bz2 -C .voice-models
python -m studio.voice --model .voice-models/kokoro-int8-multi-lang-v1_1
```

### 同步方式

- 每句用一个 `SpokenCue` 同时配置文字、表情、身体动作和句后停顿。`render_voice` 从同一 PCM 源导出 WAV、句级 SRT 和 24 fps JSON 时间轴。
- 渲染时用 `speech_at(timing, seconds - clip_start)` 取当前台词及嘴型。将条目的 `expression` 传给 `Robot.set_expression`，`action` 和 `speech_mouth` 传给 `Robot.render`。体态与情绪仍使用各自帧率，嘴型按音频采样时间推进。试听的闭口、小口、张口为音量驱动预览；正式集若需要精确咬字，使用音素对齐成果替换 `mouth_frames`。
- 音色确认后在本节固定引擎版本、模型校验和、音色 ID、语速、发音词典、句间停顿及后处理参数。每集沿用该配置，并检查字幕断句、口形与首尾静音。

许可与服务来源：[Kokoro v1.1-zh 模型卡](https://huggingface.co/hexgrad/Kokoro-82M-v1.1-zh) · [sherpa-onnx 模型发布页](https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models) · [sherpa-onnx 许可](https://github.com/k2-fsa/sherpa-onnx/blob/master/LICENSE) · [Azure AI Speech 定价](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)

## 品牌仪式与科研档案

正式节目使用 `render_brand.py`，将已有三段式节目套入固定开场、嫩芽转场与片尾。保持科研小屋原构图、基础款机器人的配色和比例，镜头特写复用同一小屋素材。低分辨率场景保留整像素边缘，台词、标题和档案编号在较高分辨率的文字层绘制。

- **开启科学档案（4.6 秒）**。首帧显示档案编号和主题，并同步播放电脑提示音。随后切回小屋全景，播放固定三音动机。固定开场字幕为「今天，又发现了什么有趣的科学秘密呢？」。每集故事导入在固定开场之后单独排期。
- **开启科学世界（1 秒）**。使用早期样片的绿底金边阶梯像素卷帘，在画面完全遮挡时切换，伴随上行音效。保持角色原有短手比例。主持人仍复用故事段左下角安全区。
- **收藏科学发现（10.5 秒）**。总结及可选论文信息卡之后，将纸页合进绿色档案、盖上 `DISCOVERY COMPLETE`、归入书架，然后回到正面挥手。固定字幕为「今天的知识，又发了一颗小芽。我们下次见！」。最后出现「让知识发芽」与三音动机的低音柔和变奏。临时使用字幕，等音色确认后再接入角色语音。
- **声音标识**。开场、论文通知、嫩芽启动、科学发现、盖章和片尾均由 `studio.brand.sound` 合成。使用 `--sounds` 导出独立 WAV 供剪辑混音。每个音效保留柔和包络，按时间轴落点排布。

### 配置新一集

1. 在 `episodes/` 定义当期 `EPISODE`。论文集填入 `Paper` 的标题、作者、期刊、年份和 DOI，保留论文卡所需阅读时间，并像旧模板一样设置挥手入点。品牌片尾接管该入点之后的演出。故事道具、台词和主持人演出属于当集内容。
2. 用 `--number` 指定正整数档案号，画面格式为 `SA-001`。主题默认读取 `Episode.title`，可通过 `--theme` 指定档案主题。若为论文集，目录同时保存 DOI。
3. 使用长期维护的 `--catalog` JSON。历史档案按编号读取，重剪旧集时只显示该集之前的档案。镜头书架当前展示最近 21 册，目录保留全部。审核通过后用 `--record` 记录，渲染或解码失败不会入库。相同档案重复写入不增加副本，已占用号码对应不同主题或 DOI 时会报错。

```bash
python render_brand.py --number 1 --compact-demo \
  --catalog assets/brand/demo-catalog.json \
  --output output/brand-test.mp4 --previews output/brand-previews \
  --sounds assets/brand/sfx
```

程序调用使用 `BrandProgram(episode, Archive(number, theme, doi), records)`，`frame(seconds, caption_scale=2)` 可抽帧审核，`write_audio(path)` 生成完整音效轨。模块分别位于 `studio/brand/ritual.py`、`transition.py`、`archive.py`、`sound.py`。

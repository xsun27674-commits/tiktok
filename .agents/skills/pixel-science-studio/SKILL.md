---
name: pixel-science-studio
metadata:
  version: "V1.0"
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
- **收藏科学发现（10.5 秒）**。总结及可选论文信息卡之后，直接展示绿色档案封面、盖上 `DISCOVERY COMPLETE`、归入书架，然后回到正面挥手。固定字幕为「今天的知识，又发了一颗小芽。我们下次见！」。最后切到 1.6 秒的深绿纯色品牌卡，呈现基础款机器人、「让知识发芽」与三音动机的低音柔和变奏。临时使用字幕，等音色确认后再接入角色语音。
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

## V1.0 正式制作

在项目根目录打开 Codex，调用 `$pixel-science-studio` 并提供主题、论文（DOI、链接或全文）和故事脚本。角色配色、动作与表情、科研小屋、字幕和对话框、主持人、卷帘、归档和深绿品牌卡沿用 V1.0。每集在 `episodes/` 新建模块，沿用 `Episode` 和 `Cue`，接入 `render_brand.py`。新增图像、道具和数据放在各集专属目录，通用素材经确认再加入共享库。原始素材不覆盖，正式输出使用各集独立路径。

**科学完整性。** 先读原论文相关方法、图表、图注和补充材料，记录 DOI、图表编号、实验条件、样本量和单位。逐条校对脚本结论，区分实测、作者解释、相关性和假说。实验过程和分子图示标明「示意」，分子机制只画论文支持的步骤。不得编造数据、误差、显著性或研究结论，缺少原始数据时用有来源的定性示意或转述。使用 `studio.science.diagram` 画步骤或机制，用 `studio.science.series` 绘制有来源的观测点，在字幕层补全单位、轴范围和图注。把完整引用与数据出处随集保存。

**已确认配乐。** 固定使用 `output/music-auditions/` 的四首确认版音频。小屋导入配《科研小屋》96 BPM，故事默认《科学探险》，微观主题用 `--story-music micro`。总结到品牌片尾配《今日的发现》。音乐淡入淡出并低于品牌音效。节目当前只用字幕和音效/配乐，语音接口暂存于 `studio.voice`，历史试听不属于正式音轨。旧样片使用 `--effects-only` 复现。

**制作与交付。** 已有目录下使用下一未用档案号，先运行无视频检查，再按任务需要输出审核版。核验论文引用、观众阅读时长、主持人安全区、字幕、音效、档案编号和成片解码。通过审核后用 `--record` 归档。Git 标签 `pixel-science-studio-v1.0` 是可恢复的版本快照，后续在新提交中扩充素材。

```bash
python render_brand.py --episode episodes.light_demo --compact-demo --number 1 --check
# 将模块名、编号和输出路径换成本集值，正式制作时去掉 --check。
```

## PaperMark · 论文证据展示

PaperMark 用科普的方式表达，用科研的逻辑叙事。每集按「提出问题 → 原文定位 → 实验怎么做 → 原始证据怎么看 → 结论能走多远」切换场景。用故事内的动作与微观示意解释科学过程，只有需要逐项阅读时才短暂放大论文和图表。

1. **收集原文与授权。** 使用已核验 DOI 的论文 PDF 首页，或期刊官网的原始页面截图，核对标题、作者与页面身份。不得使用 AI 生成页面、人工复刻的论文首页或无来源截图。记录原始地址、授权条款地址、署名格式、改编条件与必要的书面许可。截图、原图和图中第三方材料分别核查，不以能下载作为授权凭据。无法核实原文或授权时暂停原图镜头，说明缺项。经核验的数据可依据许可独立绘图，并注明与原图关系。
2. **用原文切入故事。** 固定开场结束后，镜头从原小屋推向电脑。框选原文中与本集问题直接相关的文字，利用像素放大镜和关键词引导阅读。原图保持比例，不改写原文。统一信息卡展示中英文标题、作者、研究机构、期刊、发表日期、档案号与 DOI。完整作者及机构对应关系随集保存在来源记录中，卡片使用适合阅读长度的署名。
3. **把论文图表放回实验过程。** 先用像素镜头交代样品、对照、变量和测量方法，再展示相应原图。每个原图插入标明 `Figure` 编号、文献来源和必要的图版许可署名。用 `studio.science.diagram` 表达流程，用明确标注的示意表现机制。保留原图的轴、单位、图例和标注，只有获得许可才能裁切、重排或改编。若图表缩小后不可读，先用 `studio.science.series` 对许可范围内的实测点作独立图解，并在片中标注 DOI 和对应图号。
4. **总结证据边界。** 先给出论文支持的发现与意义，然后在科研小屋分别交代一个实质局限和一个尚未解决的问题。区分试验条件与一般情形、替代指标与最终结局，并保留品牌盖章、挥手和片尾卡。

### 调用与资料清单

将清单 JSON 和有权限使用的源文件保存在本集专属目录。PNG 截图应来自授权原文，PDF 首页由 Poppler 的 `pdftoppm` 从真实原件提取。SHA-256 固定审核过的文件内容，清单中授权声明须由制作时的人核对填写。

- 顶层字符串字段为 `title_en`、`title_zh`、`authors`、`institutions`、`journal`、`publication_date`（YYYY-MM-DD）、`doi`、`limitations`、`open_questions`。最后两项分别符合现有两行字幕限制。
- `front_page` 包含 `file`（相对于清单的路径）、`kind`（`pdf_first_page` 或 `publisher_capture`）、`sha256`、`source_url`、`rights_url`、`rights_note`、`allow_reproduction`。只有证据确认支持播放时填写 `allow_reproduction: true`。
- `highlights` 是一个或多个 `{"box":[x0,y0,x1,y1],"keyword":"原文对应阅读提示"}`。坐标为相对于原件宽高的 0–1 小数。
- `figures` 可为数组，每项使用同样的文件来源和许可字段，`kind` 为 `original_figure`，另填 `figure`（如 `Figure 2a`）、`citation`、`start` 和 `end`（故事段内相对秒数）。图表时段不得重叠。短引用写在画面，完整署名与条款留在资料清单内。无原图授权时从清单省略该图，并按第 3 步处理。
- 模块入口是 `studio.papermark.PaperMark(manifest)`，通过 `BrandProgram(..., paper_mark=...)` 接入。每期 PaperMark 检查路径使用：

```bash
python render_brand.py --episode episodes.paper_example --number 1 \
  --paper-mark path/to/episode/evidence.json --check
```

审核时逐一核对论文截图、放大语句、图表引用、利益相关的限制以及字幕读取时间。确认后去掉 `--check` 并传入当集的独立输出路径。默认品牌轨与通用节目的调用方式照旧。

### PaperMark 镜头验收

- 小屋道具分前景、角色和后景。手持物跟随手部锚点，与角色一起接受桌沿遮挡；桌面道具的底边必须落在桌面。电脑内容只画在屏幕内部，避免遮住嫩芽和面部。
- 麦田用留白和几根可辨认的前景麦穗交代生长状态，背景麦行降低密度和对比度。检查缩小后主持人的发光眼、腮红和眼镜，统一沿用原始透明素材的调色与最近邻缩放。发现单像素高光消失时调整布局或显示尺寸，避免临时改色。
- 需要统一配乐时，按实际时长循环同一已确认的曲目，以短交叉淡化接续。导出前在前、中、后段检查音乐信号，尤其在重复交界和没有音效的静场；单有音轨或首段有声不足以通过验收。

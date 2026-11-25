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

1. **科研小屋·故事导入**。用角色动作、已有道具和中文对话引出问题。导入镜头固定主持人位置与对话框位置。台词每个框最多两行，长句拆成多个节拍提示。
2. **科学故事**。用 `story_scene(local_beat, pulse)` 返回原生 320 × 180 的 RGBA 场景。主要事件、实验步骤、分子机制、坐标轴、数据和图例放在 y=0–123。主持人按原图 50% 最近邻缩放，在左下角，台词在其右侧。底部 y=124–179 为主持区。在镜头需要完整画幅时，将该提示的 `visible` 设为 `False`，主持人与对话框会一起隐藏。示意图注明性质，数据图标注来源、单位和条件。
3. **科研小屋·总结**。回到同一小屋，总结研究发现和意义。论文集使用 `Paper(title, authors, journal, year, doi)`，并指定 `paper_start` 和 `farewell_start`。论文卡出现在总结之后，停留到挥手告别开始。核对论文元数据原文，给卡片保留读完所需时间。非论文集可直接挥手。

### 参数与可复用模块

- `studio.timeline.Cue(beat, dialogue, expression="default", action="idle", visible=True)` 定义绝对拍号上的演出提示。每段首条提示的拍号等于其边界，段内拍号严格递增。动作、表情和台词分别配置。
- `studio.timeline.Episode(..., story_start, summary_start, end, story_scene, bpm=120)` 配置故事入点、返回小屋入点、结束拍号、故事场景和节拍。拍号从零开始，120 BPM 时每拍 0.5 秒。镜头过渡由 `studio.graphics.curtain` 生成，转场遮挡最满时切换场景。
- `studio.graphics` 包含两行中文对话框、段落标签、转场和可单独导出的 `paper_card`。默认使用 Noto Sans CJK SC Bold，以 1 位字形遮罩保持像素硬边。默认字体路径为 Debian 系统的 `fonts-noto-cjk`，使用简体中文索引 2。可通过 `STUDIO_CJK_FONT` 和 `STUDIO_CJK_FONT_INDEX` 换成可用的简体中文字体，单字体文件通常用索引 0。
- `studio.timeline.BeatClock` 将拍号换算成秒，并提供画面重音 `pulse`。`--demo-music` 使用同一个时钟生成无歌词配乐。外部配乐先剪到第一拍正好落在文件起点，将 `bpm` 设为音轨的实测恒定 BPM，再用 `--music` 输入。渲染器从零时刻同步，按片长截断或补静音。省略音乐参数导出无音轨视频。节目使用字幕对话，不加入语音旁白。
- `studio.renderer.Program.frame(seconds)` 可独立生成检查帧。`render_episode.py` 渲染整集，使用 320 × 180 原生画布、4 倍最近邻放大及 24 fps 输出。

### 制作与检查

先核对科学来源和引用字段，再写三段脚本与拍点；随后制作故事镜头并用安全区摆放图解或数据。渲染后抽查开场提问、两次转场、主持人显隐、总结、论文卡（适用时）及挥手镜头。检查台词截断、播放时长、节拍落点和最后一帧。使用全片解码检查输出文件。

```bash
python render_episode.py --episode episodes.light_demo --demo-music \
  --output output/program-test.mp4 --previews output/program-previews
```

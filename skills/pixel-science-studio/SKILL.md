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

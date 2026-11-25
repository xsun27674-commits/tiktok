# 品牌配乐试听

四首均为原创旋律、和声与编曲。采用采样乐器、力度变化、错开的节奏和轻量空间混响渲染。MP3 为审批用整段小样，保留自然尾音。

| 曲名 | 节拍 | 编曲 |
| --- | --- | --- |
| 科研小屋 | 104 BPM | 轻钢琴分解和弦、马林巴主旋律、八音盒点缀 |
| 科学探险 | 112 BPM | 木琴问答、马林巴错拍、尼龙弦和轻拨贝斯 |
| 微观世界 | 82 BPM | 柔和合成铺底、高音八音盒和留白钢琴 |
| 今日的发现 | 76 BPM | 轻钢琴重奏开场主题、弱八音盒与柔和垫音 |

开场与片尾共享从 C、E、G 三音发展出来的八音动机，沿用节目已有的三音提示。片尾保留音程和节奏轮廓，降低速度并以钢琴接替马林巴。

## 复现

运行环境需要 Python、NumPy、FluidSynth 3 运行库和 FFmpeg。编曲源文件为 `score.py`。在项目根目录执行：

```bash
python -m auditions.music.render --soundfont /path/to/GeneralUser-GS.sf2
```

试听使用 GeneralUser GS 2.0.3，固定于上游提交 `684543d5e5efaef08d02be50dcda8d552478fa60`。上游许可明确允许私人及商业音乐制作和从录音获利，也说明少量历史采样的来源无法完全追溯。交付的是原创曲目的成品和编曲代码，乐器采样库随上游独立分发。

[GeneralUser GS 许可原文](https://github.com/mrbumpy409/GeneralUser-GS/blob/684543d5e5efaef08d02be50dcda8d552478fa60/documentation/LICENSE.txt)

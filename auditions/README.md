# 角色语音第二轮试听

同一段测试台词一次输入 ZipVoice-Distill 中英双语模型，保留问句和感叹句的标点。六个音色使用六段合成的参考声线，没有使用真人录音。Kokoro 只生成另一段用于条件输入的参考台词，测试台词由 ZipVoice 重新合成。试听只统一响度，保留各候选原本的节奏和音高。此轮为音色探索，正式节目未接入候选语音。

## 方案调查

| 方案 | 调用成本 | 公开与商业发布 |
| --- | --- | --- |
| Fun-CosyVoice 3 自部署 | 本地推理无按量 API 费，需承担运行机器和部署成本。模型官方分发端点 Hugging Face 与 ModelScope 在当前环境均被拒绝，未实测。 | 官方代码库为 Apache 2.0。正式使用前还需以所下载 checkpoint 的模型卡和参考声音授权为准。 |
| 火山引擎豆包语音合成 | 托管 API，需核对具体模型、音色和资源包。当前环境无法访问官方计费页或 API，未核实当前单价。 | 需以所选资源的服务协议和音色授权范围为准，未核实具体公开发行权。 |
| ElevenLabs Eleven v3 | 托管 API，费用取决于订阅、额度及模型。当前环境无法访问官方定价和接口，未核实当前价格。 | 商业发行应核对当期商业许可、生成时所用计划和具体声音许可。 |
| ZipVoice-Distill INT8 | 本轮在 CPU 实测，无 API 费用。 | ZipVoice 代码为 Apache 2.0。发布包未附单独的 checkpoint 许可说明，本轮文件用于试听。正式商用前仍需核对模型权重许可。 |

官方入口：[CosyVoice 项目和模型](https://github.com/FunAudioLLM/CosyVoice) · [豆包语音产品文档](https://www.volcengine.com/docs/6561) · [ElevenLabs 定价](https://elevenlabs.io/pricing) · [ElevenLabs 发布条款说明](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-that-I-generate-on-the-platform) · [ZipVoice 项目源码与许可](https://github.com/k2-fsa/ZipVoice)

## 复现本轮试听

使用项目的 `requirements-voice.txt` 和 FFmpeg。模型由 sherpa-onnx 官方发布页提供，下载后使用发布的 SHA-256 校验。模型权重不随项目分发。

| 文件 | SHA-256 |
| --- | --- |
| `sherpa-onnx-zipvoice-distill-int8-zh-en-emilia.tar.bz2` | `77219c8b40f4ee8d73a7f902305ff6c1128ef9b54461c41b4ca6ed890b6c2803` |
| `kokoro-int8-multi-lang-v1_1.tar.bz2` | `259c9c8bc906d6078e4e0570421885dabb68b539c2f970fcbb890a58eeaf3e9c` |
| `lexicon-en-us.txt` | `8b67ae549a465eee78f92ecb74644ad90c3c58ce65f19c68baf85878a10ef73a` |
| `vocos_24khz.onnx` | `bcb3b970e384161c4d634f0bb9e999ff1c471b34c9bc0b1049a5014065ed3cc0` |

[模型与词典](https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models) · [Vocos 模型](https://github.com/k2-fsa/sherpa-onnx/releases/tag/vocoder-models)

```bash
python -m auditions.zipvoice_round2 \
  --model .voice-models/sherpa-onnx-zipvoice-distill-int8-zh-en-emilia \
  --reference-model .voice-models/kokoro-int8-multi-lang-v1_1 \
  --lexicon .voice-models/lexicon-en-us.txt \
  --vocoder .voice-models/vocos_24khz.onnx
```

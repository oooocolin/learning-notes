---
title: ONNX
tags:
  - AI
  - ONNX
---
## 一、概述
在一般的深度学习模型构建的流程中，常用的框架有 `PyTorch` 、 `TensorFlow` 等，一般都是在 `Python` 环境进行模型训练以及保存为特定框架的特定模型文件或是参数文件。这与框架强绑定，并且跨平台部署困难。所以 `ONNX` 应运而生，它可以实现各框架之间的相互转化，在这其中作为中间表示，并且对不同硬件平台统一接口，并做到了训练环境与部署环境分离。
## 二、部署模型的选型
- 把模型保存为 `.onnx` 文件，使用 `ONNX Runtime` 在推理环境中加载。更适合跨平台场景。
- 转换为推理引擎的专用格式，可以更贴合特定的硬件，性能往往更高。
	- `TensorRT`：针对 `NVIDIA GPU` 优化。（需要转换成专门的 `engine` 文件）
	- `OpenVINO`：`Intel CPU/NPU` 优化。
	- `CoreML`：苹果设备（`iOS/macOS`）。
	- `TFLite`：移动端和边缘设备（主要是 `TensorFlow` 生态）。
- 封装为服务（常用于企业部署），以 `REST/gRPC` 服形式存在，由此可以进行负载均衡。
- 编译成可执行库或代码，可以使用在移动端直接嵌入 `APP`，如 `ncnn/MNN` 等。
## 三、保存与导入
### 1. 保存（从 `PyTorch` 保存为 `ONNX`）
```python
def torch.onnx.export(model, args, f, *, export_params, verbose, input_names, output_names, opset_version, dynamic_axes, do_constant_folding)
```
- `model`：导出的 `PyTorch` 模型。
- `args`：模型输入张量示例，输入数据的类型和形状必须与模型训练时使用的相匹配。
- `f`：保存模型的文件路径。
- `export_params`：指定是否将模型的参数导出到 `.onnx` 文件，默认为 `True` 。
- `verbose`：是否启用详细日志记录，默认为 `None` 。
- `input_names`：输入节点的名称列表，默认为 `None` 。
- `output_names`：输出节点的名称列表，默认为 `None` 。
- `opset_version`：`ONNX` 操作集的版本号，默认为 `None` ，表示最新稳定版。
- `dynamic_axes`：指定输入或输出维度是动态的，默认为与 `args` 保持一致。
- `do_constant_folding`：指定是否在导出过程中进行常量折叠优化。
### 2. 导入
```python
# 读取模型
onnx_model = onnx.load("resnet18.onnx")

# 检查模型是否有效
onnx.checker.check_model(onnx_model)

# 创建 ONNX Runtime 会话
runtime_session = onnxruntime.InferenceSession("resnet18.onnx")

# 创建输入数据
input_image = np.random.randn(1, 3, 224, 224).astype(np.float32)

# 运行模型，注意这里的 "input" 关键字要和保存模型的输入名称一致
outputs = runtime_session.run(None, {"input": input_image})
```
**注意**：使用 load() 方法导入的 ONNX 模型数据类型是 ModelProto ，与 `PyTorch` 模型类型不一致，一般不直接使用。











---
title: ONNX
tags:
  - AI
  - ONNX
---
## 概述
在一般的深度学习模型构建的流程中，常用的框架有 `PyTorch` 、 `TensorFlow` 等，一般都是在 `Python` 环境进行模型训练以及保存为特定框架的特定模型文件或是参数文件。这与框架强绑定，并且跨平台部署困难。所以 `ONNX` 应运而生，它可以实现各框架之间的相互转化，在这其中作为中间表示，并且对不同硬件平台统一接口，并做到了训练环境与部署环境分离。
## 保存与导入
### 保存（从 `PyTorch` 保存为 `ONNX`）
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
**注意**：保存的 `ONNX` 模型可在 [`netron`](https://netron.app/) 中查看，在 `netron` 使用 `.oonx` 文件比 `.pt` 文件查看的结构更为清晰。
### 导入
```python
# 读取模型
onnx_model = onnx.load("resnet18.onnx")

# 检查模型是否有效
onnx.checker.check_model(onnx_model)
```
**注意**：使用 load() 方法导入的 ONNX 模型数据类型是 ModelProto ，与 `PyTorch` 模型类型不一致，一般不直接使用。
## 部署模型的选型
- 把模型保存为 `.onnx` 文件，使用 `ONNX Runtime` 在推理环境中加载。更适合跨平台场景。
- 转换为推理引擎的专用格式，可以更贴合特定的硬件，性能往往更高。
	- `TensorRT`：针对 `NVIDIA GPU` 优化。（需要转换成专门的 `engine` 文件）
	- `OpenVINO`：`Intel CPU/NPU` 优化。
	- `CoreML`：苹果设备（`iOS/macOS`）。
	- `TFLite`：移动端和边缘设备（主要是 `TensorFlow` 生态）。
- 封装为服务（常用于企业部署），以 `REST/gRPC` 服形式存在，由此可以进行负载均衡。
- 编译成可执行库或代码，可以使用在移动端直接嵌入 `APP`，如 `ncnn/MNN` 等。
## 模型的部署
### 部署在 `ONNX Runtime` 
`Python` 实现：
```python
# 创建 ONNX Runtime 会话
runtime_session = onnxruntime.InferenceSession("resnet18.onnx")

# 创建输入数据
input_image = np.random.randn(1, 3, 224, 224).astype(np.float32)

# 运行模型，注意这里的 "input" 关键字要和保存模型的输入名称一致
outputs = runtime_session.run(None, {"input": input_image})
```
`C++` 实现：
```cpp
// ONNX 模型地址，需改为宽字符串才能加载模型
std::string onnxpath = "resnet18.onnx";
std::wstring modelPath = std::wstring(onnxpath.begin(), onnxpath.end());

// 创建环境，指定日志级别
Ort::Env env = Ort::Env(ORT_LOGGING_LEVEL_ERROR, "yolov8-onnx");
// 创建会话选项
Ort::SessionOptions session_options;
// 优化器级别，指定为基本优化级别
session_options.SetGraphOptimizationLevel(ORT_ENABLE_BASIC);
// 设置线程数
session_options.SetIntraOpNumThreads(4);
// 设备使用优先使用GPU，没有则使用CPU
OrtSessionOptionsAppendExecutionProvider_CUDA(session_options, 0);
OrtSessionOptionsAppendExecutionProvider_CPU(session_options, 1);

// 创建 ONNX-Runtime 会话
Ort::Session session(env, modelPath.c_str(), session_options);

...

ort_outputs = session_.Run(Ort::RunOptions{ nullptr }, inputNames.data(), &input_values_, 1, outNames.data(), outNames.size());

...
```
`C++` 实现 `Run()` 方法解析：
```cpp
std::vector<Ort::Value> session_.Run(
    const Ort::RunOptions& run_options,
    const char* const* input_names,
    const Ort::Value* const* input_values,
    size_t num_inputs,
    const char* const* output_names,
    size_t num_outputs
);
```
- `run_options`：配置推理运行的选项，可设置是否开启某些优化等，不需要则填入 `Ort::RunOptions{nullptr}` 表示使用默认选项。
- `input_names`：输入节点名称，如 `"input_0"`。
- `input_values`：输入节点的实际数据，需为引用类型。
- `num_inputs`：输入节点的数量，表示一次输入节点的数据数量。
- `output_names`：输出节点的名称。
- `num_outputs`：输出的数量，表示模型会返回多少个输出。
### `ONNX` 转 `TensorRT` 
#### (1). 使用 `onnx2trt` 工具直接转换
在使用 `pip` 安装了 `tensorrt` 包后就含有了 `onnx2trt` 工具，就可以通过命令行直接转化为 `TensorRT Engine` 格式。
```shell
onnx2trt model.onnx -o model.trt
```
还可以进一步优化转换：
- `-b`：设置批量大小。
- `-d`：设置 `GPU` 设备 `ID` （如果有多个 `GPU`）
- `-fp16`/ `-int8`：使用 `FP16` 或 `INT8` 精度
#### (2). 使用 `Python` 进行转换
```python
import tensorrt as trt
import onnx
from onnx import numpy_helper

# 载入 ONNX 模型
onnx_model = onnx.load("model.onnx")

# 创建一个 TensorRT 的日志
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

# 创建一个构建器
builder = trt.Builder(TRT_LOGGER)
# 目标网络结构
network = builder.create_network(trt.NetworkDefinitionCreationFlags.EXPLICIT_BATCH)
# ONNX模型解析器
parser = trt.OnnxParser(network, TRT_LOGGER)

# 解析 ONNX 模型文件
with open("model.onnx", "rb") as f:
    if not parser.parse(f.read()):
        print("ERROR: Failed to parse the ONNX model")
        for error in range(parser.num_errors):
            print(parser.get_error(error))

# 配置 builder（比如 FP16 或 INT8 精度）
builder.fp16_mode = True  # 开启 FP16
builder.max_batch_size = 1  # 设置批次大小

# 构建 TensorRT 引擎
engine = builder.build_cuda_engine(network)

# 保存 TensorRT 引擎
with open("model.trt", "wb") as f:
    f.write(engine.serialize())
```
### `ONNX` 转 `CoreML` 
需要使用 `pip` 安装 `coremltools` 包，可以将各种框架模型转化为 `CoreML` 格式。可以用于 `CoreML Python` 执行或是 `Swift` 原生开发。
```python
import coremltools as ct
import onnx

# 加载 ONNX 模型
onnx_model = onnx.load('model.onnx')

# 转换为 CoreML 模型
coreml_model = ct.convert(onnx_model)

# 保存 CoreML 模型
coreml_model.save('model.mlmodel')
```

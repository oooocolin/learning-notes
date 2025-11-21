---
title: OpenCV-C++
tags:
  - cxx
  - opencv
---
## 概述
`OpenCV` 是一个开源的计算机视觉和机器学习软件库，广泛应用于图像处理、物体检测、机器学习等领域。其主要的模块包括：

|      模块      |                        描述                        |
|:------------:|:------------------------------------------------:|
|    `Core`    |                基本的数据结构和基本数据的基本操作                 |
|  `Imagproc`  |        图像处理功能，包括滤波、几何变换、边缘检测、形态学操作、直方图计算等        |
|  `Highgui`   |                 图像和视频的显示、鼠标和键盘事件                 |
|  `Calib3d`   |                  相机校准、3D重建、立体视觉                  |
| `Featured2d` |          特征检测，如 `SIFT`、 `SURF` 、 `ORB`           |
|     `ML`     |              机器学习模块，如 `SVM` 、 `KNN`              |
|    `DNN`     | 加载和运行深度学习模型的模块，支持 `TensorFlow` 、 `ONNX` 、`Caffe` |
## 安装与配置
### 安装 `OpenCV`
#### (1). 使用包管理工具（如 `vcpkg`）
```shell
# 克隆 vcpkg
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
bootstrap-vcpkg.bat

# 安装 opencv（默认安装最新版本）
vcpkg install opencv
```
#### (2). 使用预编译包
可在官网或者 `GitHub` [OpenCV-Released](https://github.com/opencv/opencv/releases) 下载预编译包，`Linux` 可用 `apt`、`yum` 安装，`MacOS` 可用 `brew` 安装。但是在 `GitHub` 上的预编译的 `Windows` 是使用 `Visual Studio` 编译的，如果要使用 `MinGW` 编译的版本需要自己编译。
#### (3). 自己编译安装
在 `GitHub` 下载源码，可以使用 `Visual Studio` 、`CLion` 或是 `make` 编译，安装到系统路径或是编译后再移动到指定路径。以下说明使用 `CLion` 进行 `MinGW` 的编译。
- 在 `GitHub` 下载源码，在 `CLion` 打开工程；
- 配置 `CMake` 工程配置信息，确定构建类型、工具链、 `CMake` 选项等；（**注意**：由于源码中包含着多个版本的我们只需要 `C++` 的版本，并且 `Python` 和 `C++` 在编译时头文件本身就有冲突，会导致编译不成功。需要禁用 `Python` 支持）
```cmake
-DBUILD_opencv_python2=OFF 
-DBUILD_opencv_python3=OFF 
-DBUILD_opencv_python_bindings_generator=OFF 
-DBUILD_opencv_python_tests=OFF

# 可选选项
-DBUILD_opencv_java=OFF
-DBUILD_opencv_apps=OFF
-DBUILD_SHARED_LIBS=OFF  # 编译为静态链接，避免DLL问题
-DBUILD_EXAMPLES=OFF
-DBUILD_PERF_TESTS=OFF
-DWITH_MSMF=OFF
```
- 重新加载 `CMake` 项目；
- 点击菜单栏 `构建 -> 构建项目` 执行构建项目，等待执行完成；
- 生成的文件夹即为编译的文件，可以将这个文件夹复制到想要的其他文件夹，然后指定 `CMakeLists.txt` 文件内的 `OpenCV` 地址 `OpenCV_DIR` 为复制的地址。
### `CMake` 项目配置
如果 `OpenCV` 安装在默认地址，或是使用 `vcpkg` 包管理器安装的（在 `vcpkg\installed\` 文件夹里），只需在 `CMakeLists.txt` 配置查找 `OpenCV` ，并链接 `OpenCV` 库。
```cmake
find_package(OpenCV REQUIRED)

target_link_libraries(main PUBLIC ${OpenCV_LIBS})
```
如果是安装在自定义地址，需要自己指定地址。
```cmake
set(OpenCV_DIR "<file_path>")  # <file_path> 是绝对路径
find_package(OpenCV REQUIRED)

target_link_libraries(main PUBLIC ${OpenCV_LIBS})
```
**注意**：`Windows` 安装的预编译包指定 `OpenCV_DIR` 的地址路径需要为 `~/opencv/build/x64/vc16/lib` 而不是只指定在 `~/opencv/build/` 地址（ `~` 为安装时选择安装的地址，需自行填入）。
### 导入内容
在需要使用的源文件导入头文件，可以选择使用命名空间简化模块的使用。
```cpp
// 使用顶级头 也可以使用模块头 #include <opencv2/imgproc.hpp>等
#include <opencv2/opencv.hpp>
using namespace cv;
```
## 常用模块的操作
### 核心模块 `core` 
#### (1). 数据结构 `cv::Mat` 
`cv::Mat` 是 `OpenCV` 最核心的图像容器，内部封装了图像的像素值、通道数、数据类型等常用信息。
##### (i). 创建
```cpp
Mat img1;    // 空图像
Mat img2(640, 480, CV_8U, Scalar(0,0,255));    // 创建红色图像
Mat img3 = imread("image3.jpg", IMREAD_COLOR);    // 读取图像
```
数据类型：通用格式为 `CV_[位数][符号][类型]C[通道数]` 
- `CV_8U` （8位无符号类型）、 `CV_8UC3` （3通道8位无符号类型）
- `CV_32F` （32位浮点类型）、`CV_64F` （64位浮点类型）
**注意**：`Mat` 的彩色图通道为 `BGR` 而不是 `RGB` ，所以一般在与其他库结合使用的时候需要注意转换。
##### (ii). 常用操作
```cpp
image.rows    // 行像素长度
image.rows    // 行像素长度
image.channels()    // 通道数
image.at<Vec3b>(y, x); // 访问(x, y)处的像素值
```
#### (2). 标准化 `cv::normalize` 
```cpp
void normalize(InputArray src, OutputArray dst, double alpha, double beta, int norm_type=NORM_L2, int dtype=-1, InputArray mask=noArray());
```
- `src`：输入矩阵或图像，可以是 `cv::Mat`、`cv::UMat`、`std::vector<float>` 等。
- `dst`：输出矩阵或图像，可以与 `src` 相同，也可不同，取决于 `dtype` 的设置。
- `alpha`：与 `norm_type` 模式有关。当模式是归一化类型 `NORM_MINMAX` 时，`alpha` 是归一化后的最小值；当模式是向量范数 `NORM_L2` 时，`alpha` 是归一化后的范数值。
- `beta`：也与 `norm_type` 模式有关。当模式是归一化类型 `NORM_MINMAX` 时，`beta` 是归一化后的最大值；当是其他模式时，`beta` 被忽略，无意义。
- `norm_type`：常见取值有 `NORM_INF` 无穷范数、`NORM_L1` L1范数、`NORM_L2` L2范数、`NORM_MINMAX` 映射到 `[alpha, beta]` 。
- `dtype`：输出的目标类型，如 `CV_32F`、`CV_8U` 等，默认 `-1` 表示与输入类型一致。
- `mask`：用于指定归一化的区域，只对 mask 中为 `1` 的元素进行归一化（不常用）。

### 图像 `I/O` 与显示 `highgui` 
- `imread`：读取图像；
- `imwrite`：保存图像；
- `imshow`：显示窗口。
### 图像处理 `imgproc` 
#### (1). 色彩空间转换
```cpp
// 色彩空间转换，src、dst 意义同上
cvtColor(src, dst, COLOR_BGR2GRAY)
```
#### (2). 阈值处理
把像素值根据阈值条件转换为两类或多类，实现二值化或截断等效果。用于图像二值化、像素筛选、简单分割、去噪（如 Otsu、自适应阈值）等。
```cpp
double threshold(cv::InputArray src, cv::OutputArray dst,
double thresh, double maxval, int type)
```
- `src`：输入图像通常要求单通道（灰度图），但也可以对每个通道独立处理多通道 Mat 。
- `thresh`：阈值。含义取决于 `type` 的设置。
- `maxval`：含义取决于 `type` 的设置。当是典型二值化 `THRESH_BINARY` 时，`maxval` 是大于阈值是输出的值；当是翻转二值化 `THRESH_BINARY_INV` 时，与 `THRESH_BINARY` 相反，`maxval` 是小于阈值输出的值；当是 `THRESH_OTSU`、`THRESH_TRIANGLE` 模式时，`maxval` 仍作为域上限使用。
- `type`：阈值方法。具体如下：

| type              | 效果说明                         |
| ----------------- | ---------------------------- |
| THRESH_BINARY     | src > thresh → maxval，否则 0   |
| THRESH_BINARY_INV | src > thresh → 0，否则 maxval   |
| THRESH_TRUNC      | src > thresh → thresh，否则保持原值 |
| THRESH_TOZERO     | src > thresh → 原值，否则 0       |
| THRESH_TOZERO_INV | src > thresh → 0，否则原值        |
| THRESH_OTSU       | 忽略传入 thresh，由算法自动选           |
| THRESH_TRIANGLE   | 同上，自动选 thresh                |
#### (3). 滤波（以高斯滤波为例）
```cpp
void GaussianBlur(src, dst, ksize, sigmaX, sigmaY, borderType);
```
- `ksize`：滤波器高斯核大小 `Size(5, 5)`，核大小越大，模糊效果越强。
- `sigmaX`：高斯函数在 `X` 方向的标准差值，决定了 `X` 方向上的模糊程度，若设置为 0 ，会根据核大小自动计算合适的值。
- `sigmaY`：高斯函数在 `Y` 方向的标准差值，决定了 `Y` 方向上的模糊程度，默认为 0，表示与 `sigmaY` 一致。
- `borderType`：指定滤波器核在边界的处理方法。
	- `BORDER_CONSTANT`: 用常数填充边界像素。
	- `BORDER_REPLICATE`: 重复边界像素。
	- `BORDER_REFLECT`: 反射边界。
	- `BORDER_WRAP`: 用对面图像的像素填充边界。
	- `BORDER_DEFAULT` 默认使用 `BORDER_REFLECT_101`。
#### (4). 边缘检测（以 `Sobel` 算子为例）
```cpp
void Sobel(src, dst, ddepth, dx, dy, ksize, scale, delta, borderType);
```
- `ddepth`：输出图像的类型，即 `CV_8U` 等。
- `dx`：计算 `x` 方向导数的阶数， `1` 表示一阶导数，`0` 表示不计算 `x` 方向的导数。
- `dy`：计算 `y` 方向导数的阶数，参数与上类似。
- `ksize`：`Sobel` 核的大小，必须为奇数，默认值为 `3` 。
- `scale`：缩放导数的结果，默认为 `1` 即为不缩放。
- `delta`：`Sobel` 核的大小，必须为奇数，默认值为 `0` 即为不进行偏移。
- `borderType`：边界扩展类型，边界的处理方法，同上。
#### (5). 检测与绘制轮廓
##### (i). 检测轮廓
```cpp
void cv::findContours(InputOutputArray image, std::vector<std::vector<cv::Point>>& contours, std::vector<cv::Vec4i>& hierarchy, int mode, int method, Point offset = Point());
```
- `image`：输入/输出图像，`cv::findContours` 会修改图像，通常会先克隆一份。
- `contours`：轮廓点集合，每条轮廓是一组点的 vector 。
- `hierarchy`：层级关系。每个轮廓有四个参数 `[next, previous, first_child, parent]` 。
- `mode`：轮廓检索模式。常用 `RETR_EXTERNAL`（只检索最外层轮廓）、`RETR_LIST`（检索所有轮廓，不建立层级关系）、`RETR_CCOMP`（检索所有轮廓，建立两层层级关系）、`RETR_TREE`（检索所有轮廓，建立完整层级结构）。
- `mothod`：轮廓逼近方法。常用值 `CHAIN_APPROX_NONE`（所有点都存储）、`CHAIN_APPROX_SIMPLE`（压缩水平/垂直/对角线点，只保留端点，常用）、`CHAIN_APPROX_TC89_L1 / TC89_KCOS`（Teh-Chin 链逼近算法）。
- `offset`：可选偏移量，会对输出的每个轮廓点加上 offset，用于多 ROI 情况下，方便映射回原图坐标。
##### (ii). 绘制轮廓
```cpp
void cv::drawContours(InputOutputArray image, const std::vector<std::vector<cv::Point>>& contours, int contourIdx, const cv::Scalar& color, int thickness = 1, int lineType = LINE_8, const std::vector<cv::Vec4i>& hierarchy = std::vector<cv::Vec4i>(), int maxLevel = INT_MAX, cv::Point offset = cv::Point());
```
- `contourIdx` ：指定绘制哪条轮廓，`-1` 表示绘制所有轮廓。
- `color`：绘制颜色，`cv::Scalar(B,G,R)` 或灰度值（单值）。
- `thickness`：线宽（像素），`<0` 或 `FILLED` 表示填充轮廓。
- `lineType`：绘制线型。常用 `LINE_8`（8-connected）、`LINE_4`（4-connected）、`LINE_AA`（抗锯齿线）。

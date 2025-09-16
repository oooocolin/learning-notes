---
title: OpenCV-C++
tags:
  - cxx
  - opencv
---
## 一、概述
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
## 二、安装与配置
### 1. 安装 `OpenCV`
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
### 2. `CMake` 项目配置
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
### 3. 导入内容
在需要使用的源文件导入头文件，可以选择使用命名空间简化模块的使用。
```cpp
// 使用顶级头 也可以使用模块头 #include <opencv2/imgproc.hpp>等
#include <opencv2/opencv.hpp>
using namespace cv;
```
## 三、常用模块的操作
### 1. 核心数据结构 `cv::Mat` 
`cv::Mat` 是 `OpenCV` 最核心的图像容器，内部封装了图像的像素值、通道数、数据类型等常用信息。
#### (1). 创建
```cpp
Mat img1;    // 空图像
Mat img2(640, 480, CV_8U, Scalar(0,0,255));    // 创建红色图像
Mat img3 = imread("image3.jpg", IMREAD_COLOR);    // 读取图像
```
数据类型：通用格式为 `CV_[位数][符号][类型]C[通道数]` 
- `CV_8U` （8位无符号类型）、 `CV_8UC3` （3通道8位无符号类型）
- `CV_32F` （32位浮点类型）、`CV_64F` （64位浮点类型）
**注意**：`Mat` 的彩色图通道为 `BGR` 而不是 `RGB` ，所以一般在与其他库结合使用的时候需要注意转换。
#### (2). 常用操作
```cpp
image.rows    // 行像素长度
image.rows    // 行像素长度
image.channels()    // 通道数
image.at<Vec3b>(y, x); // 访问(x, y)处的像素值
```
### 2. 图像 `I/O` 与显示 `highgui` 
- `imread`：读取图像；
- `imwrite`：保存图像；
- `imshow`：显示窗口。
### 3. 图像处理 `imgproc` 
#### (1). 色彩空间转换
```cpp
// 色彩空间转换，其中 src 为原图像， dst 为转换目的图像
cvtColor(src, dst, COLOR_BGR2GRAY)
```
#### (2). 滤波（以高斯滤波为例）
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
#### (3). 边缘检测（以 `Sobel` 算子为例）
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


---
title: OpenCV-C++
tags:
  - cxx
  - opencv
---
## 一、安装与配置
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








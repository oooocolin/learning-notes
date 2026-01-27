---
title: Python 项目规范
tags:
  - python
  - standard
---
## 项目文件的结构
一般的 Python 项目在较小的时候都是堆放在一个项目文件夹内的，没有模块分层、没有明确职责的划分等，不利于管理日渐复杂的项目工程。一般常用或常见的是 `flat layout` 和 `src layout` 两种项目结构。
### `flat layout` 
扁平布局 `flat layout` 将主代码包直接位于项目根目录下，项目模块与配置文件、测试文件等平级，结构相对简单直接，导入路径相对简洁，直接从包名开始 `from package_name import module1` ，更适合简单快速、部署相对简单的项目（`flat layout` 使用 `pytest` ，在 `site-packages` 没找到内容时，会根据 `import` 将 `package-name` 本地源码载入 `sys.path` 造成安装）。
```
project-name/
├── README.md
├── requirements.txt
├── environment.yml
├── .gitignore
├── setup.py
├── pyproject.toml
├── docs/
├── tests/
│   └── test_main.py
└── package-name/
	├── __init__.py
	├── main.py
	├── utils.py
	├── modules/
	│   ├── __init__.py
	│   └── xxx_module.py
	└── services/
        └── xxx_service.py
```
### `src layout` 
src 布局 `src layout` 将项目源代码放在一个 `src` 目录之下，将项目模块与配置文件、测试文件区隔开来，使得项目结构更为清晰，也更适合复杂部署测试的大型项目。
```
project-name/
├── README.md
├── requirements.txt
├── environment.yml
├── .gitignore
├── setup.py
├── pyproject.toml
├── docs/
├── tests/
│   └── test_main.py
└── src
	└──package-name/
		├── __init__.py
		├── main.py
		├── utils.py
		├── modules/
		│   ├── __init__.py
		│   └── xxx_module.py
		└── services/
	        └── xxx_service.py
```
### 注意
在工程中常见到 `__init__.py` 、`__main__.py` 、`run.py` 等文件。

对于 `__init__.py` 而言，最早是为了使得目录能被 Python 识别为一个包，使得 Python 能通过 `import package-name` 导入其中的模块（在 Python 3.3 之后无需这个文件也能识别为 Python 包）。并且若在 `__init__.py` 导入模块 `from .modules.xxx_module import func1` ，就能使得导入包 `import package-name` 后，用户就可以直接在顶层 `package-name.func1()` 调用。换句话说，`__init__.py` 更像提供一个显式 API 界面，而不是进行访问控制。

`__main__.py` 是为了让整个包可执行，使得进行命令行操作 `python -m package-name` 能够执行，如果没有这个文件就会报错。但这个不是必须的只有在需要包可执行的时候需要它，或是只是想导入，又或是可以使用 `run.py` 启动。

`run.py` 文件通常是项目单独的启动脚本，一般是放在项目目录而不是模块目录。此文件一般是用于内部开发调试使用，而 `__main__.py` 更偏向标准入口，一般用于发布的工具库。但两者并不直接冲突，开源项目通常两者都有。如果是内部使用可能跟偏向 `run.py` ，因为发布和命令执行不是首要要求，而且 `run.py` 更为灵活。
```
myproject/
│
├── mypackage/
│   ├── __init__.py       # 包初始化
│   ├── __main__.py       # 包执行入口
│   ├── module1.py
│   └── module2.py
│
├── run.py                # 开发/调试启动
├── requirements.txt
└── setup.py
```

对于 `setup.py` 文件，是此前打包和安装依赖的文件。而现代使用 UV 、Poetry 通过 `pyproject.toml` 进行管理，这里不做详细说明，而是简易说明。
## 包管理工具、虚拟环境与构建工具
一般 Python 默认使用 `pip` 来进行包管理，并且推荐 `venv` 作为隔离的虚拟环境工具，但在一些场景，`anaconda` 、 `miniconda` 等使用更为广泛。
### 包管理工具与虚拟环境
#### (1). `pip` 
官方支持的包管理工具，使用更为方便，但是本身没有虚拟环境对各种包做隔离，一般在虚拟环境中配合使用。
- 安装包：`pip install pkg-name` 
- 卸载包：`pip uninstall pkg-name` 
#### (2). Venv
##### (i). 概述
官方支持的虚拟环境，一般与项目直接挂钩，直接在当前项目生成 `venv` 或是 `.venv` 文件夹（后面以 `.venv` 为准），在一般是激活后配合 `pip` 使用。
##### (ii). 常用  `venv` 命令
- 创建虚拟环境：`python -m venv .venv` 
- 激活虚拟环境：
	- Windows 平台：`.venv\Scripts\activate` （先到项目文件内再使用命令行）
	- Linux/macOS 平台：`source myenv/bin/activate` 
- 关闭虚拟环境：
	- Windows 平台：`.venv\Scripts\deactivate` 
	- Linux/macOS 平台同理
- 导出虚拟环境 `pip` 包信息：`pip freeze > requirements.txt` 
- 导入虚拟环境 `pip` 包信息：`pip install -r requirements.txt` 
##### (iii). `pyproject.toml` 配置文件
一般导出 `requirements.txt` 分享给他人使用，但是由于 `pip` 自身并不管理依赖，所以卸载的时候只会卸载本身，这就会使得我们在多次使用 `pip uninstall` 后将造成项目残留无用的依赖包一并被导出，这一般依靠 `pyproject.toml` 解决，也是官方指定的统一的配置文件。  其基本结构也很简单：
```toml
[project]
name = "proj"
version = "0.1.0"
dependencies= [
	"numpy==2.3.3"
]
```
安装时使用 `pip install .` 或是 `pip install -e .` (防止将源代码也安装到虚拟环境里，造成每次执行都得重新安装依赖)，其基本流程是将当前文件夹打包成安装包，再安装入虚拟环境。  
**注意**：
- 但是这也带来了一个问题，`pyproject.toml` 配置文件需要自己手动去写依赖的包以及版本，而这需要使用 Poetry 、 UV 、PDM 这些包管理工具实现了。  
- 在一些项目中，还存在 `setup.py` 文件，这是在 `pyproject.toml` 之前配置项目使用的，目前仍作为包含 C/C++ 扩展的补充配置部分。
#### (3). Conda
##### (i). 概述
在数据科学领域更为广泛使用的包管理工具和虚拟环境工具，使用 `conda` 命令进行包管理和虚拟环境管理。Anaconda、Miniconda、Conda-forge、Miniforge、Mamba 都是基于此套生态的工具或包仓库。
##### (ii). 常用 `conda` 命令：
- 查看虚拟环境列表：`conda env list` 
- 创建虚拟环境：`conda create -n env-name` 
- 激活虚拟环境：`conda activate env-name` 
- 退出虚拟环境：`conda deactivate` 
- 移除虚拟环境：`conda env remove --name env-name` 
- 安装包：`conda install pkg-name` （默认使用 `default channel` 来源的包）
- 卸载包：`conda uninstall pkg-name` 
- 查询镜像包版本：`conda search pkg-name` 
- 导出 `conda` 虚拟环境信息：`conda env export > environment.yml` 
- 导入 `conda` 虚拟环境信息：`conda env create -f environment.yml` 
##### (iii). Conda 衍生生态
- 如果要使用 Conda-forge 来源的包可以使用 `conda create -n env-name -c conda-forge` 创建虚拟环境，以及使用 `conda install -c conda-forge pkg-name` ，或是修改默认配置以及使用 Miniforge 使得默认使用 Conda-forge 内的包。
- Mamba 是基于 Conda 生态将 `conda` 命令工具使用 C++ 重新实现并实现多线程下载的包管理工具，在下载方面更为快速，更适合大量的包管理下载，并且兼容 `conda` 命令，只需将命令的 `conda` 改为 `mamba` 即可，并且默认包含在 Miniforge 安装包内，无需额外安装。
#### (4). UV
UV 、 Poetry 这类包管理工具从底层依然是使用 `pip` 和 `venv` ，但提供了更为简单的接口方便用户使用，会自动在 `pyproject.toml` 配置文件内添加依赖信息，并创建虚拟环境，把对应依赖安装进环境。UV 为例，默认初始只需要建立最基本的结构的 `pyproject.toml` 配置文件，即可开始。
- 添加依赖：`uv add pkg-name` 
- 添加依赖，但是禁止从源码构建只允许预编译的目标包：`uv add pkg-name --no-build` 
- 跳过依赖只安装包文件：`uv pip install pkg-name` 
- 读取 `pyproject.toml` 配置文件：`uv sync` 
- 执行代码（无需手动激活环境）：`uv run main.py` 
#### (5). Pixi
近期新兴的包管理工具，可兼容 Conda 生态。
### 构建工具
Conda 的打包的 `.conda` 文件只能用于 Conda 生态，一般是用于上传到 channel 上，除此之外一般选择使用 UV、Poetry 此类打包为更轻量更易分享使用的 `.whl` 文件，可以兼容 `pip` 生态和 `conda` 生态。以下主要说的是 `.whl` 的打包和构建。  
Python 的构建系统拆解为 frontend 和 backend ，用户使用命令行操作属于 frontend ，frontend  自行调用 backend 将代码打包成 `.whl` 文件。官方推荐的 frontend 为 `build` ，其默认使用的 backend 为 `setuptools` ，也可自行选择 UV、hatchling、LIT、Poetry 等第三方实现进行构建操作，他们之中有些只实现 frontend 和 backend 中的一个，有的都完成了实现。以下使用 `build` 和 `hatchling` 实现构建:
- 在 `pyproject.toml` 配置 backend 为 `hatchling` ：
```toml
[build-system]  
requires = ["hatchling"]  
build-backend = "hatchling.build"
```
- 在 `pyproject.toml` 配置 `build` 需要打包的文件：
```toml
[tool.hatch.build.target.wheel]  
packages = ["main.py"]
```
- 执行打包命令 `python -m build` (若想用 UV 来执行打包可以使用 `uv build` ，其速度更快)
**注意**：
- hatchling 需要在打包文件夹内需要存在 `__init__.py` 文件，不添加无法顺利完成打包。
- 在以上的流程完成后就已经实现了打包，但是在实际的项目开发中，一般还需要将打包的代码安装到虚拟环境中，方便后续的测试等流程，需要执行 `pip install -e ` ，或是 `uv sync` 。


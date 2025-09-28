---
title: Python 项目规范
tags:
  - python
  - standard
---
## 一、项目文件的结构
一般的 Python 项目在较小的时候都是堆放在一个项目文件夹内的，没有模块分层、没有明确职责的划分等，不利于管理日渐复杂的项目工程。一般常用或常见的是 `flat layout` 和 `src layout` 两种项目结构。
### 1. `flat layout` 
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
### 2. `src layout` 
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
## 二、包管理工具、虚拟环境与构建工具
一般 Python 默认使用 `pip` 来进行包管理，并且推荐 `venv` 作为隔离的虚拟环境工具，但在一些场景，`anaconda` 、 `miniconda` 等使用更为广泛。
### 1. 包管理工具
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
但是这也带来了一个问题，`pyproject.toml` 配置文件需要自己手动去写依赖的包以及版本，而这需要使用 Poetry 、 UV 、PDM 这些包管理工具实现了。
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

#### (5). Pixi
近期新兴的包管理工具，可兼容 Conda 生态。


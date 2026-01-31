---
title: Python 文件处理
tags:
  - python
  - file-handing
---
## 文件的基本操作
### 打开关闭文件
`open()` 函数可用来打开文件，需要配合 `file.close()` 关闭文件释放资源。一般配合 `with ... as ...` 进行上下文管理，释放资源更安全。
```python
with open('example.txt', 'r') as file: 
	file_content = file.read()
	print(file_content)
```
访问模式常见如下：

| 模式   | 说明                                     |
| ---- | -------------------------------------- |
| `r`  | 只读模式，文件必须存在                            |
| `w`  | 只写模式，文件存在则清空后写入，不存在则创建                 |
| `a`  | 追加写入，文件存在则末尾追加，不存在则创建                  |
| `x`  | 独占创建写入，文件必须不存在，存在则报错                   |
| `r+` | 读写组合，文件必须存在，会在开头覆盖当前位置内容               |
| `w+` | 读写组合，文件存在则清空后写入，不存在则创建                 |
| `a+` | 读写追加，文件存在写入只在末尾，不存在则创建，读取需要先 `seek(0)` |
| `x+` | 独占创建读写，文件必须不存在，存在则报错                   |
| ...  | ...                                    |
### 读写文件
使用 `open()` 函数打开文件后可以对文件进行读写。对于写入来说有大致以下几种主要的形式。
- 使用 `file.write("Hello World!")` 写入文本文件。
- 使用 `csv.writer(csvfile)` 写入 CSV 文件。
- 使用 `json.dump(data, jsonfile)` 写入 JSON 文件。
对于读取而言，有以下几种形式。
- 使用 `file.read()` 读取文件内容。
- 使用 `csv.reader(csvfile)` 读取 CSV 文件内容。
- 使用 `json.load(jsonfile)` 读取 JSON 文件内容。
- 使用 `file.readline()` 以文件逐行读取文件内容。
- 使用 `file.readlines()` 以文件以行读取文件所有内容。
### 重命名文件名
Python 使用 `os.rename(full_path, new_name_path)` 对文件进行重命名。
### 创建目录
| 功能                     | 说明            |
| ---------------------- | ------------- |
| `os.mkdir()`           | 创建一个子目录       |
| `pathlib.Path.mkdir()` | 创建单个或多个目录     |
| `os.makedirs()`        | 创建多个目录，包括中间目录 |
如果目录存在，则会引发异常。可以通过捕获异常，或是设置 `pathlib` 对象的 `p.mkdir(exist_ok=True)` 的参数来忽略这个已存在的目录。
## 获取目录
```
my_directory/
│
├── sub_dir/
│   ├── bar.py
│   └── foo.py
│
├── file1.py
├── file2.csv
└── file3.txt
```
### 旧版 Python 获取列表
在 Python 3 之前的版本，可以使用 `os.listdir("my_directory/")` 获取目录列表。结果返回一个 Python 列表，其中包含由路径参数指定的目录中的文件和子目录的名称。
```
['file1.py', 'file3.txt', 'file2.csv', 'sub_dir']
```
### 现代 Python 获取列表
现代 Python 仍可以使用 `os.listdir()` 函数，但该函数在每个文件都会进行一次 `stat` 的系统调用，导致性能比较差。现代更推荐使用 `os.scandir()` 函数或是 `pathlib.Path()` ，在一次读取中无论内含多少文件都是只进行一次 `stat` 系统调用。而且这两种方法都支持更为集中方便地获取文件名、后缀、地址等衍生信息获取。
#### (1). `os.scandir()` 
`os.scandir()` 该函数在 Python 3.5 中引入。调用该函数时，它返回的是一个迭代器而不是列表。
```python
with os.scandir('my_directory/') as entries:
    for entry in entries:
        print(entry.name)
```
#### (2). `pathlib.Path()` 
`pathlib` 库本质上也是基于 `os.scandir()` ，但对其进行内部的资源管理，无需手动释放或是 `with` 上下文管理，所以更为推荐使用。
```python
entries = pathlib.Path('my_directory/')
for entry in entries.iterdir():
    print(entry.name)
```

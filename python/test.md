---
title: Python 测试
tags:
  - python
  - test
---
## 概述
Python 的测试库一般有两种，一个是官方标准库里的 `uinttest` ；另一个是更为精简强大的 `pytest` 。
## `unittest` 
### 简介
`uinttest` 类似于 Java 的 Junit 风格，但工程上一般很少主动选择使用 `uinttest` ，因为有更为强大的 `pytest` 。但 `uinttest` 是 Python 测试的基础，也是举足轻重的部分。
### 实现
```python
import unittest

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

if __name__ == '__main__':
    unittest.main()
```
代码中没有直接调用测试函数 `test_somthing` 却能进行测试。这是因为 `uinttest` 在 `uinttest.main()` 方法中使用 TestLoader 对当前模块进行扫描找出所有继承 `unittest.TestCase` 的类中所有以 `test_` 为开头的类方法。都将其包装为 TestSuite ，这就相当于一个测试队列，里面包含一个或多个 TestCase 实例，`unittest.main()` 方法中对这个队列执行 `run()` 方法。
### `setUp()` 与 `setUpClass()` 
`setUp()` 与 `setUpClass()` 是 `uinttest` 用于进行测试执行前执行的钩子方法。`setUp()` 方法会在进行每一次测试之前执行，一般用于在每次测试前清空属性的初始状态。`setUpClass()` 必须配合 `@classmethod` 装饰器配合使用，设置为类方法，这样就实现了在进行整体的测试前执行一次的效果（不加 `@classmethod` 装饰器将会报错）。
## `pytest` 
### 简介
`pytest` 是一个更为易用的 Python 测试框架。使用前需安装 `pip install pytest` 。
### 实现
```python
def test_sum():
    assert sum([1, 2, 3]) == 6
```
`pytest` 直接使用 `assert` 语言机制的断言就不用去了解各种 `self.assert*()` 的方法。但也对文件和书写提出一定要求。
- 模块中以 `test_` 为开头的函数会被识别为测试函数。
- 类以 `Test` 开头，类内方法以 `test_` 开头，即能识别为测试类及方法。
- 文件必须以 `test_` 开始或 `_test` 结尾，在执行的时候才能正常启动测试。
### `@pytest.fixture` 
`@pytest.fixture` 装饰器用作在对 `pytest` 测试函数的入参进行注入。这要求测试函数的入参和准备注入的函数名称保持一致。该装饰器可以使多个测试函数共用一个 fixture 。所以这个装饰器的作用一般是在设定公共依赖或是默认值作为代码可正常运行的最小支持而存在（不应作为测试样例注入使用）。
```python
import pytest

@pytest.fixture(scope="module")
def sample_data():
    return {"name": "Alice", "age": 18}

def test_sample(sample_data):
    assert sample_data["age"] == 18
```
并且可以设置其作用域，可指定其生命周期，有 `function`、`class`、`module` 或 `session` 。
- `function`：默认作用域，会在每一个测试函数执行前调用。
- `class`：在同一个测试类内共享一个 fixture 实例，在不同类之间重新调用。
- `module`：同一个模块内共享，每个模块调用一次。
- `package`：`pytest` 大于等于 6.0 版本支持，在同一个Python 包（有 `__init__.py`）内共享。
- `session`：整个 `pytest` 运行周期值创建一次，所有测试共享。
fixture还可以被参数化，这意味着它们可以用不同的参数多次执行，从而为测试提供不同的环境。这是通过给 `@pytest.fixture` 装饰器添加 `params` 参数来实现的。
```python
@pytest.fixture(params=[1, 2, 3])
def param_fixture(request):
	return request.param
```

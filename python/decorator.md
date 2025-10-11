---
title: 装饰器
tags:
  - python
  - decorator
---
### 一、概述
装饰器（decorators）是基于装饰器设计模式实现的一个高级功能，它可以实现动态修改和扩展函数和类的行为的操作。本质上就是一个闭包函数，接收一个函数或类作为参数，进行修改和添加后返回一个新的函数或类的操作。常见用于日志记录、权限验证、缓存结果、性能测试、事务管理等场景。
## 二、基本语法
常见的用 `@` 符号来使用装饰器的方式其实是相关操作的一个语法糖，本质上就是将作用的函数作为参数输入到装饰器这个闭包函数，并且执行这个闭包函数。
```python
def log_decorator(func):
    def log_inner(*args, **kwargs):
        print("方法调用前")
        result = func(*args, **kwargs)
        print("方法调用后")
        return result
    return log_inner


# 传统操作视角
def test(content):
    print(content)

# 将要装饰的函数作为参数传入
t = log_decorator(test)
# 调用
t("hello world")


# 语法糖，更为方便的写法
@log_decorator
def test(content):
    print(content)

test("hello world")
```
装饰函数（外包函数）只能有一个参数，内部函数没有要求，一般与装饰函数的参数一致。
## 三、装饰器的延伸
### 1. 多装饰器的使用
多装饰器其实是就是多层闭包的实现，以传统视角来看就是层层闭包，由内向外装饰，按照离函数的远近为先后顺序，越靠近函数定义越先被装饰。
```python
@log_decorator
@cache_decorator
def test(content):
    print(content)
```
这里的就是先执行 `@cache_decorator` 装饰器，后是 `@log_decorator` 装饰器。
### 2. 带参数的装饰器
装饰器本身也可以接收参数，只需要在结构上多实现一层闭包即可
```python
def log_param_decorator(n)
	def log_decorator(func):
	    def log_inner(*args, **kwargs):
	        print("方法调用前")
	        result = func(*args, **kwargs)
	        print("方法调用后")
	        return result
	    return log_inner
	return log_decorator

@log_param_decorator(2)
def test(content):
    print(content)
```
本质上上是执行 `log_param_decorator(3)(test)` 操作。
### 3. 类装饰器
类装饰器是用于动态修改类行为的装饰器，可以用于添加或修改类的方法或属性、拦截实例化过程、实现单例模式、日志记录、权限检查等功能。
#### (1). 函数式类装饰器
本质上就是接收类对象，最后返回类对象的装饰器，其形式与函数装饰器类似。
```python
def log_decorator(cls):
    """类装饰器：自动为类中所有方法添加日志功能"""
	
    # 遍历类的所有属性
    for attr_name, attr_value in cls.__dict__.items():
        # 只处理可调用的（方法），并且排除特殊方法（如 __init__、__repr__ 等）
        if callable(attr_value) and not attr_name.startswith("__"):
            original_method = attr_value  # 原方法的引用
			
            # 定义一个新的包装函数
            def wrapped(self, *args, __method=original_method, **kwargs):
                print(f"[LOG] Calling {__method.__name__} with args={args}, kwargs={kwargs}")
                result = __method(self, *args, **kwargs)
                print(f"[LOG] {__method.__name__} returned: {result}")
                return result
			
            # 替换原方法
            setattr(cls, attr_name, wrapped)
	
    return cls

@log_decorator
class MyClass:
    def greet(self, name):
        return f"Hello, {name}!"
```
或者可以简易只装饰类的某一些方法，但是在日常开发中不常见，更多的还是期望对类进行更泛化的操作。
#### (2). 类式类装饰器
除了函数形式的类装饰器也可实现类形式的类装饰器，只需实现 `__call__` 方法（原因参考 [Python 细碎知识](python-fragmented-notes.md) ）。
```python
class CountInstances:
	"""统计实例化次数"""
	
    def __init__(self, cls):
        self.cls = cls
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.cls.__name__} created {self.count} times")
        return self.cls(*args, **kwargs)

@CountInstances
class Foo:
    pass

a = Foo()
b = Foo()
# Foo created 1 times
# Foo created 2 times
```
### 4. 内置装饰器
Python 提供了一些内置的装饰器提供用户调用，加快编程效率，例如：
- `@staticmethod`：将方法定义为静态方法，不需要实例化类即可调用。
- `@classmethod`：将方法定义为类方法，第一个参数是类本身（通常命名为 `cls`）。
- `@property`：将方法转换为属性，使其可以像属性一样访问。
**注意**：`@staticmethod` 和 `@classmethod` 的区别仅是有没有接收类本身作为参数，他们本质上是一致的，都是类方法（或是静态方法）。
## 四、总结
装饰器本质上就是将原有函数或类作为入参，包装成一个新的闭包，再执行的过程。常见的 `@` 符号作为语法糖，将 `@something` 类似的结构自动翻译为 `func_new = something(func)` 结构，并在调用的时候转而实际调用新的闭包。所以理论上来说，只要满足以上对应关系就可以实现这个语法糖，也就会说可调用对象都可以作为装饰器。  
对于其他语言可以看到类似结构作用于类属性的方式，比如 Java 等，但是 Python 不允许这样的行为，因为属性本身平常出现的形式是赋值语句内，这个无法作为输入，自然无法实现，但是可以使用 [描述符](descriptor.md) 来接管属性的行为，做到类似的效果。


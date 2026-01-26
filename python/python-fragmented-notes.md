---
title: Python 的一些细碎知识
tags:
  - python
---
## package、module 与 import 
### 模块（Module）
一个模块就是一个 Python 文件。每个模块定义自己的命名空间，可包含变量、函数、类等。使用 `import` 完成导入，导入后以 Module 类的对象存在，所以一般来说无需在自定义类里面设置静态方法，可直接用函数实现，因为在使用中模块内的函数就是本身这个模块的方法。  
一般导入后可用 `import xxxx as xx` 简写模块名称，这实际上是 `xx = xxxx` 的一个语法糖。
### 包（Package）
包是包含 `__init__.py` 文件的目录，同时只有含有 `__init__.py` 文件的目录才能被识别为包。该文件可初始化包环境，控制模块导入行为。一般使用 `from pkg import xxxx` 完成导入。
## Python 的数据模型
### 可变对象和不可变对象
可变对象是指创建后可以改变其内容的对象，不可变对象是指创建后不可以被修改的对象。常见类型以下：
- 可变对象：列表（`list`）、字典（`dist`）、集合（`set`）
- 不可变对象：元组（`tuple`）、字符串（`str`）、整数和浮点数（`int`、`float`）
Python自定义的类对象默认都是可变的，其判断依据是使用 `id()` 函数判断地址是否改变；若想设置为不可变需要特殊设计（使用 `__slots__` 和重写 `__setattr__`或是使用 `@dataclass(frozen=True)`）
### 魔术方法（特殊方法）
魔术方法的一般形式为命名被双下划线包围 `__xxx__` ，该方法是由解释器在特定时机调用，一般是为了能使类直接使用运算符、内置函数等操作。常见魔术方法如下：
- `__new__(cls, ...)`：创建对象实例（先于 `__init__`），一般用于创建单例模式等。
- `__init__(self, ...)`：构造函数，设置属性。
- `__str__(self)`：设置用户友好的字符串输出，常用在 `print(obj)` 执行时调用。
- `__call__(self)`：定义对象被调用时的行为，允许一个类的实例像函数一样被调用。
除了特殊方法外，还存在特殊属性，其形式与魔术方法类似，都是命名被双下划线包围。通常是只读的属性，提供对象的内省信息。
- `__doc__`：访问文件的文档字符串，获取开发者编写的文档注释内容。
- `__class__`：访问实例对象的类型。
## Python 的函数传参
### 参数传递的形式
函数传递参数的形式主要有以下几种，分为位置传递、关键字传递、默认值传递、不定参数传递（包裹传递）、解包裹传递。
- 位置传递：按照函数定义参数顺序传输参数。
- 关键字传递：根据每个参数的名字使用等号传递参数，关键字并不用遵守位置的对应关系。
- 默认值传递：在函数定义参数时给参数赋予默认值，若传递时没有赋值则使用默认值。
- 包裹传递：函数定义参数时不知道或是不关心调用者会传多少参数，在传递时会将收到的参数打包到一个元组里面。形式上需要在函数声明时将参数前加 `*` 符号。如果要打包为字典的话则需要 `**` 符号，并且得指定关键字。
```python
def func(*param):
	print(param)

func(1, 2, 3)
func(1, 2, 3, 4, 5)
```
- 解包裹传递：与包裹传递相反，传递时不想逐一输入或是不想自己将现有元组元素逐一拆包输入，可以直接将有元素数量同函数参数数量的元组直接传递（传递时需要在元组前加 `*` 符号），Python 会将元组元素自行拆包实现参数传递。如果解包裹对象是字典的话则需要 `**` 符号。
```python

def func(a, b, c):
	print((a, b ,c))

arg = (1, 2, 3)  
func(*arg)
```
**注意**：包裹传递和解包裹传递并不是 Python 所特有，其他语言都有类似机制。比如 TypeScript 语言则是使用 `...` 符号，其转换的对象为数组。
### 传递参数的规则
- 若函数定义参数时在参数前后加入 `*` 符号则意味着 `*` 符号后的参数必须使用关键字传递。
- 可变对象参数在函数内修改外部使用时也会感受到修改，而不可变对象不影响外部。
## 作用域
Python 是动态类型语言，变量在定义时赋值。作用域就是变量活动的空间，变量作用域取决于其定义位置。由此有以下类型：
- 局部变量：定义在函数内部的变量、在函数声明中的形参。
- 全局变量：直接定义在 `.py` 文件内，且不属于文件内函数、类的变量。
- 自由变量：定义在函数内，嵌套函数之外，且被嵌套函数引用的变量。
- 内置变量：定义在 `builtin` 中的变量。
作用域满足 LEGB 规则。LEGB 规则的 LEGB 分别指代四种变量类型，其规则内容是在本地空间找不到的变量会逐级向上寻找。
## 闭包
### 概述
闭包是一种特殊类型的对象，它由一个函数以及创建该函数时存在的作用域中的变量组成。一个函数内部定义了另一个函数，内部函数引用了外部函数的局部变量，外部函数返回了内部函数，这时即使外部函数执行结束，它的局部变量仍然会被内部函数“捕获”并保留下来，这就形成了闭包。
### 代码结构
```python
def outer(x):
    def inner(y):
        return x + y
    return inner

adder = outer(10)
print(adder(5))  # 输出 15
```
### 非局部关键字
在闭包内使用外部变量，如果只是读取变量，Python 会默认从外层作用域查找，但是如果需要在闭包内赋值外部变量的时候读取就会报错。如进行 `x = x + 1` 操作，会把左边赋值理解为创建局部变量，而此时 `x` 已经指定了这个局部变量，所以会被认为是未定义对象（如果是单纯的赋值没有读取的话不报错）。这时需要使用非局部关键字 `nolocal` 来声明这个变量是来源于外部的。
```python
def outer():
    x = 10
    
    def inner_read():
        print(x)  # 读取外层变量，不需要 nonlocal
	
    def inner_write():
        nonlocal x
        x += 5   # 修改外层变量，需要 nonlocal，否则会报错
	
	def inner1():
        x = 5  # 只赋值，不用原来的 x, 使用不报错
        print(x)  # 使用内部局部变量, x = 5 
	
    def inner2():
        x += 1  # 用到了原来的 x，使用将报错
	
    inner_read()
    inner_write()
    print(x)  # 输出 15
```
### 注意
JavaScript 都存在闭包的概念，其基本概念与代码框架是共通的。
```js
function outer(x) {
  return function inner(y) {
    return x + y;
  };
}

const adder = outer(10);
console.log(adder(5)); // 输出 15
```
两者在使用场景上略有区别：
- Python：装饰器的实现、延迟计算、状态保存。
- JavaScript：模块封装、回调状态、异步逻辑。
## Python 的封装
### 总原则
不像是 Java 、C++ 这类面向对象语言的封装是通过访问修饰符进行严格限定，Python 通常通过约定和编程实践来支持封装，期望开发者信任和尊重代码，所以如果强制不使用这些约定在 Python 很容易打破它们。
### 访问修饰符
Python 通常使用命名约定（`_protected`，`__private`）对属性开发者进行提醒，比如命名前一条下划线的属性，就是在提醒用户这个属性强烈不鼓励修改它们，建议只是访问它们；命名前两条下划线的属性，就是在提醒用户这是个私有成员，建议不修改不访问，并且进行一定限制，隐藏了属性的访问方式（但仍可以通过 `_ClassName__name` 来进行访问和赋值）。
### 实现 getter / setter 方法
在一般的 Java 中，如果对属性进行私有类型限制，若仍想有限制地访问，一般会使用 getter / setter 方法。但在 Python 中，这样会显得过于臃肿，而且不符合 Python 的风格。Python 通常使用装饰器来实现 getter / setter 方法。
#### (1). `@property` 装饰器
`@property` 装饰器为属性创建属性，这样就能使得访问私有成员也像访问公开成员一样方便，并且还限制了用户无法通过这种简易的方式修改。
```python
class Tree:
	def __init__(self, height):
	    # First, create a private or protected attribute
	    self.__height = height
	
	@property
	def height(self):
	    return self.__height

pine = Tree(17)
print(pine.height)  # 17
pine.height = 15  # 报错
```
**注意**：`@xxx.getter` 装饰器看起来似乎有着相同的效果，但其实现的前提是必须先使用 `@property` 装饰器来创建只读属性。从本质来说，`@xxx.getter` 装饰器更像是对 `@property` 装饰器的一次重写。一般而言，`@property` 装饰器就已经够用了。
#### (2). `@xxx.setter` 装饰器
`@xxx.setter` 装饰器可用来进行实现 setter 方法，实现有限制的赋值。
```python
class Tree:  
    def __init__(self, height):
        self.__height = height
	
    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, new_height):
        if not isinstance(new_height, int):
            raise TypeError("Tree height must be an integer")
        if 0 < new_height <= 40:
            self.__height = new_height
        else:
            raise ValueError("Invalid height for a pine tree")

pine = Tree(17)
pine.height = 15  # 15
pine.height = 50  # raise ValueError("Invalid height for a pine tree")
```
### 最佳实践
- 如果属性或方法仅供自己使用的话，将其创建为受保护或私有属性或方法。
- 不必为每个类属性都创建 getter / setter 方法。对于拥有大量属性的大型类来说，这会变得非常麻烦。
- 考虑在用户每次访问受保护成员时发出警告。
- 谨慎使用私有成员，因为这会使不熟悉这种约定的人难以理解这种代码。
- 清晰度更重要。封装旨在提高代码的可维护性和数据安全性，不要完全隐藏类的重要实现细节。
- 如果只需只读那就无需实现 `@xxx.setter` 方法。
- 必须始终牢记 Python 的封装只是一种约定，而不是语法层面的强制要求。
- 对于简单类，可以考虑使用数据类（DataClass），实现更为简洁。不过数据类更适合具有可预测属性和方法的简单类。

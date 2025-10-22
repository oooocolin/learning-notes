---
title: 元类
tags:
  - python
  - metaclass
---
## 一、概述
元类是定义类的类。元类允许在类定义时干预类的创建过程，比如修改类属性、方法等。在 Python 中类是对象，元类相当于创建这些对象的类。Python 中内置一个元类 `type` ，所有类的默认元类就是 `type` 。
## 二、基本用法
元类通常继承自 `type` ，并重写以下方法的一个或多个：
- `__new__(cls, name, bases, attrs)`：控制类的创建，返回新对象。
	- `cls`：当前元类自身；
	- `name`：即将创建的类名；
	- `bases`：继承的父类们（元组）；
	- `attrs`：类体中定义的所有属性、方法组成的字典。
- `__init__(cls, name, bases, attrs)`：在类创建后初始化类。
	- `cls`：刚创建好的类对象，其他同上。
```python
# 简易元类实现
class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        print(f"正在创建类: {name}")
        attrs['created_by'] = 'MyMeta'  # 增加一个属性created_by
        return super().__new__(cls, name, bases, attrs)

class MyClass(metaclass=MyMeta):
    pass

print(MyClass.created_by)  # 输出 MyMeta
```
在背后，Python 做了以下操作，元类也实质上是以下操作的语法糖：
- 收集类信息，包括 `cls`、`name`、`bases`、`attrs` 一系列信息；
- 调用元类创建类对象，调用 `__new__(cls, name, bases, attrs)` 方法；
- 调用 `__init__(cls, name, bases, attrs)` 方法初始化类；
- 存储类对象存储到命名空间中。
## 三、使用场景
### 1. 使用场景
元类的本质能力是在类创建阶段干预类的属性和方法。一般有以下使用场景：
- 添加属性和方法。自动注入工具方法、版本号、标记字段。
- 删除或替换属性。过滤掉不符合规范的字段。
- 收集类体中的信息。ORM字段、序列化字段、接口定义等，
- 自动注册类。将新类加入全局注册表或插件表。
但有时候也有其他替代方案，尤其是是其他更为简单的结构也可以考虑：
- 类装饰器：修改类定义，语法更为简单（作用在类定义完成之后，元类作用在类定义的过程中）。
- 继承：通过基类实现代码复用或行为定制。
- 描述器：用于控制属性访问。
### 2. 原则
所以一般在这些条件下选择元类：
- 当需要修改类的创建过程，而不是实例的行为。
- 当逻辑需要应用到多个类，而且无法通过继承和装饰器实现。
- 当开发框架或库需要提供高度抽象的 API 。


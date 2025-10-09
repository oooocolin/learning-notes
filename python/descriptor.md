---
title: 描述符
tags:
  - python
---
## 一、概述
描述符（descriptor）是实现了 `__get__` 、 `__set__` 、 `__delete__` 方法中的一种或者是多种的类。其核心作用是用于拦截属性访问，类似于 TypeScript 的 `get` / `set` 方法的功能，只是在功能上更为灵活。
## 二、语法结构
### 1. 示例 1 （类型验证）
```python
class Typed:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
	
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)
	
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} 必须是 {self.expected_type}")
        instance.__dict__[self.name] = value

class Person:
    name = Typed("name", str)
    age = Typed("age", int)
    
    def __init__(self, name, age):
        self.name = name  # 自动验证类型
        self.age = age
```
### 2. 示例 2 （带控制的缓存属性）
```python
class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, instance, owner):
        cache_attr = f"_cached_{self.name}"
        if not hasattr(instance, cache_attr):
            setattr(instance, cache_attr, self.func(instance))
        return getattr(instance, cache_attr)
    
    def __set__(self, instance, value):
        """允许手动设置缓存值"""
        setattr(instance, f"_cached_{self.name}", value)
    
    def __delete__(self, instance):
        """清除缓存"""
        if hasattr(instance, f"_cached_{self.name}"):
            delattr(instance, f"_cached_{self.name}")
```
### 3. 示例 3（Python 自带的 `@property` 实现方法进行属性的类似操作）
```python
class Person:
    def __init__(self):
        self._age = 0
	    
    @property
    def age(self):
        return self._age
	    
    @age.setter
    def age(self, value):
        if not (0 <= value <= 150):
            raise ValueError("年龄无效")
        self._age = value
```
## 三、局限性和使用场景
### 1. 局限性
- 学习曲线陡峭：概念抽象，初学者难以理解。
- 代码复杂度：简单的属性验证需要较多代码。
- 调试困难：属性访问被拦截，调试时可能不直观。
- 过度工程：简单场景下使用描述符可能显得"杀鸡用牛刀"。
### 2. 使用场景
目前由于主要功能还是对属性进行拦截操作，所以普通业务代码中较少直接使用，只是在一些 Django、SQLAlchemy 等大型框架中使用。并且描述符在很多场景被高级抽象替代，如 @`property`、数据类、第三方库替代，但仍然是 Python 元编程和框架开发的重要工具。


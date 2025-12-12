---
title: C++ 语言概念
tags:
  - cxx
---
语言概念（Language Concepts）通常是指标准层面定义的语义与机制，也就是直属于语言本身的规则、语法和语义约束。
## 类型转换
C++ 中类型转化方法有隐式与显式之分，隐式类型转化由编译器自动进行，基本依照数值范围或元素退化以及多态进行，显式转化由程序员指定，推荐使用四种不同的类型转换方法，加上 C 语言继承的方法共五种显式转化方法。
### `static_cast` 
这是 C++ 中最常用、最安全的类型转换方法。它在编译时执行，当需要显式地转换数据类型时应该使用它。
```cpp
int a = 10;
float b = static_cast<float>(a);
```
### `dynamic_cast` 
这专门用于在类层次结构中安全地转换基类和派生类之间的指针和引用。这种转换会安全地向下转换（base → derived）并检查类型是否兼容。
```cpp
class Base {};
class Derived : public Base {};

Base* base_ptr = new Derived();
Derived* derived_ptr = dynamic_cast<Derived*>(base_ptr);
```
### `const_cast` 
这种类型转换方法用于移除 `const` 变量的限定符以及 `volatile` 。通常不建议使用，但在某些情况下，当您无法控制变量的常量性时，它可能很有用。
```cpp
const int x = 10;
int* p = const_cast<int*>(&x);
```
### `reinterpret_cast` 
这种是推荐的四种转换方法中最危险的转换，进行位级别（bitwise）的重新解释，会改变指针、引用或整数值的类型。用于指针类型之间转换、指针与整数之间转换、将某类型强制解释为另一类型。仅当对所做操作有深刻理解时才应使用，因为它不能保证结果值有意义。
```cpp
int* a = new int(42);
long b = reinterpret_cast<long>(a);
```
### C 风格类型转换
这是从 C 语言继承来的语法，只需将目标数据类型放在要转换的值前面的括号即可，但也是最危险的。这实际中其实就是尝试 `static_cast` 失败后执行 `const_cast` ，再次失败后使用 `reinterpret_cast` ，它隐藏了具体使用的 cast ，是最危险的一种转换方式。
```cpp
int a = 10;
float b = (float)a;
```

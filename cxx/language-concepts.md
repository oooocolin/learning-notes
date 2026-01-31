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
## 未定义行为（UB）
未定义行为（Undefined Behavior, UB）不是一个实现的细节，而是 C++ 语言规范的机制。UB 是指咋程序执行某些操作后，语言校准对结果不起任何作用，也不要求实现做任何的检查或报错。典型的就是空指针解引用、数组越界、除以0等操作，编译器不会作为编译错误，而是在执行时由操作系统或内存等硬件本身的保护触发异常。
```cpp
int *ptr = nullptr;
int val = *ptr; 
```
C++ 这么做是从以下几个方面考虑的：
- 提高性能，让编译器不必去进行各种检测，生成极为高效的代码。
- 兼容硬件性能特性，比如有些 CPU 对整数溢出没有做统一定义。
- 允许编译器避免增加运行时检查成本，如果都进行检查的话 C++ 的性能将不复存在。
这么做也会带来一些问题就是错误直接落到硬件或 OS 层面容易崩溃。与其他语言，如 Java 运行时 JVM 进行安全检查，所以 Java 几乎没有 UB ，要么正确要么抛异常，不会随意崩溃。
## 参数依赖查找（ADL）
ADL（Argument-Dependent Lookup）是指参数依赖查找 ，也叫 Koenig Lookup（柯尼格查找）。它是 C++ 中函数调用名字查找规则的补充机制，就是编译器不仅会在当前作用域查找名字，还会根据实参类型所属于的命名空间，自动查找相应命名空间中的函数。
```cpp
namespace geometry {
    struct Point {};
    void draw(Point);
}

geometry::Point p;
draw(p);
```
**说明**：
- ADL 仅限定义在一个命名空间的函数和对象，若跨命名空间则 ADL 不会作用，比如结构体写在一个命名空间，而方法写在另一个，则查找不到。而且只作用于函数，对于类内部的函数不会进行查找。
- ADL 对普通代码作用有限，如果调用点明确写了命名空间或使用 using namespace，ADL 不会增加好处。ADL 对泛型库和 operator 重载非常关键，STL、Boost、Eigen 等库广泛依赖 ADL 来实现可扩展性和封装。同时 ADL 可能引入二义性，这是设计者需要注意的副作用。
## 符号重整
符号重整（Name Mangling）是编译器对符号名字的改写/编码，目的是让链接器能够区分原本在源代码中名字相同的不同实体。
```cpp
namespace ns {
    void foo(int);
    void foo(double);
}

// 经过 Name Mangling，可能生成的符号
_ZN2ns3fooEi      // foo(int)
_ZN2ns3fooEd      // foo(double)
```
并且不同的编译器重整的风格不同，GCC、Clang、MSVC 都有自己的规则。所以在面对其他语言使用 C++ 的 DLL 无法识别函数名，因为都是 `_ZN2ns3fooEi` 或 `?foo@ns@@YAXH@Z` 的形式而无法调用，只能使用 `extern "C"` 导出 C 风格符号名（详见 [C++ 关键字与符号](keywords-and-symbols.md) 的 `extern` 关键字），即没有这些参数编码来确保正常调用，但是也就限制了不能导出 C++ 特性的接口，比如不能导出模板、命名空间、类（分别导出指针 + 函数，或结构体 + 函数）等。

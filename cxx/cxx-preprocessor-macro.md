---
title: 预处理与宏
tags:
  - cxx
---
## 预处理器
在编译之前，C++会先经过一个预处理阶段（整体流程为 `源码 -> 预处理 -> 编译 -> 汇编 -> 链接 -> 可执行文件` ），实现纯文本替换、条件剪裁、头文件展开的操作，主要由预处理器完成，主要处理的指令如下：
```cpp
#include
#define
#undef
#if #ifdef #ifndef #elif #else #endif
#line
#error
#pragma
```
预处理阶段的本质就只是字符串级别的替换，没有类型检查、没有作用域、不检查语法。
## 宏
### 简述
C++ 宏的本质就是编译前的文本替换规则，基于预处理器进行。也是由于只是进行简单的文本替换，没有类型检查、容易产生运算符优先级错误等所以现代 C++（C++ 11 及以后）更推荐使用 `constexpr`、模板、内联函数等“语言级机制”来取代宏。但宏仍然是比较重要的知识内容。
### 对象宏（常量宏）
```cpp
#define PI 3.1415926
#define MAX_SIZE 1024
```
预处理后作为简单的常量，但现代 C++ 更推荐使用 `constexpr` 定义。
```cpp
constexpr double PI = 3.1415926;
```
### 函数宏（带参数宏）
```cpp
// 错误写法，展开后会变为 x + x * x + x 会优先进行乘法操作
#define SQUARE(x) x * x

// 正确写法，可以正常按照 (x + x) * (x + x) 的顺序进行计算
#define SQUARE(x) ((x) * (x))
```
现代 C++ 更推荐使用 `constexpr`（或模板）定义，有真正的函数语义，有调用栈且可调试。而且使用 `constexpr` 修饰调用的语句，可以在编译期直接执行计算。
```cpp
constexpr int square(int x) {
    return x * x;
}

constexpr int x = square(1 + 2);  // 编译期直接计算为 9
```
### 多行宏（宏里写代码块）
由于宏无法进行作用域验证，在进行多行语句执行的场景，直接写多行语句的话会造成 `if` 作用域被隔断，造成如下错误。这是典型的 “宏破坏 if-else 结构” 问题。
```cpp
if (x > 0)
    std::cout << "begin";
std::cout << "x > 0" << std::endl;   // 脱离 if 控制！
else
    foo();   // 语法直接炸掉
```
使用 `do { } while(0)` 结构使得能在语法层面构成一条完整的单语句。
```cpp
#define LOG(msg) do { \
    std::cout << msg << std::endl; \
} while (0)
```
现代 C++ 推荐使用内联函数 `inline` 或更现代的模板实现。以及还可以使用 `constexpr + if constexpr` 等实现。
```cpp
// 内联变量实现
inline void LOG(const std::string& msg) {
    std::cout << msg << std::endl;
}

// 模板实现
template<typename T>
inline void LOG(T&& msg) {
    std::cout << std::forward<T>(msg) << std::endl;
}
```
### 宏字符串化 `#` 
宏字符串化可以将代码变为字符串。典型场景就是用于日志、断言和调试输出等。
```cpp
#define STR(x) #x

STR(hello)      // "hello"
STR(1 + 2)      // "1 + 2"
STR(a > b)      // "a > b"
```
以及字符串化还可以二次展开，如下：
```cpp
#define X 100
#define STR(x) #x
#define XSTR(x) STR(x)

STR(X)   //  "X"
XSTR(X)  //  "100"
```
这项功能在现代 C++ 中没有替代，因为这是在预处理阶段直接拿到源码形态的字符串。但是对于它所适用的场景，如日志等可以有替代，但是直接转化任意表达式为字符串功能本身不能被替代。
### 宏拼接 `##` 
宏拼接在预处理阶段造新标识符，基本定义是 `#define CONCAT(a, b) a##b`。典型场景就是自动生成变量名，避免命名冲突。还可以配合 `__LINE__` 生成 “唯一变量” ，以及生成批量接口等用法。
```cpp
#define MAKE_VAR(name) int var_##name

MAKE_VAR(foo);   // int var_foo;
MAKE_VAR(bar);   // int var_bar;
```

```cpp
#define UNIQUE_NAME(base) base##__LINE__

// 产生类似 tmp123、tmp124 等命名形式的变量
int UNIQUE_NAME(tmp);
int UNIQUE_NAME(tmp);
```
和宏字符串化一样，宏拼接本身的功能没有更现代的方式进行替代，但其使用场景能进行部分替代，比如使用模板 + `constexpr` 实现批量生成代码，使用智能指针 `std::unique_ptr` / RAII 替代唯一变量名宏。
```cpp
// 实现唯一变量
#define SCOPE_EXIT \
    auto UNIQUE_NAME(scope_exit_) = make_scope_exit([&]{ ... });

auto guard = make_scope_exit([&]{ ... });
```
## 其他预处理器使用场景
### 条件编译
条件编译一般是跨平台实现必备的机制，以下是实现平台判断的示例。不仅如此，条件编译还用于判断宏是否已定义、功能开关等。
```cpp
#ifdef _WIN32
    std::cout << "Windows";
#elif __linux__
    std::cout << "Linux";
#elif __APPLE__
    std::cout << "macOS";
#endif
```
### `#include` 
`#include` 的本质就是文本拷贝，就是将目标头文件的内容原样复制到源文件中。一般为了防止头文件重复会进行宏防卫。
```cpp
#ifndef MY_H
#define MY_H

class A {};

#endif
```
更为现代的写法是只需在头文件顶行写一个 `#pragma once` 即可，两者功能完全相同。
### 预定义宏（编译器自带）
以下是常见的预定义宏，可根据需要进行直接使用。但也有部分如`__FILE__`、`__LINE__` ，可以使用 C++ 20 的 `std::source_location` 进行替代。
```cpp
__FILE__     // 当前文件名
__LINE__     // 当前行号
__FUNCTION__ // 当前函数名（GCC/Clang）
__DATE__     // 编译日期
__TIME__     // 编译时间
__cplusplus  // C++ 标准版本
```
使用：
```cpp
std::cout << __FILE__ << ":" << __LINE__;
```

---
title: C++ 14 新特性
tags:
  - cxx
  - language-feature
---
## 泛型 lambda
C++ 11 引入的泛型，但是有一定的限制，比如参数类型必须明确指定类型、无法进行类型推导，本质上还是固定类型的 `operator()` ，而 C++ 14 是模板化的 `operator()` 。C++ 14 在以下几个方面进行了增强。
- Lambda 参数支持 `auto` 类型。
```cpp
auto add = [](auto a, auto b) { return a + b; };
```
- 返回类型支持自动推导，允许返回 Lambda 表达式和不同类型的返回值。
- 捕获表达式支持在捕获时可以初始化新变量。
```cpp
auto f = [val = 42]() { return val * 2; };
```
还可进行移动捕获
```cpp
auto ptr = std::make_unique<int>(10);
auto f = [p = std::move(ptr)]() { return *p; };
```
- 允许对 Lambda 表达式使用 `constexpr` 。
## 自动返回类类型推导
在 C++ 11 中，函数的返回值不能自动推导，除非显式使用尾置返回类型。
```cpp
auto func(...) -> return_type { ... }
```
但在 C++ 14 中解除了这个限制，允许使用 `auto` 推导返回类型。
```cpp
auto add(int a, int b) {
    return a + b;    // 自动推导为 int
}
```
注意：
- 对于 Lambda 表达式可以书写返回值不同的形式，但对于函数而言使用 `auto` 类型必须唯一的返回类型。
- `auto` 作为函数返回类型，遵循推导规则，所以在返回引用类型是并不会返回引用类型。
```cpp
int x = 100;
int& ref() { return x; }

auto f() {
    return ref();    // auto 推导成 int，而不是 int&
}
```
- 如果想返回引用类型，可以使用 `decltype(auto)` 。
```cpp
decltype(auto) f() {
    return ref();    // 返回 int&
}
```
## constexpr 增强
C++ 14 放宽了 constexpr 的限制，函数体允许多条语句，允许局部变量，允许循环、分支。
```cpp
constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i)
        result *= i;
    return result;
}

constexpr int f5 = factorial(5);  // 编译期计算 120
```
- 分支的条件必须在编译器求值。
- 不支持 `switch` 进行分支判断。
这样 constexpr 就可实现复杂的逻辑，基本上可以替代宏或模板元编程。
## `make_unique` 
原 C++ 11 支持的独占式指针只能使用 `std::unique_ptr<A>(new A())` 的方式进行创建，但当中存在风险。  
比如在 `f(std::unique_ptr<A>(new A()), g());` 的方法使用场景，`new A()` 先分配内存，当 `g()` 抛异常， `unique_ptr` 还没有构造成功，导致内存泄漏。而 `std::make_unique` 的内存分配 + 对象构造在一个表达式内完成，一旦异常发生，不会暴露裸指针。两种实现方式的差别不在功能，而在表达式的原子性和安全性。
## 二进制字面量
### 概述
C++14 开始支持直接用二进制写整数常量，在此之前只能用十进制、八进制、十六进制，不能直接写二进制。支持所有整数类型，也支持 `constexpr` 、`static_assert`，不支持浮点。二进制字面量语法是：
```cpp
0b101010
0B101010
```
### 使用场景
#### (1). 提高位掩码（bitmask）可读性
旧时一般采用十六进制写法，必须在脑子里转化。现在直接使用二进制写法，位结构一眼可见。
```cpp
// 十六进制写法
constexpr int mask = 0x2A;
// 二进制写法
constexpr int mask = 0b00101010;
```
#### (2). 寄存器 / 协议 / 标志位定义
可以非常直观地看到：bit0 = 1，bit2 = 1，bit3 = 1。这在嵌入式、协议解析、驱动代码中价值极高。
```cpp
constexpr uint8_t flags =
    0b0000'1101;
```
#### (3). 其他
推荐场景：
- 权限/状态位
- 编码/解码逻辑
不推荐使用场景：
- 普通业务逻辑数值
- 需要频繁修改的配置数值（除非是位字段）

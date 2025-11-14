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



## `make_unique` 

## 二进制字面量

## constexpr 增强




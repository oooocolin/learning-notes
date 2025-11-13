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



## 二、`make_unique` 

## 三、二进制字面量

## 四、自动返回类类型推导

## 五、constexpr 增强




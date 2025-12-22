---
title: C++ 20 新特性
tags:
  - cxx
  - language-feature
---
## 模板类型约束
### 概述
在 C++ 20 前，模板参数可以是任意类型，错误只在实例化时才报出，错误信息冗长，不容易对用户提供清晰的约束。此前使用 `enable_if` + SFINAE 解决，但是语法复杂，难以维护。C++ 20 引入 Concepts 为了提前约束模板类型，能清晰表达意图，可以在编译期检查，如果类型不满足要求，直接报错，并且改善错误信息。
### 实现
```cpp
#include <concepts>

template<typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::same_as<T>;
};
```
- `requires(T a, T b) { ... }`：要求类型 T 可以进行 `a + b` 操作。
- `-> std::same_as<T>`：要求结果类型与 T 相同。
- `Addable` 就是一个类型约束。
使用约束进行设置模板参数列表，这样 T 必须满足 `Addable` ，不满足就直接报错，错误信息清晰。以下是两种写法，语义一致，只是写法不同。
```cpp
template<Addable T>
T add(T a, T b) {
    return a + b;
}

template<typename T>
requires Addable<T>
T add(T a, T b) {
    return a + b;
}
```
以下这种写法，更为灵活，可针对函数重载使用不同约束。
```cpp
template<typename T>
T add(T a, T b) requires Addable<T> {
    return a + b;
}
```
### 标准库支持 Concepts
| Concept                         | 说明            |
| ------------------------------- | ------------- |
| `std::integral<T>`              | T 是整型         |
| `std::floating_point<T>`        | T 是浮点型        |
| `std::signed_integral<T>`       | 有符号整数         |
| `std::unsigned_integral<T>`     | 无符号整数         |
| `std::derived_from<T, U>`       | T 是 U 类或U类派生类 |
| `std::same_as<T, U>`            | T 与 U 类型相同    |
| `std::assignable_from<T, U>`    | 可以赋值          |
| `std::default_initializable<T>` | 可默认构造         |
| …                               | …             |
## Ranges
### 概述
此前，STL 的算法通常依赖迭代器区间。算法参数是迭代器，不直观，用户需要手动传入 `.begin()` / `.end()` ，进行链式操作很困难，且语义不够贴近 “集合/范围” 的概念。
```cpp
std::vector<int> v = {1,2,3,4,5};
std::sort(v.begin(), v.end());
auto it = std::find(v.begin(), v.end(), 3);
```
### 核心
#### (1). Range（范围）
范围相当于一对迭代器 + 边界，或者一个可迭代对象。本质上就是一个可迭代的集合。
```cpp
std::vector<int> v = {1,2,3};
auto r = v;  // v 本身就是 range
```
#### (2). View（视图）
视图是轻量、非拥有型范围，不拷贝底层数据，懒求值（按需计算）。其典型操作有 `filter` / `transform` / `take` / `drop` 。
```cpp
std::vector<int> v = {1,2,3,4,5};
auto evens = v | std::views::filter([](int x){ return x % 2 == 0; }); // {2, 4}
```
- `evens` 是视图，没有创建新容器。
- 底层直接引用 `v` 数据。
#### (3). Adapter（适配器）
Range 可以通过适配器组合操作，进行变换、筛选操作。
```cpp
auto r = v 
         | std::views::filter([](int x){ return x % 2 == 0; })
         | std::views::transform([](int x){ return x*x; });
```
- 链式调用，懒求值。
- 只有在遍历（`for` / `copy` / `accumulate`）时才真正计算。
### 使用
这样就不用分别传入迭代器，直接使用尤其是 STL 算法中，比如排序。
```cpp
std::ranges::sort(v);
```
## constexpr 再增强
C++ 20 支持在 constexpr 实现动态内存分配（`new/delete`），允许完整的 `try/catch`，允许虚函数，允许容器在编译期创建（元素是字面量类型），支持所有 STL 算法的执行。
```cpp
constexpr int* create_array(int n) {
    int* arr = new int[n];
    for (int i = 0; i < n; ++i) arr[i] = i;
    return arr;
}

constexpr auto arr = create_array(5);  // C++20 才允许
```
## 模块化

## 三路比较符（`<=>`）

## Coroutines

## 强化 lambda


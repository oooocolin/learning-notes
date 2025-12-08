---
title: C++ 20 新特性
tags:
  - cxx
  - language-feature
---
## constexpr 再增强
C++ 20 支持在 constexpr 实现动态内存分配（`new/delete`），允许完整的 `try/catch`，允许虚函数，允许容器在编译期创建（元素是字面量类型），支持所有 STL 算法的执行。
```cpp
constexpr int* create_array(int n) {
    int* arr = new int[n];
    for (int i = 0; i < n; ++i) arr[i] = i;
    return arr;
}

constexpr auto arr = create_array(5); // C++20 才允许
```
## 模板类型约束

## Ranges

## 模块化

## 三路比较符（`<=>`）

## Coroutines

## 强化 lambda


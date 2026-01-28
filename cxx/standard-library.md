---
title: C++ 标准库
tags:
  - cxx
  - std
---
## 概述
标准库是 ISO C++ 标准中规定的全部库集合，包含 STL 、字符串、I/O 、多线程、数值库、正则、时间库、文件系统等。C++ 标准模板库（STL）是一系列头文件的集合，它提供了多种数据结构、算法和函数，旨在简化 C++ 编码体验。STL最常用的功能可以分为三大类：容器、算法和迭代器。STL 和标准库有时会被混用叙述，但其实两者是不是一个层级的概念，STL 是标准库的一个子集。这是因为 STL 先出现，而后进入标准化后产生了标准库，所以造成这种混合语义的情况。
## STL 容器
C++容器是标准模板库（STL）的一部分，它提供用于存储和组织数据的数据结构。主要的有向量、双端队列、链表、映射表、集合等。详见 [C++ 容器](container.md) 。
## STL 算法
C++ 标准模板库 (STL) 提供了一系列通用算法，这些算法旨在与各种容器类配合使用。这些算法以函数的形式实现，可以应用于不同的数据结构，例如数组、向量、列表等。算法的主要头文件是 `<algorithm>` 。
### 排序
STL 提供了几种排序算法，例如 `std::sort`、`std::stable_sort` 和 `std::partial_sort` 。
- `std::sort` 不保证相等元素相对位置。
- `std::stable_sort` 保证相等元素相对位置。
- `std::partial_sort` 只保证前 K 个元素是最小（或最大）的 K 个，且这 K 个元素有序，不保证稳定性。
```cpp
std::vector<int> nums = {10, 9, 8, 7, 6, 5};
std::sort(nums.begin(), nums.end());

// 找出最小的 3 个元素并排序
std::partial_sort(v.begin(), v.begin() + 3, v.end());
```
### 搜索
搜索是指在给定的元素范围内查找特定元素是否存在。STL 提供了各种搜索算法，例如 `std::find` 、`std::binary_search` 和 `std::find_if` 。
- `std::find`：在区间中查找等于指定值的元素，返回指向第一个匹配元素的迭代器，未找到返回 `last` 。
- `std::binary_search`：在已排序区间中查找指定值是否存在，返回布尔值，若为排序返回未定义。
- `std::find_if`：查找第一个满足谓词条件的元素，不要求有序，返回值同 `std::find` 。
```cpp
std::vector<int> nums = {5, 6, 7, 8, 9, 10};
auto it = std::find(nums.begin(), nums.end(), 9);
bool exists = std::binary_search(v.begin(), v.end(), 42);
auto it2 = std::find_if(v.begin(), v.end(), [](int x) { return x > 7; });
```
### 修饰序列
STL 还提供了用于修改序列的算法，例如 `std::remove` ，`std::replace` 和 `std::unique` 。
- `std::remove`：从容器中移除给定范围 `[first, last)` 内的所有指定值，逻辑删除，不调整容器的大小。
- `std::replace`：替换容器中等于某个值的元素为另一个值。
- `std::unique`：移除相邻重复元素，不改变容器大小。
```cpp
std::vector<int> v = {1, 2, 3, 2, 4};
auto it = std::remove(v.begin(), v.end(), 2);  // 把所有 2 移到末尾
v.erase(it, v.end());  // 真正删除末尾的元素
```


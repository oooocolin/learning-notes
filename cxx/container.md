---
title: C++ 容器
tags:
  - cxx
  - container
---
## 概述
C++ 容器是标准模板库（STL）的一部分，它提供用于存储和组织数据的数据结构。主要的有向量、双端队列、链表、映射表、集合等。
## 向量
向量 `std::vector` 是可以根据需要调整自身大小的动态数组。它们将元素存储在连续的内存位置，从而可以使用索引进行快速随机访问。
```cpp
std::vector<int> vec = {1, 2, 3, 4, 5};
vec.push_back(6);
```
## 列表
列表 `std::list` 是一种双向链表，允许在常数时间内从任意位置插入或删除元素。它不支持随机访问。在需要频繁地在链表中间插入或删除元素的情况下，列表比向量更合适。但是在现代 C++ 中使用极少，因为 Cache 不友好（链表节点不连续分散分配在堆上）、内存开销大且碎片问题严重、标准算法对随机访问更友好、难以并发等一系列问题，所以在现代 C++ 中，只在明确需要稳定迭代器和 splice 常数时间拼接的要求（但实际上非常有限）才有可能使用，一般默认使用向量实现。
```cpp
std::list<int> lst = {1, 2, 3, 4, 5};
lst.push_back(6);
```
## 队列
C++ 的队列容器是双端队列 `std::deque` ，普通队列 `std::queue` 不是容器，是容器适配器，是通过容器进行接口层面的限制或是进行语义化封装产生的，可视作容器，`std::queue` 就是 `std::deque` 限制接口而来的。而优先级队列 `std::priority_queue` 是使用向量封装而来的，这是由二叉堆的算法模型天然依赖连续内存和随机访问的使用场景决定的。
```cpp
dequeue<int> dq = {1, 2, 3, 4, 5};

dq.push_front(1);
dq.push_back(6);

dq.pop_front();
dq.pop_back();
```
## 映射表与集合
映射表 `std::map` 是一种关联容器，用于存储键值对。它支持根据键检索值。默认情况下，键按升序排列。集合 `std::set` 也是关联容器，元素不可重复（`std::multiset` 允许重复，`std::multimap` 同理）。两者底层是红黑树，所以能保持有序。
```cpp
std::map<std::string, int> m;

m["one"] = 1;
m["two"] = 2;

std::set<int> st;
st.insert(2);
```
## 无序映射表与无序集合
与 Map 类似，无序 Map `std::unordered_map` 也存储键值对，但它使用哈希表实现。这意味着无序 Map 的平均性能比 Map 更快，因为它不维护排序顺序。然而，其最坏情况下的性能可能不如 Map。同样的，无序 Set `unordered_set` 与之类似。
```cpp
std::unordered_map<int, int> um;

um["one"] = 1;
um["two"] = 2;
```
## 现代 C++ 使用容器的核心准则
### 优先级顺序
1. `std::vector` 
2. `std::unordered_map` / `std::unordered_set` 
3. `std::map` / `set` 
4. `std::deque` 
5. `std::list` / `std::forward_list` （谨慎）
### 能 reserve 就 reserve
`reserve(n)` 强制容器的容量至少为 n（如果 n 比当前容量小，则什么也不做）。reserve 避免多次不必要扩容，从而达到性能优化的效果。
```cpp
v.reserve(n);
um.reserve(n);
```
### 值语义 + 移动语义是默认假设
容器天然支持移动语义操作。
```cpp
std::vector<BigObject> v;
v.push_back(std::move(obj));
```
### 不要滥用指针容器
现代 C++ 推荐不直接使用指针，使用智能指针进行声明和创建。
```cpp
// 旧写法
std::vector<Foo*>

// 现代写法
std::vector<Foo>
std::vector<std::unique_ptr<Foo>>
```

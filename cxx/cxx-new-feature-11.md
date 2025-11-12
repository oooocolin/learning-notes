---
title: C++ 11 新特性
tags:
  - cxx
  - language-feature
---
## 基于范围的 `for` 循环
是一种简化循环书写的语法糖，其结构为 `for (decl : range) statement;` 相当于一种容器的遍历。
```cpp
std::vector<int> v = {1, 2, 3, 4};

for (int x : v) {
    std::cout << x << " ";
}
```
相当于
```cpp
for (auto it = v.begin(); it != v.end(); ++it) {
    int x = *it;
    std::cout << x << " ";
}
```
## 自动类型推断
### 简介
`auto` 让编译器根据初始化表达式的类型自动推导变量类型，但它并不是“动态类型”，而是编译期静态类型推导。
```cpp
auto x = 10;        // x 是 int  相当于 int x = 10;
auto y = 3.14;      // y 是 double  相当于double y = 3.14;
auto s = "hello";   // s 是 const char*  相当于const char* s = "hello";
```
### 推导规则
| 表达式形式      | 推导结果                | 示例                                        |
| :--------- | :------------------ | ----------------------------------------- |
| 普通值        | 去掉引用和cv修饰           | `const int x=1; auto a=x; // a是int`       |
| 引用         | 保留实际类型，不自动添加引用      | `int &r=i; auto a=r; // a是int`            |
| 指针         | 保留指针                | `int *p; auto a=p; // a是int*`             |
| const指针    | const属性保留在指针上，不在值上  | `const int *p; auto a=p; // a是const int*` |
| 初始化为引用或右值  | 推导成值类型（除非用 `auto&`） | `auto a = getInt(); // 值拷贝`               |
| 使用 `auto&` | 保留引用关系              | `auto& r = i;`                            |
### 与基于范围的 `for` 循环结合
一般在使用 `for` 循环的遍历对象尤其是容器时比较常见 `auto&` 与 `const` 的集合，因为这个这既保证了不参与拷贝，降低了拷贝的性能开销，`const` 又保证了元素不被修改，是在循环遍历中常见的结构。
```cpp
for (const auto& item : vec) {
    // 安全，不拷贝
}
```
## Lambda 表达式
### 简介
Lambda 是一种匿名函数对象（functor），可以在定义的同时使用。其基本格式为 `[捕获列表](参数列表) -> 返回类型 { 函数体 }` 。
```cpp
auto f = [](int x, int y) { return x + y; };
std::cout << f(2, 3);  // 输出 5
```
- `[]`：捕获外部变量，可以捕获具体的变量，或是根据捕获规则按需捕获。
- `(int x, int y)` → 参数列表
- `{ return x + y; }` → 函数体
### 捕获规则
- `[=]`：值捕获。拷贝外部变量到 lambda 内部，但内部不可修改外部变量（除非用 `mutable`并且只会在内部生效，不影响外部）。
```cpp
int x = 10;
auto f = [=]() mutable { x += 1; return x; }; // x 在 lambda 内可改，但外部 x 不变
f();  // 内部 x = 11
```
- `[&]`：引用捕获。捕获外部变量的引用，lambda 内修改会影响外部变量。
```cpp
int x = 10;
auto f = [&]() { x += 1; };
f();  // 外部 x = 11
```
- `[x, &y]`：混合捕获。可以对不同变量选择值捕获或引用捕获。
### 注意
- 在 C++ 11 中如果返回值类型不一致时需要指定返回值类型，但在 C++ 14 中改善了这个问题，可以不用指定返回值了。
```cpp
auto f = [](bool b) -> double { 
    if (b) return 1; 
    else return 2.0; 
};
```
- C++ 11 书写函数以及 lambda 表达式返回 lambda 表达式 不支持 `auto` 类型，这要在 C++ 14 改善。
- C++ 11 只支持捕获普通变量、指针、容器、`this` 指针，之后版本将支持更多，比如初始化捕获（C++ 14）、`*this` （C++ 17）、泛型类型约束（C++ 20）等。
## 列表初始化
列表初始化（List Initialization），也叫统一初始化（Uniform Initialization），这是现代 C++ 很重要的语法糖之一。提升了可读性，也减少了类型歧义和隐式转换问题。C++11 引入了 `{}` 花括号来初始化变量，相比传统初始化，`{}` 是统一的初始化语法，所有类型都可以使用，避免了 C++98/03 多种写法的混乱。
```cpp
int x{5};                        // x = 5
std::vector<int> v{1,2,3,4,5};
std::string s{"hello"};          // s = "hello"
Student{1, "LiHua"};             // 初始化类对象
```
但也得注意分别一些特殊情况：
- 注意数组与容器语法的区别。
```cpp
std::vector<int> v1{10}; // 1个元素 10
std::vector<int> v2(10); // 10个默认元素 0
```
- 列表初始化可以进行嵌套初始化。
```cpp
struct Rect {
    Point topLeft;
    Point bottomRight;
};

Rect r{{0,0}, {10,10}}; // 嵌套列表初始化
```
## 移动语义
### 简介
传统 C++ 对象拷贝都是 深拷贝（Copy），这对小对象无妨，但对大对象，比如容器、字符串、文件句柄等，复制成本很高。移动语义优化的目标是将临时对象或即将被销毁的对象，不必再做昂贵的拷贝，直接搬走资源（之后原对象置空），避免内存拷贝。具体而言，移动语义专门针对右值（临时对象，反之左值是有名字可寻址的对象）。在 C++ 11 中新增 `T&&` 类型用于表示右值引用。
### 转换左值
C++ 11 新支持的 `std::move` 可以将左值强制转换为右值，之后在构造/赋值过程中实现移动语义。
```cpp
std::vector<int> v1 = {1,2,3};
std::vector<int> v2 = std::move(v1);
```







## 四、线程与并发

## 六、智能指针

## 八、constexpr



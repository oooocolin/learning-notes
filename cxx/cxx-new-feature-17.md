---
title: C++ 17 新特性
tags:
  - cxx
  - language-feature
---
## 结构化绑定
结构化绑定允许你把一个由多个值组成的对象，如 `pair` （类似有且仅有两个元素的元组）、`tuple`（类似 Python 的元组）、数组、自定义 struct，拆开成多个变量直接绑定。这大大简化了书写的方式。
```cpp
// 旧的书写方式
auto p = std::make_pair(1, 2);
int a = p.first;
int b = p.second;

// 结构化绑定
auto [a, b] = std::make_pair(1, 2);
```
**注意**：
- 结构化绑定不能写类型限制，不能写成 `int [a, b] = p;` 。
- 对于 `struct` 成员必须要求必须是 `public` ，必须是非 `static` 。
## `if`/ `switch` 内初始化
C++ 17 开始可以在 `if` / `switch` 的括号内加入初始化语句。并且初始化的结果只在 `if` / `switch` 的作用域中有效。其语法结构如下：
```cpp
if (init; condition) { ... }

switch (init; expr) { ... }
```
**优点**：
- 减少作用域泄漏，使真正仅为该分支语句使用的变量限制作用域在分支语句内。
- 让逻辑更紧凑，更能表达代码编写者的意图。
- 有利于节省内存，该变量会在分支判断后销毁。
## 值的包装
### 简介
C++ 17 新引入 `std::optional`, `std::variant`, `std::any` 三个重要类型，都用于值的包装。但三者功能和使用场景完全不同。
### `std::optional` 
`std::optional` 类型确定，但值可能不存在。类似于Swift 的 `Optional`、Rust 的 `Option<T>`、Haskell 的 `Maybe` 。
```cpp
std::optional<int> getAge(bool ok) {
    if (ok) return 20;
    return std::nullopt;  // 无值
}

// main.cpp
auto age = getAge(true);
if (age) {
    std::cout << *age;   // 解引用
}
```
`std::optional` 类型本身更多偏向是一种语义传达，在编写者看到这个类型就该意识到可能返回空值。如果是直接指定特殊值，调用者可能会容易忘记空值的情况。本质上而言，`optional` 就是 “有值 / 无值” 的单类型联合。因为其底层结构如下，本质就是 `union Maybe<T> = None | Some(T)` 。
```cpp
struct optional {
    bool has_value;  // 标签(tag)
    T value;         // 如果 has_value=true 则有效
};
```
### `std::variant` 
`std::variant` 就是类型安全的 `union` 。以下就是可以是 int 或 string类型的变量。
```cpp
std::variant<int, std::string> v;

v = 10;
v = std::string("hello");

// 访问需要 std::visit
std::visit([](auto& x){
    std::cout << x;
}, v);
```
**优点**：
- 比传统 `union` 更安全。
- 编译期类型检查。
- 不需要额外内存分配（放在栈上即可）。
**使用场景**：
- 解析 JSON（`number`/`string`/`bool`/`null`）。
- 状态机（State A/B/C）。
- 多类型返回值。
- 代替继承+多态的场景。
### `std::any` 
`std::any` 是能存任何类型的值，类似 Java 的 Object 或 Python 的动态类型，是完全的的类型擦除。但是也带来了对应的问题，就是放弃了类型安全，除非真的需要使用动态类型，不建议随意使用 `any` 。
```cpp
std::any a = 10;
a = std::string("hello");
a = std::vector<int>{1,2,3};

// 取值方法，若类型不匹配会抛出异常
auto s = std::any_cast<std::string>(a);
```
**优点**：
- 完全动态类型。
- 适合框架、元编程、通用容器。
- 解耦不同模块。
**缺点**：
- 需要动态内存，导致一定得性能降低。
- 必须运行时检查类型，而不是在编译器确认，不够安全。
- 可能抛异常。
## 文件系统库
### 简介
C++ 17 引入了文件系统库 `<filesystem>` ，用于文件/目录操作、路径处理、递归遍历、文件状态查询等场景。提供了跨平台的路径 API（不用再写 `#ifdef Windows / Linux`），提高了安全性，提供了异常处理和明确返回值，替代旧的 C 系列的 API（`<cstdio>`, `system("mkdir")` 等）。
### `path` 
`std::filesystem::path` 表示文件路径。可以把 `path` 看成 C++ 的字符串+路径语义，它自动处理分隔符、拼接、文件名和扩展名解析。
```cpp
namespace fs = std::filesystem;

fs::path p = "C:/Users/admin/data.txt";

cout << p.filename();    // "data.txt"
cout << p.stem();        // "data"
cout << p.extension();   // ".txt"
```
### `exists` 
`exists` 用于检查文件或目录是否存在。
```cpp
fs::path p = "test.txt";

if (fs::exists(p)) {
    cout << "File exists\n";
}
```
### 创建和删除文件/目录
创建目录
```cpp
fs::create_directory("data");
fs::create_directories("a/b/c");    // 递归创建（一层层创建直到最后的目录）
```
删除目录/文件
```cpp
fs::remove("data/test.txt");        // 删除一个文件
fs::remove_all("data");             // 删除整个目录
```
### 遍历目录
`directory_iterator` 进行非递归遍历目录，`recursive_directory_iterator` 进行递归遍历目录（包含地址子目录内的内容）。
```cpp
for (auto& entry : fs::directory_iterator("data")) {
    cout << entry.path() << endl;
}

for (auto& entry : fs::recursive_directory_iterator("data")) {
    cout << entry.path() << endl;
}
```
### 文件拷贝
```cpp
fs::copy("a.txt", "b.txt");
```
### 重命名/移动文件
```cpp
fs::rename("old.txt", "new.txt");
```
如果目标路径不同，即为移动操作。
## 内联变量
C++ 17 起，可以在全局或类内声明 inline 变量，它的可以在多个 `.cpp` 文件中重复定义（不会链接错误；链接时自动合并为一个实例（与 inline 函数一样）；适用于常量、全局变量、类静态成员等。
```cpp
inline int x = 10;
```
而在此前必须在头文件声明，并且使用 `extern` 关键字，然后再在源文件初始化。在 C++ 17 之后可以直接在头文件定义，并且在任意源文件引用时不会报重复定义，链接器会合并它们。并且类静态成员变量同样支持。
```cpp
// 其此前的写法
// .h
extern int counter;

// .cpp
int counter = 0;
```
## 并行算法

## constexpr 进一步增强

## 字符串字面量改进



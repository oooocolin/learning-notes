---
title: C++ 模板
tags:
  - cxx
  - template
---
## 概述
模板用于编写与数据类型无关的代码，是 C++ 中实现泛型的基础，避免方法因为类型而多次重载，提高代码复用率。模板的背后原理是通过编译器根据传入类型生成具体函数的版本，在调用时调用具体的实现。模板分为函数模板和类模板。
## 语法结构
函数模板：
```cpp
// 泛型函数模板
template <typename T>
T add(T a, T b) {
    return a + b;
}

int main() {
    cout << add(2, 3) << endl;       // int
    cout << add(2.5, 3.7) << endl;   // double
}
```
类模板：
```cpp
template <typename T>
class Box {
    T value;
public:
    Box(T v) : value(v) {}
    T get() { return value; }
};

int main() {
    Box<int> intBox(10);      // T = int
    Box<double> doubleBox(3.14);  // T = double

    cout << intBox.get() << endl;
    cout << doubleBox.get() << endl;
}
```
## 特化及偏特化
模板函数和模板类需要对传入的不同类型进行不同的处理，是针对某些类型或是某些类型模式专门写一个实现。具体而言，有全特化和偏特化之分。  
- **全特化**：模板类型里的所有类型参数全部具体指明之后处理。`template<>` 中为空，代表所有类型都在下面特殊化处理。
- **偏特化**：模板类型里的局部类型参数进行具体指明，仍保留一部分泛化类型。
```cpp
// 全特化
template<>
struct A<int,int> {
	A(){ cout<<"int, int特化版本构造函数"<<endl; } 
	void func() { cout<<"int,int特化版本"<<endl; } 
};

// 对指针类型的偏特化
template <typename T>
struct TypeInfo<T*> {
    static void print() {
        cout << "指针类型" << endl;
    }
};
```
**注意**：
- 对于函数模板没有偏特化。因为模板会自动进行重载，这相当于语义上支持更特定版本，支持偏特化的话会与重载冲突。
- 模板特化与其他语言的泛型类型约束不同。模板本身不能限制类型，只能对特定类型进行特定逻辑的实现，而泛型类型约束可以约束实现的类型。若需要限制类型需要使用 C++ 11/17 以后的约束机制。
- 模板特化需要保留最通用的那个模板，因为特化本质上只是一种实现而已。
## 注意
由于 C++ 模板是在编译器在编译期间静态创建模板实现的，所以模板不存在其他静态类型语言实现泛型的泛型擦除问题（由于 Java、C# 泛型是在编译期做类型检查，运行时将类型擦除为 Object 类型）。

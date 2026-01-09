---
title: 原型模式
tags:
  - common
  - design-pattern
  - prototype
---
## 概述
原型模式适用于当对象创建成本很高，且结构复杂时，通过复制已有对象来创建新对象。特征是类构造函数参数多，且内部状态复杂，new 的初始化成本高。
## 现代工程的处境
原型模式在现代工程中存在感很低。因为构造成本不再是核心问题，尤其是 JVM 优化过后，避免 new 本身已经不是强诉求。但深拷贝复杂度极高，这在真实系统中极其容易出 bug。而且现代系统更倾向于不可变对象 + 构造组合，而不是复制，使得原型模式的价值大大削弱。从现实的工程实践来说，原型模式基本死亡。
## 替代方案
从语言层面，原型模式被 new 创建方式本身取代，或是被 record 吞噬，使用不可变对象的特点，从对象的复制转向数据结构的复制，其在框架内也被配置 + 构造取代。这是该设计模式的前提被否定造成的现象，
```java
public record User(String name, int age, String email) {}
User u2 = new User(u1.name(), u1.age(), "new@mail.com");

// 或是进行封装
User withEmail(String email) {
    return new User(name, age, email);
}
```
## 误区
框架中的 prototype scope 并不是 GoF 原型，而是每次请求创建新实例，名字相同，但是语义上并不相同。

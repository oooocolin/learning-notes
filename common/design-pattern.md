---
title: 设计模式
tags:
  - common
  - design-pattern
---
## 概述
设计模式是一个面向对象开发方法下的概念，是解决代码设计 / 软件架构问题的可复用的元素。一般的设计模式一般是指源于GoF所著的 "Design Patterns - Elements of Reusable Object-Oriented Software" 一书（也有将该书直接简称为GoF），译著为 “设计模式：可复用面向对象软件的基础” 的 23 种设计模式。其目的是**补充语言能力不足的结构实现**。原书将这23种设计模式分为三类：
- 创建型包含5种模式，涉及对象/对象组合的创建构建。
- 结构性包含7种模式，涉及对象/类之间的关系。
- 行为型包含11种模式，涉及对象/类的行为、状态、流程。
但广泛的说，还有由此在新场景下诞生或是以上几种设计模式组合演变的成果，也在设计模式的探讨范围，也将展开说明。而且 GoF 式的设计模式在现代语言编程中已经被语言和框架吞并，所以对于传统的 23 种设计模式学习的重点主要是为了识别，而不是套用和实现。
## 传统 23 种设计模式
### 创建型
- [工厂方法与抽象工厂](design-pattern-factory.md) 
- [单例模式](design-pattern-singleton.md) 
- [原型模式](design-pattern-prototype.md) 
- [建造者模式](design-pattern-builder.md) 
### 结构型
- [适配器、桥接与外观模式](dp-adapter-bridge-facade.md) 
- [代理模式与装饰器模式](dp-proxy-decorator.md) 
- [组合模式、享元模式](dp-composite-flyweight.md) 
### 行为型
- [策略模式和状态模式](dp-strategy-status.md) 
- [责任链模式和备忘录模式](dp-chain_of_resp-memento.md) 
- [观察者模式、中介模式、访问者模式](dp-observer-mediator-visitor.md) 
- [命令模式、迭代器、解释器](dp-command-iterator-interpreter.md) 
- [模板方法模式](design-pattern-template.md) 





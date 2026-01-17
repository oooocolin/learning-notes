---
title: 观察者模式、中介模式、访问者模式
tags:
  - common
  - design-pattern
  - observer
  - mediator
  - visitor
---
## 概述
观察者模式、中介模式在理念上有部分重合，都是为了响应变化，观察者模式偏向一对多的广播式，中介模式偏向多对多的集中管理。而且观察者不包含业务规则，中介的价值恰恰在于规则集中。而对于访问者模式，与前两个模式在实现上没有太多联系。但观察者、访问者二者都是想去 “读” ，不会直接改变被读对象的状态。观察者通过订阅监听的方式被动地读，而访问者是主动视角。访问者不同于中介，访问者不协调对象，访问者只定义如何处理。
## 观察者模式
### 简介
观察者模式的意图是当一个对象的状态发生变化时，所有依赖于它的对象都会得到通知并自动更新。核心目标是解耦状态变化与变化后的响应，支持一对多的依赖关系。一般用在 UI 数据变化、配置变更等场景。
### 实现
Subject 持有 Observer 列表，状态变化后主动通知。
```java
interface Observer {
    void update(State state);
}

interface Subject {
    void addObserver(Observer o);
    void removeObserver(Observer o);
    void notifyObservers();
}
```
### 工程现状
观察者模式至今未淘汰，是行为型中生命力最强的模式，只是以及高度工程化，以平台或框架接管，已经不再以模式代码而存在。在语言层级，可以使用回调函数、Lambda 、Promise / Observable 进行部分轻量化实现，在框架和平台层级 Spring ApplicationEvent 、DOM Event 、Rx / Reactive Stream 、SwiftUI 的 `@ObservedObject` 等都是其应用。
## 中介模式
### 简介
中介模式的意图是用一个中介对象来封装一系列对象之间的交互，使它们不需要显式地相互引用。核心目标是避免对象之间形成网状依赖，将协作逻辑集中管理。一般用在表单控件联动、UI 状态协调、复杂业务流程调度、游戏对象交互逻辑。
### 实现
中介模式以中央协调者的形式存在，各 Colleague 统一持有这个中介对象，而不是各 Colleague 相互依赖。中介可以以硬编码显式引用或是 Map 、List 、Set 等容器实现。
```java
interface Mediator {
    void notify(Component sender, String event);
}

// Colleague
class Component {
    protected Mediator mediator;
}
```
### 工程现状
现代工程的中介这模式不以 Mediator 显式声明，也是现代工程弱化设计模式命名的体现，但集中协作决策的结构任然存在，多见于系统级设计，而非普通业务类。语言层级主要是闭包封装协作逻辑、状态机；框架层级主要是 Controller / ViewModel 、Workflow / Saga 、Orchestrator 。
## 访问者模式
### 简介
访问者模式的意图是表示一个作用于某对象结构中的各元素的操作，使你可以在不改变元素类的前提下定义新操作。核心目标是操作与数据结构分离，对结构开放、对操作扩展。
### 实现
```java
interface Element {
    void accept(Visitor v);
}

class A implements Element {
    void accept(Visitor v) { v.visit(this); }
}

class Visitor {
    void visit(A a) { ... }
    void visit(B b) { ... }
}
```
### 现状
访问者模式通过将结构和操作分开，从事实上形成双向绑定，并造成了结构侵入，工程应用极窄。所以虽然在 AST / 编译器里仍然用，因为元素结构稳定，操作多，但在 UI / 后端业务逻辑里几乎不用，往往用策略模式、命令模式或者函数式组合代替。

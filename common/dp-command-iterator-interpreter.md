---
title: 命令模式、迭代器模式、解释器模式
tags:
  - common
  - design-pattern
  - dp-command
  - dp-iterator
  - interpreter
---
## 命令模式
### 简介
命令模式将一个请求封装成对象，从而使得可用不同的请求、队列或日志来参数化客户端；支持可撤销操作。核心目标是把调用者和执行者解耦，支持请求排队、日志记录、撤销，使请求成为对象，可灵活操作。典型场景是 UI Menu / Toolbar 操作，事务操作封装等
### 实现
```java
// 命令接口
interface Command {
    void execute();
}

// 具体命令
class SaveCommand implements Command {
    private final Document doc;
    public SaveCommand(Document doc) { this.doc = doc; }
    @Override
    public void execute() { doc.save(); }
}

// 调用者
class MenuItem {
    private Command command;
    public MenuItem(Command command) { this.command = command; }
    public void click() { command.execute(); }
}

// 接收者
class Document {
    void save() { System.out.println("保存文档"); }
}
```
### 工程现状
现代工程对命令模式依然常用，但使用形式发生了一些变化，更多依赖语言特性和框架，而不是显式地创建命令类。在语言层面可以使用函数 / Lambda，或是闭包，在框架层级，Spring `TaskExecutor` / 异步方法、JS Promise / async queue 是其替代形式。
## 迭代器模式
### 简介
迭代器模式提供一种方法顺序访问一个集合对象中的各个元素，而又不暴露该对象的内部表示。核心目标是隐藏集合内部结构，提供统一访问接口，并支持多种遍历方式，典型场景是 Collection / List 遍历、数据库分页、Stream / 流处理等。
## 实现
```java
interface Iterator<T> {
    boolean hasNext();
    T next();
}

interface Aggregate<T> {
    Iterator<T> iterator();
}

class ListAggregate<T> implements Aggregate<T> {
    private final List<T> list;
    public ListAggregate(List<T> list) { this.list = list; }
    @Override
    public Iterator<T> iterator() { return list.iterator(); }
}
```
### 工程现状
在现代工程中，内置迭代器替代手动写的迭代器，并且可用函数式遍历大幅减少样板代码。在语言层面 for-each 循环、Generator / yield（JS / Python）、Iterable / Sequence（Kotlin / Scala）可进行替代，在框架层级的有 Stream / Rx / Flow 、Spring Data 分页 / Stream 等。迭代器模式基本已被语言原生特性取代，但思想仍然重要，即是隐藏集合结构、统一访问接口的思想。
## 解释器模式
### 简介
解释器解决这么一个场景的问题，给定一个语言，定义它的文法表示，并定义一个解释器，该解释器使用该表示来解释句子。核心目标在语法树 / 文法结构的解释，支持复杂语法解析和表达式计算等方面。典型场景是表达式解析（数学 / 逻辑公式）、DSL / 配置解析、查询条件构建（SQL / Criteria / Elasticsearch Query）等。
### 实现
```java
interface Expression {
    boolean interpret(String context);
}

class TerminalExpression implements Expression {
    private String data;
    public TerminalExpression(String data) { this.data = data; }
    @Override
    public boolean interpret(String context) {
        return context.contains(data);
    }
}

class OrExpression implements Expression {
    private Expression expr1, expr2;
    public OrExpression(Expression expr1, Expression expr2) {
        this.expr1 = expr1; this.expr2 = expr2;
    }
    @Override
    public boolean interpret(String context) {
        return expr1.interpret(context) || expr2.interpret(context);
    }
}
```
### 工程现状
解释器模式在现代工程中几乎退场，只有 DSL / 语言编译器等领域仍用，一般在利用解析器生成工具、组合式函数时使用。语言层级使用函数式组合、AST + Pattern Matching 、正则 / parser combinator 就可完成替代，框架层级有 ANTLR / Xtext / Kotlin Parser 、SQL 构建器 / JPA Criteria / Elasticsearch DSL 、Spring Expression Language（SpEL）等。

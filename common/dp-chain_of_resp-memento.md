---
title: 责任链模式和备忘录模式
tags:
  - common
  - design-pattern
  - chain_of_responsibility
  - memento
---
## 概述
责任链和备忘录模式虽然在意图和设计上都不相同，但它们都依赖对象的组合与调用时机控制，二者都有非常浓厚的 IoC 控制反转的味道，和生命周期的设计联系紧密。
## 责任链模式
### 简介
责任链模式将请求沿着对象链传递，直到某个对象处理它。调用方不知道具体谁处理请求，每个对象只关心自己能否处理，可动态添加 / 删除处理对象。典型场景就是中间件、拦截器、事件处理管道。
### 实现
```java
// 请求处理接口
public interface Handler {
    void setNext(Handler next);
    void handle(Request request);
}

// 具体处理者 A
public class AuthHandler implements Handler {
    private Handler next;
	
    @Override
    public void setNext(Handler next) { this.next = next; }
	
    @Override
    public void handle(Request request) {
        if (!request.isAuthenticated()) {
            System.out.println("认证失败，停止处理");
        } else if (next != null) {
            next.handle(request);
        }
    }
}

// 具体处理者 B
public class LoggingHandler implements Handler {
    private Handler next;
	
    @Override
    public void setNext(Handler next) { this.next = next; }
	
    @Override
    public void handle(Request request) {
        System.out.println("记录日志");
        if (next != null) next.handle(request);
    }
}

// 使用
public class Main {
    public static void main(String[] args) {
        Handler auth = new AuthHandler();
        Handler log = new LoggingHandler();
		
        auth.setNext(log); // 链路：Auth -> Logging
		
        Request req = new Request(true);
        auth.handle(req);
    }
}
```
### 现代工程替代
责任链本身可以使用函数链 / Lambda 进行实现。
```java
Consumer<Request> chain = req -> {
    auth(req);
    logging(req);
};
```
在框架层面可以使用 Spring 责任链或是使用管道或是相关中间件实现。
- Spring `HandlerInterceptor` 。
- Servlet Filter Chain 。
- Express / Koa 中间件 。
责任链的核心思想就是把处理逻辑解耦，控制权交给链结构。
## 备忘录模式
### 简介
备忘录模式意图在不破坏封装的前提下保存对象状态，以便恢复。关注对象的生命周期，强调状态快照与隔离。
### 实现
实现核心就是使用一个类来持有不可变状态对象，由此在返回状态的时候重新赋值回去。
```java
// 备忘录类：保存状态
public class Memento {
    private final String state;
	
    public Memento(String state) { this.state = state; }
    public String getState() { return state; }
}

// 发起人（需要被保存状态的对象）
public class Editor {
    private String content;
	
    public void type(String text) { content = text; }
	
    public Memento save() { return new Memento(content); }
    public void restore(Memento m) { content = m.getState(); }
	
    public String getContent() { return content; }
}

// 管理者（可选）
public class History {
    private final Stack<Memento> stack = new Stack<>();
	
    public void push(Memento m) { stack.push(m); }
    public Memento pop() { return stack.pop(); }
}

// 使用
public class Main {
    public static void main(String[] args) {
        Editor editor = new Editor();
        History history = new History();
		
        editor.type("Hello");
        history.push(editor.save());
		
        editor.type(" World");
        System.out.println(editor.getContent()); // Hello World
		
        editor.restore(history.pop());
        System.out.println(editor.getContent()); // Hello
    }
}
```
### 现代工程替代
备忘录解决的是一个不可消除的问题，要求状态必须可恢复、状态必须与业务对象解耦、不能暴露对象内部结构所以其需求不会消失。但是在现代工程中不显式地去写 Memento 类了，而是变成 Snapshot 语法更轻。
```java
record Snapshot(String content, long version) {}
```
而对于备忘录模式而言，模式使用不可变对象 / Snapshot + Map 进行实现。其中 Snapshot 是一个不可变的、可复制的、完整描述对象状态的数据结构。在各种语言中都是以不可变对象的语言机制存在的，比如 Java 就是 record ，TypeScript 就是 Readonly Object 或 `as const` ，Kotlin 就是 data class ，Swift 就是 struct 。以 Java 为例演示实现。
```java
// Snapshot
public record OrderSnapshot(
    String orderId,
    String status,
    BigDecimal amount
) {}

// 业务对象使用
public class Order {
    private final OrderSnapshot snapshot;
	
    public Order(OrderSnapshot snapshot) {
        this.snapshot = snapshot;
    }
	
    public OrderSnapshot snapshot() {
        return snapshot;
    }
	
    public Order changeStatus(String status) {
        return new Order(new OrderSnapshot(
            snapshot.orderId(),
            status,
            snapshot.amount()
        ));
    }
}

// 状态管理，可使用 Map / Stack 
Map<String, Deque<OrderSnapshot>> history = new HashMap<>();
history.computeIfAbsent(id, k -> new ArrayDeque<>())
       .push(order.snapshot());

// 回滚
OrderSnapshot prev = history.get(id).pop();
Order order = new Order(prev);
```
## 与 IoC 的联系
责任链和备忘录都不是 “算法模式” ，而是 “控制权转移模式” ，它们与 IoC 的关系，不在注入，而在于谁决定流程、谁决定时机、谁拥有状态的演进权。
### 责任模式
责任模式转移了执行流程的决定权。调用者不再知道谁会处理，调用者不再决定下一个是谁，流程的推进权被交给链本身。
```java
// 调用者控制流程
if (a.canHandle()) {
    a.handle();
} else if (b.canHandle()) {
    b.handle();
} else if (c.canHandle()) {
    c.handle();
}

// 流程的推进权被交给链本身
handler.handle(request);
```
所以责任链可插拔、可重排、可配置的特性天然适合框架。所以在日志、鉴权、校验、限流、事务边界大量使用责任链。
### 备忘录模式
备忘录模式转移了状态演进与回滚的决定权。现代 Snapshot 形态下，在回滚中业务对象不决定是否保存，业务对象不决定回滚到哪一版，业务对象甚至不知道谁在管理历史，这就是标准的 IoC 。也就是把状态的时间维度控制权从对象交给系统。

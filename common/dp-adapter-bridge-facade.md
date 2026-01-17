---
title: 适配器、桥接与外观模式
tags:
  - common
  - design-pattern
  - adapter
  - bridge
  - facade
---
## 概述
在 GoF 的结构型设计模式中，适配器模式、桥接模式、外观模式在现代的工程中仍在使用，甚至是至今活跃，并且由于三者在过程代码实现中的形式往往类似或是在某种场景中是一致的。他们都是使用组合进行持有其他对象，并暴露出新接口，在不修改原对象的前提下实现意图，从代码结构来看是同一类型。
```
Client
  ↓
Wrapper（Adapter / Bridge / Facade）
  ↓
One or More Wrapped Objects
```
这三者的不同点在于意图的偏向：
- 适配器模式：使接口能用，偏向解决接口不兼容的问题。
- 桥接模式：隔离两端的变化，将抽象和实现解耦。
- 外观模式：简化使用，组合流程，实现用户友好。
## 模式介绍
### 适配器模式
适配模式一般偏向于一些解决不兼容问题的场景，比如历史包袱（旧接口）、第三方库（无法修改）、边界系统（协议不同）等。
```java
// 第三方SDK
class AliPayClient {
    void pay(String orderNo, BigDecimal amount) {}
}

// 期望的统一接口
interface PaymentService {
    void pay(PaymentRequest request);
}

// 适配器
class AliPayAdapter implements PaymentService {
    private final AliPayClient client;
	
    AliPayAdapter(AliPayClient client) {
        this.client = client;
    }
	
    @Override
    public void pay(PaymentRequest request) {
        client.pay(request.orderNo(), request.amount());
    }
}
```
### 桥接模式
桥接模式将内部变化的两个部分分离，即抽象部分与实现部分，使它们可以独立变化。两个部分要求正交，分离也是由此实现。偏向于解决多种组合导致子类数量过多，提供稳定的接口层，对外屏蔽具体实现等场景。
```java
// 发送渠道接口
public interface MessageSender {
    void send(String message, String toUser);
}

// 具体发送实现
public class SmsSender implements MessageSender {
    @Override
    public void send(String message, String toUser) {
        System.out.println("发送短信给 " + toUser + "，内容：" + message);
    }
}

public class EmailSender implements MessageSender {
    @Override
    public void send(String message, String toUser) {
        System.out.println("发送邮件给 " + toUser + "，内容：" + message);
    }
}

// 消息抽象类
public abstract class Message {
    protected MessageSender messageSender;
	
    public Message(MessageSender messageSender) {
        this.messageSender = messageSender;
    }
	
    public abstract void sendMessage(String message, String toUser);
}

// 具体消息类型
public class NormalMessage extends Message {
	
    public NormalMessage(MessageSender messageSender) {
        super(messageSender);
    }
	
    @Override
    public void sendMessage(String message, String toUser) {
        messageSender.send(message, toUser);
    }
}

public class UrgentMessage extends Message {
	
    public UrgentMessage(MessageSender messageSender) {
        super(messageSender);
    }
	
    @Override
    public void sendMessage(String message, String toUser) {
        String urgentMessage = "【紧急】" + message;
        messageSender.send(urgentMessage, toUser);
    }
}

// 客户端使用
public class Client {
    public static void main(String[] args) {
        MessageSender smsSender = new SmsSender();
        MessageSender emailSender = new EmailSender();
		
        Message normalMessage = new NormalMessage(smsSender);
        normalMessage.sendMessage("系统运行正常", "张三");
		
        Message urgentMessage = new UrgentMessage(emailSender);
        urgentMessage.sendMessage("服务器宕机", "李四");
    }
}
```
以上将消息类型和发送方式分离，这样就不再产生大量子类，并且符合开闭原则，业务的维度清晰，实现多个变化维度的分离演进。
### 外观模式
外观模式更为偏向于向子系统中的一组接口提供一个统一的高层接口，使子系统更易使用，比如API 网关、Controller 层等场景。
```java
public class OrderFacade {
	// 库存子系统
    private InventoryService inventoryService = new InventoryService();
    // 订单子系统
    private OrderService orderService = new OrderService();
    // 支付子系统
    private PaymentService paymentService = new PaymentService();
    // 积分子系统
    private PointService pointService = new PointService();
	
    public void placeOrder(String userId, String productId) {
        if (!inventoryService.checkStock(productId)) {
            throw new RuntimeException("库存不足");
        }
		
        inventoryService.deductStock(productId);
        orderService.createOrder(userId, productId);
        paymentService.pay(userId);
        pointService.addPoint(userId);
		
        System.out.println("下单流程完成");
    }
}

// 客户端调用
public class Client {
    public static void main(String[] args) {
        OrderFacade orderFacade = new OrderFacade();
        orderFacade.placeOrder("U1001", "P2001");
    }
}
```
## 简化
### 适配器模式
适配器本身修改不多只需 1~2 个地方的场景，在一些可以函数式编程的语言中，使用函数式的修改是更为轻量化的选择，而面对更为重大或是关联性较强的转换方法仍应该使用类结构。
### 桥接模式
在一些可以函数式编程的语言中，高阶函数 + 模块组合可以替代桥接，类存在更多是为了类型约束和语义清晰。
### 外观模式
在现代语言中，模块本身就可以承担 Facade 功能，可以通过限制模块的可见性实现隐藏子系统的功能，明确划分了边界，而不是依靠团队本身的管理。而提供友好的接口这个功能仍需要导出类或是函数实现。

---
title: SOLID 原则
tags:
  - common
  - programming-principles
---
## 一、SOLID 原则
SOLID 原则是面向对象设计的“黄金五法”。
### 1. 单一职责原则（SRP - Single Responsibility Principle）
> 一个类应该只有一个引起它变化的原因。

**说明**：
- 从“变化点”出发去设计。一个类的修改原因越多，说明它职责越杂。
- 一般可以从以下维度去拆分：
	- 数据模型（如 `User`），
	- 行为（如 `UserRepository`、`UserValidator`、`UserService`），
	- 视图控制（如 `UserController`）；
- 拆分时遵循 “高内聚、低耦合”；
- 技巧：观察修改日志，如果同一个类频繁被多个开发者出于不同目的修改，那一定违反 SRP。
### 2. 开闭原则（OCP - Open/Closed Principle）
> 对扩展开发，对修改关闭。

**说明**：
- 使用多态、接口、抽象类来定义稳定的契约；
- 让新功能通过继承或组合的方式添加，而不是修改旧代码；
- 不是永远不改代码，而是频繁变化的部分要易扩展、少修改。
```java
interface Payment {
    void pay();
}

class AliPay implements Payment { ... }
class WeChatPay implements Payment { ... }

// 新增一种支付方式 → 不修改已有类，只新增一个实现
```
### 3. 里氏替换原则（LSP - Liskov Substitution Principle）
> 子类对象必须能替换父类对象，且保证程序逻辑不变。

**说明**：
- 子类不应该破坏父类的契约（行为一致性）；
- 不要滥用继承来复用代码；
- 如果子类行为与父类冲突，就说明它不适合继承，用组合代替；
- 设计接口时，不要让子类被迫实现无意义的方法。
### 4. 接口隔离原则（ISP - Interface Segregation Principle）
> 客户端不应该被迫依赖它不使用的方法。

**说明**：
- 拆分过大的接口，让每个接口专注于一个用途；
- 接口不应承担 “便利函数合集” 的角色；
- 多个小接口比一个大接口更易维护；
- 使用适配器或代理避免过多直接依赖。
```java
interface Reader { void read(); }
interface Writer { void write(); }

class FileStream implements Reader, Writer { ... }
class InputOnlyStream implements Reader { ... }
```
### 5. 依赖倒置原则（DIP - Dependency Inversion Principle）
> 高层模块不应该依赖底层模块，二者都应该依赖抽象。

**说明**：
- 不直接依赖具体类，而依赖接口或抽象类；
- 通过依赖注入（DI）或 IOC 容器实现松耦合；
- 模块之间的连接通过抽象层（契约）沟通。
```java
class OrderService {
    private final Payment payment;
	
    // 通过注入而非直接创建
    public OrderService(Payment payment) {
        this.payment = payment;
    }
}
```
## 二、其他注意点
### 1. SOLID 原则作用
**SRP** 提高可维护性，  **OCP** 提高可扩展性，  **LSP** 保证可靠替换，  **ISP** 减少无关依赖，  **DIP** 降低模块耦合。
### 2. OCP 的度
开闭原则错误做法是所有类都定义成接口 + 实现”，即便永远不会扩展。正确思想是抽象不是提前准备，而是应对变化的副产品。你预期某部分会变化，才加抽象。如果暂时稳定，可以等第一次变化到来时再抽象（延迟抽象）。  
**实践指导**：
- 如果某接口只有一个实现，且未来没有第二种实现的迹象 → 先不抽象；
- 如果你要通过接口进行依赖隔离（比如不同层之间），那就合理；
- 设计时问自己一句话：“我加这层抽象，是为了应对哪个可能变化点？”。
总的来说，OCP 的贯彻点在“变化隔离”，不是“处处抽象”。
### 3. DIP 的度
DIP 的本意是高层依赖抽象，不依赖实现，而不是说“所有对象都必须通过构造函数注入”。如果再加上未使用 IoC 容器的话，手动层层注入会导致初始化链过长，代码杂乱。  
**实践指导**：
- 内部小类可以直接 new（低层逻辑不需要注入）；
- 模块对外暴露的服务层接口要依赖抽象；
- 最外层用 IOC 或装配代码（factory/builder/DI容器）一次性组装好。
总的来说，DIP 要用在模块与模块之间的依赖关系上，而不是每一个类。


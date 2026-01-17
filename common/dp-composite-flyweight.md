---
title: 组合模式、享元模式
tags:
  - common
  - design-pattern
  - composite
  - flyweight
---
## 概述
组合模式和享元模式两者在理念和实现上都不同，但是这两者都已经完成了思想内化，实现被完全拆分替代。在编写程序的绝大多数的场景下（包含业务框架级别的编写场景，如 IoC 容器），已经几乎见不到这两者模式的实现了，两者已经内化为了思想或是最底层的实现。
## 组合模式
组合模式将对象组合成树形结构以表示 “整体-部分” 的层次结构，让客户端对单个对象和组合对象使用统一接口。核心是统一接口 + 递归组合。这就隐含了一个条件就是父子组件的节点行为一致。
```java
interface Component {
    void render();
}

class Button implements Component {
    void render() { ... }
}

class Panel implements Component {
    private List<Component> children;
    void render() {
        for (Component c : children) c.render();
    }
}
```
## 享元模式
享元模式运用共享技术有效地支持大量细粒度对象的复用，以减少内存开销。核心是区分内部状态（可共享，不可变）和外部状态（不可共享，外部传入），将共享部分抽象出来，这样多个对象就可以通过引用的方式共享信息达到降低内存的效果。享元模式一般用于超大数量且相似并且能清晰拆分出内部 / 外部状态的对象，不适合对象数量不多，或是状态高度依赖上下文，难以分离的对象。
### Java 字符串常量池
字符串常量池是一个全局缓存，由 JVM 维护，key 值是字符串的内容，也就是字符串字面量，而 value 值是唯一的 String 实例。如果存在直接返回引用，如果不存在则创建 String 对象，放入池中。
### GUI 中的图标对象共享
```java
class Glyph {
  private final char intrinsic; // 可共享
  public void draw(int extrinsicX, int extrinsicY) { ... } // 外部状态
}
```
## 现状
### 组合模式
组合模式是以统一的树形结构实现迭代调用。但是在现代编程中，语言的容器本身已经十分强大，比如 Java 的 List 已经事实上成为了组合容器，并且函数式 / 流式处理替代了递归的操作，容器本身就能提供这些功能，而且现代业务越来越扁平化，组合模式已经完全内化，模式退化为一种使用约定而非原本的实现模板的定位。到了这个程度，不能说设计模式使用不使用了，因为这类模式已经被拆除了分散在各类更为抽象的编程原则里，而不是设计模式。
### 享元模式
享元模式的管理职责被拆散了，所以在一般日常编写代码的场景，几乎见不到享元模式，而是被各种的工程习惯吸收和取代，原始的 GoF 享元工厂的形式（Flyweight 、ConcreteFlyweight 、FlyweightFactory ）已经淘汰，更多是作为一种思想而存在着，并且 “不可变对象共享” 已经从特定的模式变为当今的编程共识。并且模块、缓存、不可变对象已经在实现层面拆解的享元模式。
#### (1). 模块 + 缓存
现代语言尤其是具有模块的，可以使用模块和缓存结合实现替代享元工厂。
```ts
const fontCache = new Map<string, Font>();

export function getFont(family: string, size: number): Font {
  const key = `${family}-${size}`;
  if (!fontCache.has(key)) {
    fontCache.set(key, new Font(family, size));
  }
  return fontCache.get(key)!;
}
```
- 使用缓存意图一致，但是实现更为简单。并且模块天然单例。
- 没有显式 Flyweight 层级。
- 没有外部/内部状态的教科书划分。
#### (2). 不可变对象 + 引用共享
如果对象是不可变的，那么共享引用本身就是安全的享元。
```java
public record Role(String name) {}

public final class Roles {
    public static final Role ADMIN = new Role("ADMIN");
    public static final Role USER  = new Role("USER");
}

user.setRole(Role.ADMIN);
```
只创建一个状态不可变的对象，零同步成本。这是享元模式的自然态。


















































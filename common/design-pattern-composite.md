---
title: 组合模式
tags:
  - common
  - design-pattern
  - composite
---
## 概述
组合模式将对象组合成树形结构以表示 “整体-部分” 的层次结构，让客户端对单个对象和组合对象使用统一接口。核心是统一接口 + 递归组合。其他的结构型设计模式在代码实现层面可以看做结构简单的组合思想的使用（因为没有 “整体-部分” 的层次结构，只是单纯的组合），以及行为型的桥接模式、状态模式、策略模式都基于此模式。
## 实际场景
### GUI 组件
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

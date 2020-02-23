## 设计模式
### IoC 控制反转
```  
==类A依赖类B，可以在类A里创建B的实例，或通过类B实例作为参数传入类A的函数中 来实现。
==>控制反转可以将这个类间的耦合借助容器，放到容器中来代为管理。这样类A的对B的实际依赖变为通过容器的装饰进来使用。
   @InjectIoC container
   class A:
     private class B b;
   
   Class B:
-->该容器的实现可以参考Spring的IoC类依赖管理配置的实现


```  
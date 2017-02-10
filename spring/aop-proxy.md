# AOP관련 Proxy 정의

Spring AOP는 두가지 Type의 Proxy를 지원하고 있다. 

1. JDK Dynamic Proxy
2. CGLIB Proxy

기본적으로 Spring AOP는 JDK Dynamic Proxy를 사용한다. 이외에 CGLIB Proxy방식도 사용 가능하다. 모델이 인터페이스로 구현되어 있지 않으면 CGLIB을 기본으로 사용한다.

## JDK Dynamic Proxy
J2SE 1.3 부터 제공하는 기능. 메서드 요청을 인터셉트해서 추가적인 행동을 끼워넣을 수 있다. 

_인터페이스에 대한 Proxy만 지원_하기 때문에 클래스에 대한 Proxy를 지원하지 않는다. Proxy기능을 사용하기 위해 인터페이스를 사용해만 하는 제약사항이 있다.

#### 구현되어 있는 애플리케이션에 Proxy기능을 추가할 때
클래스로 구현되어 있다면 인터페이스를 추출한 후 Proxy를 적용해야하는 단점있다. 이렇게 클래스에 적용하고 싶은 경우 `CGLIB Proxy` 사용

Target 클래스에 대한 모든 메서드 호출이 JVM에서 Interceptor한 후 invoke호출. 이 때 JDK의 리플렉션을 이용하여 호출하기 때문에 퍼포먼스가 떨어질 수 있다.




JDK Proxy가 가지는 또 하나의 단점은 Target 클래스에 Proxy를 적용할 때 PointCut에 정보에 따라 Advice되는 메써드와 그렇지 않은 메써드가 존재한다. 그러나 JDK Proxy를 사용할 경우 Target 클래스에 대한 모든 메써드 호출이 일단 JVM에 Intercept한 다음 Advice의 invoke 메써드를 호출하게 된다. 그 후에 이 메써드가 Advice되는 메써드인지 그렇지 않은지를 판단하게 된다. 이 과정에서 JVM에 의하여 Intercept한 다음 invoke 메써드를 호출할 때 JDK의 reflection을 이용하여 호출하게 되는것이다. 이는 Proxy를 사용할 때 실행속도를 상당히 저하시키는 원인이 된다.

Spring 프레임워크에서 JDK Proxy를 사용하고자 한다면 ProxyFactory의 setProxyInterfaces() 메써드에 사용할 인터페이스를 전달하면 JDK Proxy를 이용할 수 있다. 그러나 이 메써드를 통하여 인터페이스를 전달하지 않을 경우 기본적인 Proxy는 CGLIB Proxy가 된다.


## CGLIB Proxy

타겟 메서드가 호출될 때마다 JDK dynamic proxy처럼 런타임시 적용 여부를 결정한다. 

메서드가 최초 호출될 때만 동적으로 Bytecode를 생성하고 다음 호출부터는 재사용하기 때문에 실행속도의 향상을 가져올 수 있다.

인터페이스만 가능했던 JDK dynamic proxy와는 달리 _클래스에 대한 Proxy가 가능_




> Proxying 매커니즘
> 
> Spring AOP는 주어진 타겟 오브젝트에 대한 프록시를 생성하기 위해 JDK dynamic proxy 또는 CGLIB를 사용한다. (선택권이 있어도 JDK dynamic proxy가 우선적)
> 
> 만약 타켓 오브젝트가 최소 하나의 인터페이스를 구현했다면 `JDK dynamic proxy` 가 사용될 것이다. 타겟 타입으로 구현된 모든 인터페이스들은 프록시될 것.
> 
> 만약 타겟 오브젝트가 인터페이스를 구현하고 있지 않다면 `CGLIB proxy`가 생성될 것이다.
> 
> 개발자가 강제로 CGLIB proxy를 사용하고 싶다면 (예를들어, ) 그렇게 할 수 있다. 하지만 여기에는 몇몇 고려해야할 사항들이 있다.
> 
> * final 메서드는 안된다. 재정의가 될 수 없다.
> * 스프링 3.2 버전에서, 더 이상 CGLIB를 프로젝트 classpath에 추가하지 않아도 된다. CGLIB 클래스들은 스프링 프레임워크에 포함된다. 이 말은 즉, JDK dynamic proxy와 같이 단지 실행만 시켜주면 된다.
> * 
> 


----
**참고**
[Spring Documents](https://docs.spring.io/spring/docs/current/spring-framework-reference/html/aop.html#aop-proxying)

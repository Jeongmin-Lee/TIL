# 확장 포인트와 PropertyEditor/ConversionService

## 확장 포인트
* BeanFactoryPostProcessor : 빈 설정 정보 변경
* BeanPostProcessor : 빈 객체 변경

위와 같이 빈 객체

## PropertyEditor

## ConversionService


# Spring AOP(Aspect Oriented Programming)
## 개요
관점 지향 프로그래밍(AOP)은 문제를 바라보는 관점을 기준으로 프로그래밍 하는 기법이다. 공통된 관심사항을 모듈화하여 여러 코드에 쉽게 적용할 수 있도록 도와준다. 이를 구현하기 위해 기존의 OOP 방식으로는 한계가 있어 (상속, 위임 등으로 해결하려 하지만 코중복된 코드 등의 한계 발생) AOP개념이 도입되었다. 그렇기 때문에 OOP와는 반대되는 개념이 아닌 보완을 해주는 개념이라고 볼 수 있다.

Spring IoC 컨테이너에 의존하지 않기 때문에 필요하지 않으면 사용하지 않아도 무방하다. 이러한 특성 때문에 핵심 비즈니스 로직을 변경하지 않고도 공통 관심 기능을 추가, 적용할 수 있다.

> 공통 관심 기능은 주로 **로깅, 트랜잭션, 인증** 등이 있다.

### 용어
* JoinPoint : Advice 적용 가능한 지점(메서드 호출, 값 변경 등)
* PointCut : 실제 Advice가 적용되는 지점(JoinPoint 부분집합)
* Advice : 언제 로직에 적용할지 등의 정의(before, after, around,...)
* Weaving : Advice를 실제 로직에 적용하는 것을 의미
* Aspect : 공통으로 적용되는 기능을 의미(로깅, 트랜잭션 등)

### 3가지 Weaving 방식
* 컴파일 시 : AspectJ에서 사용하는 방식. 컴파일 할 때 알맞은 위치에 공통 코드를 삽입하면 컴파일 결과 AOP가 적용된 클래스파일이 생성 -> 원본 변경됨
* 클래스 로딩 시 : 로딩한 클래스의 바이너리 정보를 변경하여 공통 코드를 삽입한 새로운 클래스 바이너리 코드로 사용하도록 함. -> 원본 변경 X
* 런타임 시 : **프록시**를 이용하여 AOP적용. 소스, 클래스 정보 변경하지 않는다. 

### 스프링에서 AOP
* 스프링은 자체적으로 **프록시 기반의 AOP를 지원**한다.
* 메서드 호출 JoinPoint만 지원.
* 필드 값 변경 등을 이용하려면 AspectJ와 같은 도구를 이용해야 한다.


## 구현 방법
* XML스키마 기반의 POJO클래스를 이용한 방법
* AspectJ에서 정의한 애노테이션 기반
* Spring API를 이용한 구현(많이 사용되진 않는다)

기본적으로 프록시 방식으로 적용된다. 

### Advice 종류
Aspect에 적용가능한 Advice의 종류는 다음과 같다.

* Before : 메서드 호출 전
* After Returning : 메서드가 예외없이 실행된 이 후
* After Throwing : 메서드 예외가 발생했을 때 이 후
* After : 예외 여부 상관없이 메서드 호출 후 
* **Around** : 메서드의 실행 전과 후, 예외 발생 시점 전부 (가장 범용적)


### XML스키마 기반으로 구현하기
구현하는 방법은 아래 순서대로 이루어진다.

1. Dependency 추가
2. 공통 기능 제공할 클래스 정의
3. XML설정으로 Aspect를 정의


#### 1. Dependency 추가
AOP를 적용하기 위해 ```Spring-AOP```, ```AspectJ``` 두 가지 의존을 추가해야 한다.

```xml
<dependency>
	<groupId>org.springframework</groupId>
	<artifactId>spring-aop</artifactId>
	<version>4.3.6.RELEASE</version>
</dependency>
<dependency>
	<groupId>org.aspectj</groupId>
	<artifactId>aspectjweaver</artifactId>
	<version>1.7.4</version>
</dependency>
```
spring-aop대신 context로 추가해도 무방하다. (aop를 이미 의존하고 있기 때문)

#### 2. 공통 기능 제공할 클래스 정의
Advice구현 클래스 정의.

```java
package com.navercorp.test.aop;

import org.aspectj.lang.ProceedingJoinPoint;

public class Profiler {
	
	public Object trace(ProceedingJoinPoint joinPoint) throws Throwable {
		long start = System.currentTimeMillis();
		System.out.println("시작");
		try {
			return joinPoint.proceed();
		} finally {
			System.out.println("종료");
			long finish = System.currentTimeMillis();
			System.out.println("실행시간 : " + (finish - start) + "ms");
		}
	}
}

```
언제 실행될지 어떤 모듈에 정할지 등의 정보는 없고 오로지 공통 수행 기능에 대한 부분만 명시되어 있다.

#### 3. XML설정으로 Aspect를 정의
XML설정 파일에 Aspect관련 설정을 추가한다.

```xml
<bean id="profiler" class="com.xxxx.Profiler" />

<aop:config>
   	<aop:aspect id="traceAspect" ref="profiler">
   		<aop:pointcut expression="execution(public * com.navercorp.test..*())" id="publicMethod"/>
   		<aop:around method="trace" pointcut-ref="publicMethod"/>
	</aop:aspect>
</aop:config>
```
aspect ref는 ```Profiler``` 클래스를 정의한 빈의 id.
pointcut을 정할 때 expression을 활용해서 다양하게 적용할 수 있다.
around의 method는 실제 적용될 메서드 (Profiler에서는 trace) 명을 지정하고 pointcut-ref는 pointcut의 id 입력


## 설정
### XML 설정

## Annotation 설정


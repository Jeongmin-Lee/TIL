# 데이터베이스 테스트 DbUnit..?
데이터베이스와 관련된 테스트를 짜기는 쉽지 않다. 초기 시점의 데이터가 매번 다르고 테스트 수행하면서 데이터가 변경되기 때문에 동일한 테스트를 수행해도 어쩔땐 성공, 어쩔땐 실패하는 경우가 발생한다. 

이와 관련해서 통합테스트 식으로 한 번만 쭉 수행하면 된다는 생각을 가지고 있었지만, 아무리 생각해도 단위테스트는 Idempotent해야할 듯 해서 여러가지 적용을 한적이 있었다.

1. 테스트 하기 전, 데이터베이스 상태를 항상 비워놓고 시작한다. BaseTest를 두고 setUp과정에서 최소 필요한 데이터를 넣는 작업을 한다. 실질적인 테스트 클래스는 이 BaseTest를 상속받으며 ```super.setUp()``` 을 호출하며 데이터를 넣는 작업부터 검증까지 진행한다.
2. 테스트를 위한 임시의 데이터를 정해놓고 스크립트를 작성한다. 테스트 수행 전 매번 이 스크립트를 수행시켜 데이터를 마련한다.

첫 번째 방식은 테스트할 비즈니스 로직이 크고 처리해야할 데이터가 많으면 복잡해진다는 문제가 발생한다. 단일 상속만 허용되므로 BaseTest가 커질 가능성이 있으며 계층화시킨다고 해도 계층 구조가 복잡해진다.

두 번째 방식은 스크립트를 직접 관리해야 한다는 점. 그리고 한 번만 수행 가능하다는 점이 불편했다.

Mock을 사용하는 방식으로 접근해도 되는데 결국은 데이터베이스에 데이터가 잘 들어갔냐 테스트를 해야하므로 개운치가 않았다. TDD책을 보다보니 **DbUnit**이란 것이 이러한 문제에 대해 고민한 듯 보였다.

## 1. DbUnit
일종의 도구로써 단독적으로 쓰기보단 JUnit과 결합해서 사용한다. 핵심 원리는 위에서 언급한 사항과 비슷하다. 초기화 후 스크립트가 정의되어 있는 XML을 테스트 할 때마다 실행시켜 데이터를 세팅한다.

* 독립적인 데이터베이스 연결 지원
* 특정 시점의 상태를 Import/Export (xml, csv파일 지원)
* 데이블, 데이터셋을 서로 쉽게 비교 가능

## 2. Unitils

동일성 검사
```assertReflectionEquals(a, b)```

너그러운 비교

* 순서무시
* 시간, 날짜 비교 무시
* 기본값 필드 비교 무시


프로퍼티 단정문
값이 잘 들어갔는지 getter가 없어도 확인할 수 있다.
**assertPropertyLenientEquals**


### 다양한 모듈 지원
Database, Mock, Spring

* DbUnit모듈

	```@Dataset```, ```@TestDataSource``` 등 애노테이션 지원
	
* Spring 지원 모듈

	```@SpringApplicationContext```, ```@SpringBean``` 등 의존성 주입을 위한 애노테이션 지원
	@ContextConfiguration, @Autowired 사용중이라면 별 이득 없음

* Mock 지원 모듈
	 
## 3. 개발 영역에 따른 TDD작성 패턴
테스트 케이스를 작성할 때 어떤 상황에 접하게 되는지 어떻게 해결해나가는지 알아보자.
### 3.1. 일반 애플리케이션

#### 3.1.1 생성자 테스트

* 굳이 테스트 작성 하지 않는다. 
* 다만, 반드시 갖춰야하는 값을 생성자에 설정하는 경우 부분적으로 작성
* **DB커넥션**과 같이 객체 생성 의미를 넘어 선행조건, 업무로직을 직접 작성하는 경우

#### 3.1.2. DTO 스타일 객체
Getter/Setter 로 이루어진 DTO객체를 테스트하는 경우도 

* 굳이 작성하지 않는다.
* 특정 목적을 가진 **불변객체**의 경우 getter/is 메서드로 작성하는 경우도 있다.
	(isReady, isConnected등)

#### 3.1.3. 닭? 달걀 메서드 테스트
메서드가 서로 맞물려 독립적으로 테스트하기 힘든 경우가 있다.
(add, remove 등 로직과 get, show, is 등의 계열과 짝을 이룰 때)

참석자 클래스 테스트하는 경우
```java
public class AttendeeTest {
	@Test
	public void testAdd() {
		Attendee attendee = new Attendee();
		attendee.add("lee jeongmin");
		assertEquals("lee jeongmin", attendee.get(1));
	}
}
```

add와 get이 맞물려 있다. 별도로 하려고해도 서로 연결되어 독립적으로 테스트 작성 불가한 상황..


**한 번에 실패하는 테스트 하나씩 작성**

이 상황은 이 규칙을 지키기 어려운 경우. 해결책은 3가지있다.
1. 실패 케이스가 두 개인 상태에서 작업(일반적) : 복잡한 코드인 경우는 파악 힘들 수 있음.
2. 안정성이 검증된 제 3의 모듈 이용(가능하다면 권장) : DbUnit과 같은 외부모듈을 이용하는 방법.
3. 리플렉션으로 강제 확인(비추) : 곧잘 깨지기 쉬운 테스트이므로 좋은 테스트가 아님.

#### 3.1.4. 배열 테스트

##### **JUnit4 assertArrayEquals 활용**

기본적으로 순서까지 고려한다.

```java
int[] arrayA = new int[]{1,2,3};
int[] arrayB = new int[]{1,2,3};
assertArrayEquals(arrayA, arrayB);
```

순서고려하지 않는다면 ```Arrays.sort(..)``` 활용
```java
int[] arrayA = new int[]{1,2,3};
int[] arrayB = new int[]{3,1,2};
Arrays.sort(arrayA);
Arrays.sort(arrayB);
assertArrayEquals(arrayA, arrayB);
```

##### **Utilils의 assertReflectionEquals, assertLenientEquals 이용**
```java
assertLenientEquals(arrayA, arrayB);
```

##### **JUnit3 이면 List로 변환하여 비교**
미리 정렬하여 Arrays.asList 로 배열로 변환하여 비교

#### 3.1.5. 객체 동치성
동일성, 동치성 구분하여 생각해야 함.
다르게 생성했더라도 값이 같으면 같게 처리해야 한다. 하지만 assertEqual 수행시 다른 결과가 나옴.

1. 필드를 직접 꺼내서 검사 : 필드가 많으면 번거롭다
2. toString을 구현하여 비교
3. **equals 메서드 구현** : 가장 올바른 방법.
4. Unitils의 assertReflectionEquals 이용

> **assertEquals 메서드 재정의**
> 
> equals, toString 을 재정의하지 않은 써드파티 모듈의 경우 assertEquals 메서드를 재정의하는 것도 방법.
> ```java
> private boolean assertEquals(Car expected, Car actual) {
>     assertEquals(expected.getNum(), actual.getNum());
>     ...
> }
> ```


#### 3.1.6. 컬렉션 테스트
List, Set, Map 등의 컬렉션 테스트.

1. 기본형, 컬렉션의 경우 toString이 기본으로 있기 때문에 assertEquals로 바로 비교
2. 컬렉션에 일반 객체일 경우, toString을 재정의하여 해결


### 3.2. 웹 애플리케이션

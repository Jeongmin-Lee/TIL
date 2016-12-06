# Lambda Expression

## Introduction
람다 표현식(Lambda Expression)은 Java8의 새롭고 중요한 기능이다. 이것은 표현식을 사용하는 하나의 인터페이스 메서드를 표현하기 위해 간결하고 명확한 방법을 제공한다. 람다표현식은 또한 Collection으로 부터 데이터를 추출하고 거르고 반복하는 아주 쉽게 만들 수 있도록 Collection 라이브러리들을 개선했다. 게다가 멀티코어 환경에서 새로운 동시성 기능 성능이 향상된다.

## 람다식(Lambda Expression)
아래코드를 보자.

```java
calculator(new Operator<Integer> {
	public int execute(int a, int b) {
		return a + b;
	}
});
```

여기서 필요한 코드는 연산하는 부분인 a + b가 전부이다.
Java는 기본 타입과 객체만 매개변수로 넘길 수 있기 때문에 이렇게 주저리주저리 클래스를 만들어야 한다. 이를 더욱 간결하게 사용할 수 있도록 Java8에서는 람다표현식을 제공한다.

```java
calculator((int a, int b) -> {
	return a - b;
});
```

위와 같이 문법은 아래와 같다.
> 람다 매개변수 -> 람다 본문

약식으로 다음과 같이 표현할 수 도 있다.

```java
calculator((a, b) -> a - b);
```

약식으로 하게되면 람다식이 **매개변수 타입 추론** 을 할 수 있기 때문에 가능하다. 블럭을 생략할 수도 있으며, return문 제거도 가능하다. ***매개변수가 하나라면 괄호 생략 가능 ***

다음 람다식의 다양한 예시이다.

```java
() -> {}                     // No parameters; result is void
() -> 42                     // No parameters, expression body
() -> null                   // No parameters, expression body
() -> { return 42; }         // No parameters, block body with return
() -> { System.gc(); }       // No parameters, void block body
() -> {
  if (true) return 12;
  else {
    int result = 15;
    for (int i = 1; i < 10; i++)
      result *= i;
    return result;
  }
}                             // Complex block body with returns
(int x) -> x+1                // Single declared-type parameter
(int x) -> { return x+1; }    // Single declared-type parameter
(x) -> x+1                    // Single inferred-type parameter
x -> x+1                      // Parens optional for single inferred-type case
(String s) -> s.length()      // Single declared-type parameter
(Thread t) -> { t.start(); }  // Single declared-type parameter
s -> s.length()               // Single inferred-type parameter
t -> { t.start(); }           // Single inferred-type parameter
(int x, int y) -> x+y         // Multiple declared-type parameters
(x,y) -> x+y                  // Multiple inferred-type parameters
(final int x) -> x+1          // Modified declared-type parameter
(x, final y) -> x+y           // Illegal: can't modify inferred-type parameters
(x, int y) -> x+y             // Illegal: can't mix inferred and declared types
```

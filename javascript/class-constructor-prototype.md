# Class
자바스크립트는 실제 클래스 기능을 지원하지 않는다.
대신 _모조 클래스_ 를 정의.

> 모조 클래스 = 프로토타입 객체 or 생성자 함수를 사용하여 구현 가능

## 생성자

생성자 함수
```js
function Rect(w, h) {
	this.w = w;
	this.h = h;
}
```

```js
function Rect(w, h) {
	this.w = this.w;
	this.h = this.h;
	this.area = function() {
		return this.w * this.h;
	}
}
```


## 프로토타입 & 상속

### 프로토타입 객체
모든 함수에 있는 프로퍼티.
함수가 정의될 때 자동으로 생성되고 초기화된다.
초기값은 프로퍼티가 하나 있는 객체로 지정. `constructor`

만든 클래스는 프로토타입 객체를 상속받는다.
상수나 메서드를 프로토타입으로 빼면서 사용하는 메모리 양을 절감시킬 수 있다.

_만약 프로토타입에 새로운 메서드가 추가된다면, 이미 생성된 인스턴스들도 적용된다_

```js
var r = new Rect(2, 3);
r.hasOwnProperty("w") // true
r.hasOwnProperty("area") // false
"area" in r; // true
```

### 프로퍼티 읽기, 쓰기

객체의 프로퍼티가 있나 검사 -> 프로토타입의 프로퍼티인가 검사

_프로토타입의 상속은 읽기에만 일어난다. 쓰기를 허용할 경우 모든 객체의 프로퍼티가 변경될 수 있다._

프로토타입의 프로퍼티는 모든 클래스가 공유, 객체의 메서드를 정의하기엔 딱임.
자주 사용되는 기본값을 정의해두는 것도 좋은 방법.

### 내장형 타입의 확장
사용자 정의 클래스만 프로토타입 객체가 있는게 아니라 `String이나 Date같은 내장형 클래스에도 프로토타입이 존재`한다. 여기에 값 할당할 수 있다.

```js
String.prototype.endsWith = function(c) {
	...
}
```
처럼 재정의 가능.

> 논란이 있다.
>
> 코어 자바스크립트 API의 사용자 정의 버전을 만들게 됨.
> 직접 로우레벨 부터 프레임워크를 만들어 범용적으로 사용하게 할 목적이 아니면, 
> **내장형 타입의 프로토타입은 건드리지 않는 편이 좋을것이다**

**Object 타입의 프로토타입에 어떤것이라도 추가하지마라**
`{}` 와 같이 빈 객체에도 열거할 프로퍼티가 감지된다.
객체를 연관배열로 사용하는 코드가 작동하지 않기 때문.

> 내장형 타입을 확장하는 기술은 코어 자바스크립트의 네이티브 객체들에서만 작동.
> (웹 브라우저, 자바 애플리케이션 같은 곳에 포함될 때)
> 
> 웹 브라우저 문서 내용을 가리키는 호스트객체. 생성자나 프로토타입이 없으면 확장불가.
> 
> _예외로 건드리는 경우는 브라우저 별 자바스크립트 표준 메서드의 호환성을 맞출 때._

## 클래스 시뮬레이션
자바스크립트는 클래스에 대한 개념은 없다. 하지만 `생성자`와 `프로토타입` 객체를 통해 흉내낼 수 있다.

### 인스턴스 프로퍼티
자신만의 사본.

### 인스턴스 메서드
클래스의 인스턴스 메서드는 생성자의 프로토타입 객체가 가진 프로퍼티에 함수 값을 넣어주는 방법을 통해 정의.

### 인스턴스 메서드와 this
인스턴스 메서드에서 프로퍼티들을 사용하려면 명시적으로 this를 사용해야함.
아니면 `with`를 사용하는 것도 방법이다. 

```js
Rectangle.prototype.area = function() {
	with(this) {
		return w * h;
	}
}
```

### 클래스 프로퍼티
인스턴스와 다르게 하나 존재. 한 개의 사본만 있기 때문에 `전역적`으로 접근. 
프로퍼티에 생성자로 당연히 만들 수 있다.

```js
Rect.UNIT = new Rectangle(1,1);

var sample = Rect.UNIT;
```

### 클래스 메서드
인스턴스 메서드와는 다르다. 클래스 자체를 통해 호출된다.(Java의 static 함수처럼)
`Date.parse()` 같은 것.

this 키워드를 사용하지 않는다. 생성자 함수를 통해 호출되기 때문에 this는 특정 인스턴스 참조하지 않는다. 


### 예시
```js
// 생성자 함수
function Circle(r) {
	// 인스턴스 프로퍼티
	this.r = r;
}

// 인스턴스 메서드
Circle.prototype.area = function() {
	return Circle.PI * this.r * this.r;
}

// 클래스 프로퍼티
Circle.PI = 3.141;

// 클래스 메서드
Circle.Max = function(a, b) {
	if (a.r > b.r)
		return a;
	else 
		return b;
}
```


> 클래스 만들 때
> 
> 1. 생성자 함수 정의
> 2. 프로토타입 객체에 인스턴스 메서드 정의
> 3. 클래스 메서드와 상수, 필요한 클래스 프로퍼티 정의



### Private 멤버
자바스크립트는 `클로저` 를 사용하여 흉내낼 수 있지만 이렇게 하려면 인스턴스마다 접근 메서드가 저장되어 있어야 한다.

```js
function ImmutableRect(w, h) {
	this.getWidth = function() { return w; }
	this.getHeight = function() { return h; }
}

ImmutableRect.prototype.area = function() {
	return this.getWidth() * this.getHeight();
}
```

## 공통적인 메서드
새로운 클래스를 정의할 때 항상 염두해두고 정의해야 하는 메서드들이 있다.

### toString()
prototype 프로퍼티에 추가할 수 있다.

```js
Circle.prototype.toString = function() {
	return "[Circle of r : " + this.r + "]";
}

var c1 = new Circle(35);
alert(c1.toString());
```

### valueOf()
객체를 Number 같은 기본타입으로 변환하려 할 때 호출. 
Number나 Boolean 객체가 서로 같은 기본 타입의 값인 것 처럼 작동하는데 각 클래스는 valueOf() 메서드를 재정의해서 적절한 기본타입의 값을 반환하기 때문.

> 주의
> 
> 객체를 문자열로 변환할 때, 우선순위가 valueOf() > toString() 이다.
> 클래스에 valueOf() 메서드를 정의해 놨다면 _반드시 toString 도 명시적으로 써줘야 한다._



### 비교 메서드
원하는 순서대로 객체를 비교하기 위해 `compareTo` 메서드를 사용한다. 
정렬 시, 0, 1, -1 을 직접 리턴했었는데 compareTo로 쉽게 구현할 수 있다.

## 슈퍼 클래스와 서브 클래스
클래스 계층을 유사하게 구현가능.

`Object` 클래스

* 가장 일반화 되어 있음
* 모든 내장 클래스의 최상위 슈퍼 클래스
* 프로토타입 객체의 상위 클래스이기도 함

적용방법

1. `call()` 메서드를 이용한 생성자 체이닝을 통해 호출
2. 프로토타입을 슈퍼클래스로 지정 : _기본으로 하면 Object를 슈퍼클래스로 받음_
3. 프로토타입 객체가 Person() 로 만들어졌기 때문에 constructor는 이 생성자를 참조. Student의 constructor를 다시 Student로 할당.

```js
function Person(name, gender) {
	this.name = name;
	this.gender = gender;
}

function Student(name, gender, grade, score) {
	
	// 1
	Person.call(this, name, gender);

	this.grade = grade;
	this.score = score;
}

// 2
Student.prototype = new Person();

// 3
Student.prototype.constructor = Student;

```

이런 단계까지 다 해줘야되다니.. 자바보다 서브 클래스를 만드는게 어렵다. 

### 생성자 체이닝
Student 생성자 함수는 상위 클래스 Person의 생성자 함수를 명시적으로 호출했었다. 위의 방법은 너무 길고 수다스럽다.

생성자 체이닝을 통해 간소화 시킬 수 있다.
```js
Student.prototype.superclass = Person;

function Student(name, gender, grade) {
	this.superclass(name, gender);
	this.grade = grade;
}
```

this 를 통해 상위 클래스의 생성자 함수가 호출됨.
_더이상 `apply() 나 call()` 을 사용하지 않아도 됨_

### 재정의된 메서드 호출
상위 클래스에서 정의된 메서드를 하위클래스에서 재정의 할 때,

상위 클래스에 정의된 메서드는 하위 클래스 프로토타입 객체의 프로퍼티.
직접 호출할 수 없다.

`apply()`로 호출해야 한다.

```js
Student.prototype.toString = function() {
	return this.grade + " : " + this.superclass.prototype.toString.apply(this);
}
```

## 상속없이 확장
서브 클래스화와 상속이 클래스 확장하는 유일한 방법이 아님.
또 다른 방법이 존재함. `함수들을 한 클래스에서 다른 클래스로 복사할 수 있다`.

```js
function borrow(borrowFrom, addTo) {
	var from = borrowFrom.prototype;
	var to = addTo.prototype;

	for (m in from) {
		if (typeof from[m] != "function")
			continue;

		to[m] = from[m];
	}
}
```

## 객체 타입 판단
타입제약이 느슨하다. 임의의 값이 어떤 타입에 속하는지 알 수 있다.

* `typeof`
	`typeof undefined` : undefined
	`typeof null` : object

### instanceof & constructor
기본타입이나 함수가 아니라 객체일 때, 더 많은 정보를 얻기위해 `instanceof` 사용.

`constructor` : 정의한 객체가 특정 클래스의 인스턴스이고 그 클래스의 하위 클래스의 인스턴스는 아닌 걸 확인할 때.

```js
var d = new Date();
var realObject = d.constructor == Object // false
```


### 객체 타입 지정을 위한 Object.toString()
instanceof, constructor는 이미 알고있는 클래스만 확인 가능하다는 단점.
모르는 객체를 조사할 때 주로 사용한다.

```js
Object.prototype.toString.apply(s);
```
항상 기본 toString을 호출.

### 오리 타이핑
객체가 다른 클래스에서 메서드를 빌려왔는지 검사



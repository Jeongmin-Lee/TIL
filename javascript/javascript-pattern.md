# 함수

## 콜백패턴

```js
function writeCode(callback) {
	...
	callback();
}
```


콜백의 유효범위에서 콜백이 객체의 메서드인 경우가 많다. 
콜백 메서드가 자신이 속해있는 객체를 참조하기 위해 `this`를 사용하면 _예기치 않는 동작이 있을 수 있다._

콜백함수와 콜백이 있는 객체를 전달하고, `call` 메서드로 바인딩 한다.


## 즉시 실행 함수

함수가 선언되자마자 실행되도록 하는 문법.
```js
(function () {
	alert('watch out!');
}());
```
구성

* 함수 표현식으로 선언
* 즉시 실행되도록 `()` 를 추가
* 전체 함수를 괄호로 감싼다. 

객체 프로퍼티를 정의할 때도 사용.

전역변수를 남기지 않고 작업할 수 있어서 `임시변수가 전역변수를 어지럽히지 않는다.`

## 즉시객체 초기화
위와 비슷하게 `init()` 메서드를 실행해 객체를 사용.
일회성 작업에 적합하다. 완료되면 객체에 접근할 수 없음. 접근하고 싶다면 init마지막에 `return this;` 를 추가하면 됨


## 함수 프로퍼티 - 메모이제이션 패턴
함수 프로퍼티에 결과값을 캐시할 수 있다. 다음 호출 시 복잡한 연산을 거치지 않아도 되므로 반복을 줄인다. 

함수이름, `arguments.callee`

## 설정 객체 패턴
깨끗한 API를 제공하는 방법.
함수의 전달인자가 많을 수 있다. 순서도 헷갈리기 때문에 설정 객체를 이용하면 편함.

```js
var conf = {
	username: "test",
	....
}
```

말그대로 넘길 설정값들을 객체로 만들어 객체를 넘겨버리도록 함.

DOM엘리먼트나 CSS스타일 지정할 때 유용.

## 커리(Curry)
커링

### 함수적용
함수형 프로그래밍에서 함수를 호출한다 기 보단 `적용한다` 의 개념으로

```js
sayHi.apply(null, ["hi"]);

sayHi.call(null, "hi");
```

첫 번째 인자는 this와 바인딩할 객체, null이면 전역객체와 바인딩.

### 커링(Currying)
함수를 커링한다..?
커링은 함수를 변형하는 과정. 한 함수가 있으면 부분 적용을 처리하는 함수.

```js
function add(x, y) {
	var oldx = x, oldy = y;
	if (typeof oldy === "undefined") {
		return function(newY) {
			return oldx + newY;
		}
	}

	return x + y;
}


// 
add(3)(5) // 8

var add2000 = add(2000);
add2000(10) // 2010
```

좀 더 개선된 add함수의 커링화
```js
function add(x, y) {
	if (y === "undefined") {
		return function(y) {
			return x + y;
		};
	}

	return x + y;
}
```


좀 더 범용적인 함수를 만들 수 있음.

> 커링을 사용해야 할 경우
> 
> 함수 호출 시 대부분의 매개변수가 비슷할 때 적합하다.
> 일부를 적용해서 동적으로 함수를 생성하고 필요한 부분을 추가적으로 저장하면 됨


# 객체 생성 패턴
자바스크립트는 언어적으로 모듈 패키지, Private 프로퍼티, 스태틱 멤버 등을 위한 기능이 없다. 이를 구현하는 패턴을 적용

## 네임스페이스 패턴
필요한 전역 변수의 개수를 줄이고 과한 접두어를 사용하지 않고 이름이 겹치지 않게 해줌.

전역 전용 객체를 지정하여 모든 함수와 변수를 이 전역 전용 객체의 프로퍼티로 지정.
```js
var MYAPP = {};
MYAPP.some_var = 1;
...

```

### 단점
* 전부 접두어를 써야하기 때문에 코드량이 많아짐
* 전역 인스턴스가 하나라서 한 부분이 수정되어도 전역 인스턴스를 수정함. 나머지 기능들에 영향이 감
* 이름이 중첩되고 길어짐으로 판별을 위한 검색 작업이 길고 느려진다. (대안 : 샌드박스 패턴)

## 범용 네임스페이스 함수
네임스페이스 생성하거나 프로퍼티 추가하기 전에 먼저 존재여부를 확인한다.

```js
// 이미 존재하는 것들도 갱신될 수 있다...
var MYAPP = {};

// 개선
if (typeof MYAPP === "undefined") {
	var MYAPP = {};
}

// 개선을 개선
var MYAPP = MYAPP || {};
```

하지만 _추가되는 확인작업으로 인해 상당량의 중복 코드가 발생_. (MYAPP.modules.a 인 경우 세 번 체크)

네임스페이스 생성의 실제 작업을 맡을 재사용 가능한 함수를 만들면 편하다. (범용 네임스페이스 함수)

이 함수를 `namespace()` 라 하고 사용한다면,

```js
// namespace 함수
MYAPP.namespace = function (ns_string) {
	var parts = ns_string.split('.'),
		parent = MYAPP,
		
		...

	
}


// 활용
var module2 = MYAPP.namespace('MYAPP.modules.module2');

```
아무리 긴 네임스페이스라도 간결하게 사용할 수 있다.

## 의존관계 선언 
자바스크립트 라이브러리는 네임스페이스 지정하여 모듈화되어 있어서 필요한 모듈만 골라쓸 수 있다.

함수나 모듈 최상단에 의존하는 모듈을 선언하는 것이 좋다. 지역변수를 사용해서 가리키게 함.


## 비공개 프로퍼티와 메서드
자바스크립트는 private, protected, public 등의 프로퍼티를 나타내는 별도의 문법이 없다.

객체의 모든 멤버는 public.

## 비공개 멤버
별도의 문법은 없지만 클로저를 사용해서 구축 가능.

```js
function Gadget() {
	var name = "android";
	var getName = function () {
		return name;
	}
}
```

`getName` 은 특권 메서드라 할 수 있다.

하지만 단점이 있다.
비공개 멤버라도 특권 메서드에서 바로 반환하면 값이 아닌 참조만 반환되기 때문에 변경될 수 있다.

## 객체 리터럴과 비공개 멤버
지금까지 생성자로 생성한 방법을 다뤘음.
객체 리터럴로 생성한 경우는 어떻게 해야할까

`익명 즉시 실행 함수` 를 추가하여 클로저를 만든다.

```js
var myobj = (function () {
	var name = "my, ";
	
	return {
		getName: function() {
			return name;
		}
	};
}());

myobj.getName();
```
모듈패턴의 기초

## 프로토타입과 비공개 멤버
생성자 사용 -> 새로운 객체 만들때마다 비공개 멤버가 매번 재생성됨.
중복 없애고 메모리 절약하려면 _공통 프로퍼티와 메서드를 prototype에 추가_

```js
function Gadget() {
	var name = 'iPOd';
	
	this.name = function() {
		return name;
	}
}

Gadget.prototype = (function() {
	var browser = "xx";
	
	return {
		getBrowser: function() {
			return browser;
		}
	}
}());

var toy = new Gadget();
toy.getName();    // 인스턴스 특권 메서드
toy.getBrowser(); // 프로토타입 특권 메서드
```


## 비공개 함수를 공개 메서드로 노출
노출 패턴

객체 리터럴 안에서 비공개 멤버를 만드는 패턴에 기반하여 생성

```js
var myarray;

(function() {
	var str = ..;
	
	function isArray(a) {
		return toString.call(a) === str;
	}

	function indexOf() {
		...
	}

	// 
	myarray = {
		isArray: isArray,
		indexOf: indexOf
	}
}
```

공개해도 괜찮은 함수는 myarray에 지정됨.


## 모듈 패턴

* 네임스페이스 패턴
* 즉시실행 함수
* 비공개 멤버, 특권 멤버
* 의존 관계 선언

를 조합한 것이다.

1. 네임스페이스 설정, 범용 네임스페이스 함수를 이용한 정의
2. 모듈 정의. 비공개 함수로 한다면 즉시 실행 함수로 비공개 유효범위를 만든다.
즉시 실행함수가 반환하는 결과는 모듈의 공개 API

### 모듈 노출 패턴
모듈 내 비공개 메서드를 유지하고 최종족으로 공개할 메서드만 골라서 노출하는 것.

비공개 프로퍼티를 설정했으면 최종족으로 공개할 메서드를 리턴한다.

```js
MYAPP.array = (function() {

}());
```

### 생성자를 생성하는 모듈
모듈을 감싼 즉시 실행 함수의 리턴값이 객체가 아닌 함수를 반환하면 된다.

### 모듈에 전역변수 가져오기

1. 모듈을 감싼 즉시 실행 함수에 인자를 전달하는 방법
2. 전역 객체 자체를 전달.


## 샌드박스 패턴
네임스페이스 패턴의 아래 단점을 해결

* 전역객체가 단 하나의 전역변수에 의존. 한 페이지에서 동일한 애플리케이션이나 라이브러리를 실행 할 수 없다.
* . 으로 연결된 긴 이름 써야하고 런타임에는 탐색 작업을 거쳐야 함.

어떤 모듈이 다른 모듈과 그 모듈의 샌드박스에 영향을 미치지 않고 동작할 수 있는 환경을 제공.

### 전역 생성자
샌드박스의 유일한 전역은 생성자.

```js
Sandbox(['ajax', 'event'], function(box) {
	// ...
});
```

콜백 함수로 코드를 감싸기 때문에 전역 네임스페이스를 보호.


### 모듈 추가

### 생성자 구현


## 스태틱 멤버

### 공개 스태틱 멤버
```js
var Test = function () {
	...
}

// 스태틱 메서드
Test.isTest = function() {
	return "isTest";
}

// 인스턴스 함수
Test.prototype.isSimple = function () {
	return this.v;
}
```

### 비공개 스태틱 멤버
* 동일한 생성자 함수로 생성된 객체들이 공유하는 멤버
* 생성자 외부에서는 접근할 수 없음.

Gadget 생성자 안에 conter 라는 비공개 스태틱 멤버를 구현해보자
```js
var Gadget = (function () {
    var counter = 0;
    return function () {
        document.write(counter++);
    }
})();
```

### 객체 상수
```js
Person.HEIGHT_AVG = 173;
```

## 체이닝 패턴
연쇄적으로 메서드를 호출할 수 있게 하는 패턴

```js
var test = {
	value: 1,
	add: function(v) {
		this.value += v;
		return this;
	}

	shout: function() {
		alert("value is " + value);
	}
}
	
// 
test.add(33).shout();
```

`this` 를 리턴하면서.

* 장점 : 코드 간결, 하나의 문장처럼 쓸수 있으
* 단점 : 디버깅하기 힘듬

## method()
function 에 체이닝으로 메서드를 정의할 수 있는 함수.
보통 `prototype`을 이용하여 생성하지만 이 방식으로 정의할 수 있다.

```js
var Person = function(name) {
	this.name = name;
}.method('getName', function() {
	return this.name;
});
```


# 코드 재사용 패턴

## 클래스 방식의 상속패턴 - 생성자 빌려쓰기
자식에서 부모로 인자를 전달하지 못했던 문제점들을 해결할 수 있다.
`apply`, `call` 메서드를 활용한다.

```js

function Parent() {
	this.text = ['ss', '3e'];
}

function Child() {
	Parent.call(this);
}

```

Child에 text 프로퍼티가 생성되는데 이는 복사본이다. 


## 프로토타입 체인


## 클래스 방식의 상속 패턴 #3 - 생성자 빌려쓰고 프로토타입 지정

apply로 생성자 빌려써도 프로토타입은 상속되지 않는다.

이를 해결하기 위해 위 작업을 두번 진행.

1. apply를 통한 생성자 빌려쓰기
2. 해당 프로토타입을 부모 생성자로

```js
function Child(a, b, c, d) {
	Parent.apply(this, arguments);
}

Child.prototype = new Parent();
```

부모 생성자를 비효율적으로 두 번 호출하는 점은 단점.


## 클래스 방식의 상속 패턴 #4- 프로토타입 공유
위 방식은 다 좋은데 부모 생성자를 두 번 호출한다. 공유가 되도록  프로로타입을 걸어준다. 이 방식은 부모 생성자를 한 번도 호출하지 않는다.

```js
A.prototype = B.prototype;
```

체인 검색이 짧고 간단하지만, 상속 받은 누군가가 수정하면 전부 영향을 미친다.


## 클래스 방식의 상속 패턴 #5 - 임시 생성자
프로토타입 체인의 이점은 유지하면서 동일한 프로토타입을 공유할 때의 문제를 해결하기 위함.

빈 함수를 두어서 `Proxy` 기능을 맡게 한다.

```js
function inherit(C, P) {
	var F = function() {};
	F.prototype = P.prototype;
	C.prototype = new F();
}
```

1. 상위 클래스 저장
부모 원본에 참조를 추가. (uber)

2. 생성자 포인터 재설정
생성자 함수를 가리키는 포인터를 재설정한다. 설정하지 않으면 모든 자식 객체의 생성자는 `Parent()` 로 지정돼 있을 것이다. 유용성이 떨어진다. 




### 클래스 방식의 상속 패턴 완결하는 최종 버전
```js
function inherit(C, P) {
	var F = function() {};
	F.prototype = P.prototype;
	C.prototype = new F();
	C.uber = P.prototype;
	C.prototype.constructor = C;
}
```

호출 시 F 프록시 객체를 매번 생성한다. 즉시 호출 함수를 통해 최적화해보자.

임시 생성자는 한 번만 만들어두고 임시 생성자의 프로토타입만 변경한다.

```js
var inherit = (function() {
	var F = function() {};
	return function(C, P) {
		F.prototype = P.prototype;
		C.prototype = new F();
		C.uber = P.prototype;
		C.prototype.constructor = C:
	}
})();
```

클로저가 형성되면서 프록시 함수 F를 저장한다.


## 프로토타입을 활용한 상속

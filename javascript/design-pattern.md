# Javascript 디자인 패턴
## 1. 싱글톤 패턴
특정 클래스나 인스턴스를 오직 하나만 유지.

자바스크립트는 클래스가 없고 _오직 객체_만 존재.
즉 새로 객체를 만들면 다른 객체와도 같지않아 **이미 싱글톤**.

```js
var a = {
	k: 1
};

var b = {
	k: 1
};

a == b  // false
a === b // false
```
값이 같아도 다른 객체 취급.
_객체 리터럴을 이용해 객체 생성할 때마다 싱글톤 만드는 것이다._

### 스태틱 프로퍼티에 인스턴스 저장

```js
function Singleton() {
	if (typeof Singleton.instance === "object") {
		return Singleton.instance;
	}
	
	// 정상적으로 진행 
	this.a = 0;
	..

	// 인스턴스 캐시
	Singleton.instance = this;

	return this;
}
```

클래스 프로퍼티 instance를 이용한 방법.
instance가 공개되어 있다는 것이 단점이다. 다른 시점에서 변경될 수 있음.

### 클로저에 인스턴스 저장
클로저를 이용해 단일 인스턴스를 보호하는 방법.

```js
function Singleton() {
	
	// 캐싱
	var instance = this;
		
	// 정상적으로 진행 
	this.a = 0;
	..

	// 생성자 재작성
	Singleton = function() {
		return instance;
	}
}
```

첫 호출 시 캐싱을 하고, 클로저를 통해 생성자 재정의
다음 호출 시 재작성된 생성자로 호출된다. 클로저로 물고있는 instance를 참조.

단점 : 재작성된 함수는 재정의 시점 이전에 원본 생성자에 추가된 프로퍼티를 잃어버린다는 점이다.

`Singleton` 클래스의 프로토타입에 뭔가를 추가해도 연결되지 않는다.

```js
Singleton.prototype.m = true;

var a = new Singleton();

Singleton.prototype.test = function() {
	return "test";
}

var b = new Singleton();
```

a, b 는 미리 정의한 프로토타입 m을 가지고 있다.
한 번 호출 후 추가로 정의한 test 메서드는 반영되지 않는다.

> 한번 생성된 constructor가 재정의된 생성자가 아닌 원본 생성자를 가리키고 있기 때문


_해결방법_
생성자 메서드에서 prototype과 constructor를 재지정하는 방법

```js
function Singleton() {
	var instance;

	Singleton = function Singleton() {
		return instance;
	}

	// prototype 프로퍼티 변경
	Singleton.prototype = this;
	
	instance = new Singleton();
	instance.constructor = Singleton;

	...

	return instance;
}
```

또는 즉시 실행함수로 감싸는 방법.
비공개 instance를 가리키는 방식

```js
var Singleton;

(function() {
	var instance;

	Singleton = function Singleton() {
		if (instance) {
			return instance;
		}

		instance = this;

		...
	};
})();

```


## 2. 팩토리 패턴
객체들을 생성하는 것이 목적.

* 비슷한 객체를 생성하는 반복작업 수행
* 사용자가 컴파일 타임에 구체적인 타입을 모르고도 객체를 생성하도록

클래스 내부 또는 스태틱 메서드로 구현한다.

```js
// 부모
function CarMaker() {}

// 스태틱 메서드
CarMaker.factory = function(type) {
	var constr = type,
		newCar;

	if (typeof CarMaker[constr] !== "function") {
		// 예외 발생
	}

	// 존재 확인하면 부모 상속
	// 상속은 단 한번만 수행
	if (typeof CarMaker[constr].prototype.drive !== "function") {
		CarMaker[constr].prototype = new CarMaker();
	}

	newCar = new CarMaker[constr]();
	return newCar;
};

CarMaker.SUV = function() {
	this.doors = 24;
}

...

```

## 3. 반복자 패턴
객체는 일종의 집합적인 데이터를 가진다.
개별 요소에 쉽게 접근할 방법이 필요함.

객체는 next() 메서드를 제공. next()를 연이어 호출하면 다음 요소에 접근하여 반환.

```js
var e;
while (e = agg.next()) {
	// e로 작업
	...
}

// 

while (agg.hasNext()) {
	console.log(agg.next());
}
```

다음으로 사용할 index를 비공개로 들고있어야 한다.

```js
var agg = (function() {
	var index = 0,
		data = [1,2,3,4,5],
		length = data.length;

	return {
		next: function() {
			var element;
			if (!this.hasNext()) {
				return null;
			}

			element = data[index];
			index = index + 1;
			
			return data[index];
		},
		hasNext: function() {
			return index < length;
		}
	}
})();

```

여러 차례 반복 순회할 수 있다. 추가로 메서드를 제공할 수 있다.

* rewind() : 포인터 처음으로 되돌리기
* current() : 현재 포인터 인덱스에 해당하는 요소 리턴


## 4. 데코레이터 패턴
런타임시 부가적인 기능을 객체에 동적으로 추가할 수 있다.
기대되는 행위를 사용자화하거나 설정할 수 있다.
평범한 객체로 시작하다가 동적으로 사용 가능한 장식자들 후보 중에서 원하는 것을 골라 객체에 기능을 추가해 나갈 수 있다.

### 사용 방법
물건 파는 기능을 구현할 때, 판매건은 sale 객체가 된다.
각 지방마다 가격을 계산하는 방식이 다른데 이러한 기능들을 동적으로 추가(장식)할 수 있다.

```js
var sale = new Sale(100);
sale = sale.decorate('tax');     // 세금 추가
sale = sale.decorate('money');   // 통화 형식 지정
sale.getPrice();   // "$110.22"
```

### 구현1
모든 장식자 객체에 특정 메서드를 포함하여 메서드를 덮어쓰게 만드는 방법.

각 장식자는 이전의 객체에서 기능이 추가된 객체를 상속.

```js
// 1. 생성자, 프로토타입 메서드
function Sale(price) {
	this.price = price || 100;
}

Sale.prototype.getPrice = function() {
	return this.price;
}


// 2. 장식자 객체들을 클래스 프로퍼티로 구현
Sale.decorators = {};
Sale.decorators.tax = {
	getPrice: function() {
		var price = this.uber.getPrice();
		price = ...
		return price;
	}
};

Sale.decorators.money = {
	getPrice: function() {
		return "$" + this.uber.getPrice().toFixed(2);
	}
}


// 3. decorate() 구현
Sale.prototype.decorate = function(decorator) {
	var F = function() {};
	
	// decorator의 재정의된 함수를 불러오기 위함
	var overrides = this.constructor.decorators[decorate];
	var newObj;

	F.prototype = this;
	newObj = new F();
	newObj.uber = F.prototype;

	// overrides의 프로퍼티를 newObj에 복사하고 리턴
	for (var i in overrides) {
		if (overrides.hasOwnProperty(i)) {
			newObj[i] = overrides[i];
		}
	}
	
	return newObj;
};

```

### 구현2 - 목록을 사용
상속을 사용하지 않고 목록을 활용.
이전 메서드의 결과를 다음 메서드에 매개변수로 전달.

장식 취소나 제거가 쉽다.

```js
function Sale(price) {
	this.price = price || 100;

	// 데코레이터들의 목록을 관리할 배열
	this.decorators_list = [];
}


// 2. Sale 클래스 프로퍼티로 데코레이터 선언
Sale.decorators = {};
Sale.decorators.money = {
	getPrice: function(price) {
		return "$" + price.toFixed(2);
	}
};
...

// 3. decorate 메서드 정의. 목록에 추가하는 역할
Sale.prototype.decorate = function(decorator) {
	this.decorators_list.push(decorator);
}

// 4. Sale의 getPrice 메서드를 정의
Sale.prototype.getPrice = function() {
	var price = this.price,
		i,
		max = this.decorators_list.length,
		name;
	
	// decorator의 목록을 검사해서 price를 가져온다
	for (i = 0; i < max; i++) {
		name = this.decorators_list[i];
		price = Sale.decorators[name].getPrice(price);
	}
	
	return price;
}
```


## 5. 전략 패턴
런타임에 알고리즘을 선택할 수 있게 해준다.
보통 입력양식 폼에 대한 유효성 검사에 쓰인다.

데이터 유효성 검사 예제

* 검증할 데이터
```js
var data = {
	first_name: "jm",
	last_name: "Lee",
	age: 15,
	username: "test"
}
```

* 어떤 데이터를 받아들일지 유효성 검사기 설정
```js
validator.config = {
	first_name: 'isNonEmpty',
	age: 'isNumber',
	username: 'isAlphaNum'
};
```

* 유효성 검사기(validator) 구현
설정에 정의한 이름의 인터페이스를 구현
```js
validator.types.isNonEmpty = {
	validate: function(value) {
		return value !== "";
	},
	instructions: "이 값은 필수"
};

validator.types.isNumber = ...
validator.types.isAlphaNum = ...
```

* 유효성 검사기(validator) 구현
```js
var validator = {
	// 검증 알고리즘 인터페이스 들
	types: {},

	// 에러 메시지들
	messages: [],

	// 검사 설정
	config: {},

	validate: function(data) {
		var i, msg, type, checker, result_ok;
		...
		
		// 데이터 필드를 순회하면서 데이터가 i 프로퍼티를 가지고 있다면
		for (i in data) {
			if (data.hasOwnProperty(i)) {
				type = this.config[i];
				checker = this.types[type];

				// 예외처리
				if (!type) {
					...
				}
				...

				// 데이터의 각 프로퍼티 별로 검증
				result_ok = checker.validate(data[i]);
			}
		}
	},

	hasErrors: function() {
		return this.messages.length !== 0;
	}
};
```


## 6. 퍼사드 패턴
객체에 대한 인터페이스를 제공.
메서드를 짧게 유지하고 하나의 메서드가 너무 많은 일을 하지 않도록 해야 하는 것이 설계 상 좋은 습관.
_하지만, 이렇게 하면 메서드 수가 폭발적으로 증가할 수 있다._

두 개 이상의 메서드가 함께 호출되는 경우가 많으면,
하나로 묶어주는 새로운 메서드로 만드는 것이 좋다.

만약
```
stopPropagation();
preventDefault();
```

두 개의 메서드가 있을 때, 다른 목적이지만 함께 호출되어야 한다.
이럴 때 _함께 호출하는 퍼사드 메서드를 생성하는 것이 좋다._

```js
var myevent = {
	...
	stop: function(e) {
		e.preventDefault();
		e.stopPropagation();
	}
}
```
설계 변경과 리팩터링 수고를 덜어준다.
객체의 API역할을 하는 퍼사드를 생성해 적용할 수 있다. 기존 객체를 완전히 교체하기 전에 최신 코드가 새로운 API를 사용하면, 최종 교체할 때 변경폭을 줄일 수 있다.


## 7. 프록시 패턴
하나의 객체가 다른 객체에 대한 인터페이스로 동작.

> * 퍼사드 : 메서드 호출 몇 개를 결합 시켜 편의 제공
> * 프록시 : 클라이언트 객체와 실제 대상 객체 사이에 존재, 접근 통제

성능 개선에 도움을 준다.
왜? 실제 대상 객체를 보호하여 되도록 일을 적게 시키기 때문.
구체적으로 `lazy한 초기화`.
초기화의 경우 비용이 발생하는데, 최초 초기화 요청을 대신 받지만 실 `객체가 정말로 사용되기 전까지는 요청 전달하지 않는다.`

애플리케이션의 응답성을 향상 시킴.

### 예시
#### 동영상 재생 애플리케이션
동영상 목록들을 프록시가 없다면 매번 가져와야 한다. 프록시가 있으므로 횟수를 줄일 수 있다.

Videos <--> HTTP : 3번 요청 시 3번의 id 요청 / 3번의 응답이 발생
Videos <--> Proxy <--> HTTP :
프록시에 id요청을 모아놓은 후 보내고, 한번에 응답을 받는다. 프록시는 응답을 각각 나눠준다.

이러한 방식으로 라운드 트립을 줄일 수 있다.


1. HTTP로 직접 호출하지 않고 프록시로 요청.
2. 50ms 안에 다른 호출이 들어오면 하나로 병합
3. 하나로 받은 Id들을 대기열(큐)에 모아놓고 HTTP 요청 후 비운다.(flush)
4. 응답 후 콜백

proxy의 코드를 간략하게
```js
var proxy = {
	ids: [],
	delay: 50,
	timeout: null,
	callback: null,
	context: null,

	makeRequest: function(id, callback, context) {
		this.ids.push(id);

		this.callback = callback;
		...

		// timeout 설정
		if (!this.timeout) {
			this.timeout = setTimeout(function() {
				proxy.flush();
			}, this.delay);
		}
	},
	
	flush: function() {
		http.makeRequest(this.ids, "proxy.handler");

		// timeout, queue비움
		this.timeout = null,
		this.ids = [];
	},
	
	handler: function() {
		..
	}
	
}
```


### 프록시 사용해서 요청 결과 캐시
프록시 내에 캐시 프로퍼티를 정의하여 `요청 결과를 캐싱`할 수 있다. 

> **Videos <--> Proxy <--> HTTP**
> 
> 1. Proxy로 보낸 후 HTTP로 보낸다.
> 2. 요청을 받아 `프록시 캐시`에 저장하고 리턴한다.
> 3. 요청을 받을 때 프록시 캐시에 이미 결과가 있나 확인한다.
> 4. 있으면 캐시에서 바로 내려주고, 없으면 1번 작업 반복


만약 HTTP쪽 원본이 바뀌면, 캐시와 어떻게 동기화??


## 8. 중재자(Mediator)
객체간의 결합도를 낮추고 유지보수를 쉽게 한다.
객체간 직접 통신하지 않고, `중재자 객체` 를 거친다.
(e.g. 자신의 상태가 변경될 때 중재자에 알릴 때, 중재자는 변경분을 알아야 하는 객체에게 알린다)

옵저버랑 유사?

### 예시
_두 명의 플레이어 중 30초 동안 더 많이 버튼을 누르는 플레이어가 이기는 게임_

* 플레이어 객체 정의
* Scoreboard 객체 정의
* 중재자(Mediator) 객체 정의

#### 플레이어
```js
function Player(name) {
	this.name = name;
	this.points = 0;
}

Player.prototype.play = function() {
	this.points += 1;

	// 버튼 눌렀을 때 점수 증가 후 중재자 호출
	mediator.played();
}
```

#### 스코어보드
```js
var scoreboard = {
	...
	update: function(score) {
		for (i in score) {
			// 점수 표시
		}
	}
};
```


#### 중재자(Mediator)
중재자에 포함되어야 하는 데이터

* 플레이어들의 목록 관리
* 초기화 기능
* 버튼을 눌렀을 때 반영할 played 기능
* 키 입력 받았을 때 핸들링

```js
var mediator = {
	players: {},

	// 초기 플레이어 설정
	setup: function() {
		var players = this.players;
		players.home = new Player('home');
		players.guest = new Player('guest');
	}

	// 버튼 클릭이 일어났을 경우 보드판 갱신
	played: function() {
		var players = this.players,
    		score = {
        	Home: players.home.points,
          Guest: players.guest.points
        };
        
  	scoreboard.update(score);
  },

	// key event
	keypress = function(e) {
		if (e.which == "1번 키") {
			mediator.player.home.play();
			return;
		}
		if (e.which == "0번 키") {
			mediator.player.guest.play();
			return;
		}
	}
}
```

## 9. 감시자(Observer) 패턴
클릭과 같은 이벤트를 받아 전달할 때, 알려야하는 객체들에게 변경사항을 알릴 때 Publisher/Subscriber 패턴이라고 한다.
MQTT같은 메시지 프로토콜에서 사용되는 패턴.

주요 목적은 객체간의 결합도를 낮추기 위함.
Publisher는 구독자 즉, 감시자(Observer) 가 되고, 관찰되는 객체는 발행자, 감시대상(subject).

### 잡지 구독
잡지를 구독한 사람들에게 잡지를 발행 할 때마다 알려준다.

* subscriber : 구독자
* publisher : 발행자

두 종류가 있고 발행자는 구독자들의 목록을 가지고 있어야 한다. 발행자가 가지고 있어야할 정보와 메서드 목록을 보면,

* subscribers : 구독한 사람들의 목록(장부)
* subscribe() : 구독 요청. 목록에 추가
* unsubscribe() : 구독 취소, 목록에서 제거
* publish() : 구독자들에게 알림


### 구현
#### Publisher
```js
var publisher = {
	// 구독자 목록
	subscribers: {
		any: []
	},
	
	subscribe: function(fn, type) {
		..
		this.subscribers[type].push(fn);
	},
	unsubscribe: function(fn, type) {
		..
		this.subscribers[type].
	},
	publish: function(publication, type) {
		...
		this.visitSubscribers('publish', publication, type);
	},
	visitSubscribers: function(action, arg, type) {
		...
		
		// publish 역할을 하거나
		// unsubscribe하는 자를 찾아 목록에서 제거
		for (i = 0; i < max; i++) {
			if (action == 'publish') {
				subscribers[i](arg);
			} else {
				if (subscribers[i] === arg) {
					subscribers.splice(i, 1);
				}
			}
		}
	}	
};
```

구현 후 객체를 받아 `publisher` 의 메서드들을 복사하여 발행자 객체로 변경한다.

```js
function makePublisher(o) {
	var i;
	for (i in publisher) {
		if(publisher.hasOwnProperty(i) && ..) {
			o[i] = publisher[i];
		}
	}
	o.subscribers = {any: []};
}
```

Paper 라는 객체를 생성하여 makePublisher로 변경하면 된다.

#### Subscriber
구독자를 별도로 만든다.

```js
var jane = {
	drinkCoffee: function(paper) {
		// TODO:
	},
	sundayPreNam: function(monthly) {
		// TODO:
	}
};
```

```js
paper.subscribe(jane.drinkCoffee);
paper.subscribe(jane.sundayPreNam, 'monthly');
```
와 같이 paper의 구독자 목록에 jane을 추가한다.

jane뿐만 아니라 느슨하게 수많은 구독자를 추가할 수 있음.


> **중재자 패턴과의 다른점**
>
> 중재자 객체가 다른 객체에 대해 정확히 알아야만 했다. 즉 결합도가 높아질 수 밖에없는데,
>
> 옵저버 패턴은 객체를 알지 않아도 된다. 결합도를 낮춘다. 또한, 절차적인 방법 보단 Event driven에 가깝다.
> 


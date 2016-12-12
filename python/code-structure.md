# 파이썬 코드구조

## 조건식에서 부등호 수학기호 처럼 가능
```python
n = 10
if 1 < n < 15:
	print('ok')
```
위처럼 부등호를 붙여서 비교 가능


## True & False
확인 요소가 Bool형이 아닐때 어떻게 구분하는가?

|요소 |False|
|----|-----|
|null|None|
|정수0|0|
|부동소수점수0|0.0|
|빈 문자열|''|
|빈 리스트|[]|
|빈 튜플|()|
|빈 딕셔너리|{}|
|빈 셋|set()|

이 외의 다른것들은 True로 간주


## break확인하기 :else
while문 또는 for문이 모두 실행됐는데 발견하지 못한 경우 else가 실행됨.
```python
a = []
for i in a:
	print('found')
	break
else:
	print('Not found')
	
```

## 여러 시퀀스 순회 : zip()
여러 시퀀스를 동시에 병렬로 순회시킬 수 있다. 단 가장 짧은 시퀀스가 멈추면 멈춤.

```python
a = [1, 2]
b = [1, 2, 3]
c = ['a', 'b']

for a, b, c in zip(a,b,c):
	print(a, ' ', b, ' ', c)

>>> 1 1 a
>>> 2 2 b
```

## **숫자 시퀀스 생성 : range()**
특정한 리스트 같은 자료구조 없이 특정 범위 내에서 숫자 스트림을 반환

> range(start, stop, step)

start생략하면 0부터
stop은 반드시 입력
step은 default가 1. -1하면 거꾸로 가능

```python
range(0, 3)   # 0, 1, 2
range(10, 3, -1)    # 10, 9, 8, 7, 6, 5, 4
range(0, 11, 2)    # 0, 2, 4, 6, 8, 10
```

## List Comprehension
배열(List)를 생성하는 방법에는 여러가지가 있다.
```python
li = []
li.append(1)
li.append(2)

####

li = []
for i in range(0, 4):
	list.append(i)

####

li = list(range(0,10))
```
위와 같이 append()를 사용하는 방법, for문과 range를 활용하여 직접 입력하는 방법, 아니면 직접 range를 붙여서 생성하는 방법이 있다.

더 파이써닉한 방법은 바로 리스트 컴프리헨션을 이용하는 방법!!
```python
# 1~10까지의 리스트를 생성할 때
li = [x for x in range(1, 11)]

# 1~10까지 홀수만, 조건식도 가능함
li = [x for x in range(1, 11) if x % 2 == 1]

# 이중 for문도 가능하다, (1,1) ~ (2,4)까지 쌍으로 생성
li = [(a, b) for a in range(1, 3) for b in range(2, 5)]
```

> #### 언패킹(unpacking)
> 튜플들의 쌍으로 생성한 리스트에서 각 튜플로부터 row와 col의 값만 출력하기 위한 작업
> ```python
> for row, col in li:
>     print(row, col)
> ```


## 일등 시민: 함수

'모든것이 객체다', 객체는 숫자, 문자열, 튜플, 리스트, 딕셔너리, 함수를 포함.
> 함수는 곧 일등 시민이다.
> -> 함수를 변수에 할당 가능, 다른 함수의 인자로 쓸 있으며 반환 가능

```python
def answer():
	return 42

def run_something(func):
	return func()

>>> run_something(answer)
42
```
위와 같이 answer 함수를 데이터 처럼 사용할 수 있다. 
**run_something의 매개변수에는 answer() 이 아닌 answer이 들어간다**
이는 괄호가 없으면 함수를 객체로 간주한다.


## 키워드 인자 모으기 : 애스터리스크(*)
키워드 인자를 튜플이나 딕셔너리로 묶어서 받을 수 있다.

```python
def print_kwargs(**kwargs):
	return ('arguments : ', kwargs)

>>> print_kwargs(a='wine', entree='mutton')
arguments : {'a':'wine', 'entree'='mutton'}


# 튜플로 모으기
def print_args(*args):
	return args
	
>>> print_args(1,2,3,'df')
(1, 2, 3, 'df')
```


## 내부 함수
함수 안에 또 다른 함수를 정의할 수 있다.

```python
def outer(a, b):
	def inner(c, d):
		return c+d
	return inner(a, b)

>>> outer(4, 7)
11
```


## 클로저(closure)
- 내부 함수는 클로저 처럼 행동할 수 있다.
- 다른 함수에 의해 동적으로 생성된다.
- 바깥 함수로부터 변수값을 변경하고 저장할 수 있는 함수

```python
def a(saying):
	def inner():
		return 'hello : ' + saying

	return inner

>>> aa = a('test')
hello : test
```

inner 함수는 a함수가 전달받은 saying 변수를 알고있다. 코드에서 return inner 라인은 inner 함수의 특별한 복사본을 반환함. 이것은 외부 함수에 의해 동적으로 생성되고, 그 함수의 변수값을 알고 있는 함수인 클로저.


## 람다(Lambda)
단일문으로 표현되는 익명 함수(anonymous function).

```python
def edit_story(words, func):
	for word in words:
		print(func(word))
	
>>> edit_story(li, lambda word: word.capitalize() + '!')
```

> 람다의 : 과 닫는 괄호 사이에 있는 것이 함수 정의 부분




# 파이썬 코드구조

## 조건식에서 부등호 수학처럼 가능
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

### 여러 시퀀스 순회 : zip()
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

### **숫자 시퀀스 생성 : range()**
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

### List Comprehension
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

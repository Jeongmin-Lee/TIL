# 딕셔너리(Dictionary)

* 파이썬 딕셔너리는 리스트와 유사
* 항목의 순서를 따지지 않음
* Key, Value 형식
* Key는 대부분 문자열 or 불변하는 타입 가능(Bool, 정수, 부동소수점수, **튜플**, 문자열..) 
* 변경 가능함, 추가, 삭제, 수정 가능
* Java의 HashMap과 유사

### 생성 : {}
중괄호({}) 안에 콤마(:)로 구분된 키:값 쌍을 지정.

```python
empty_dict = {}
test_dict = {
	"hobby": "soccer",
	"description": "I'm a good boy!"
}
```


### 딕셔너리로 변환하기 : dict()
두 값으로 이루어진 시퀀스를 딕셔너리로 변환 가능

```python
list = [['a', 'b'], ['c', 'd'], ['e', 'f']]
dict(list)
```
결과
```
{'c':'d', 'a':'b', 'e':'f'}
```
_키 순서는 임의적, 순서 보장 안함_


### 항목 추가/변경하기
키에 참조되는 항목에 값을 할당하면 됨.
>* 이미 존재 -> 새 값으로 교체
>* 존재하지 않음 -> 새 키값이 추가

```python
dic = {
	'messi': 'barca',
	'son': 'tottenham',
	'ronaldo': 'realmadrid',
	'iniesta': 'barca'
}

dic['messi'] = 'manchester united'
>>> {..., 'messi': 'manchester united', ...}
```

### 딕셔너리 결합 : update()

키와 값을 복사해서 다른 딕셔너리에 붙인다.

```python
dic = {
	'a': 'b',
	'cc': 'd'
}

dic2 = {
	'gender': 'male',
	'a': 'c'
}

dic.update(dic2)
>>> {'a':'c', 'gender':'male', 'cc':'d'}
```
키값이 같은 경우 update 매개변수인 두번째 딕셔너리 값으로 바뀐다.


### 항목 삭제 : del
```python
del dic['a']
>>> {'gender':'male', 'cc':'d'}
```

### 모든 항목 삭제
```python
dic.clear()
dic = {}
```

### 키가 존재하는지 알아보기
```python
'a' in dic
>>> true or false
```


### 항목 얻기
```python
dic['a']

# 키가 존재하지 않으면 예외됨
dic['zxczxcv']
>>> ..keyError....

# get()으로 항목 얻기
# a가 없으면 None 출력됨
dic.get('a')     

# 키가 존재하지 않으면 Default값 설정 가능
dic.get('zxzxzxz', 'not found')
```

### 모든 키 얻기 : keys()
```python
dic.keys()
>>> dict_keys(['a','ccc'])

# 리스트로 변환 해야함
a = list(dic.keys())
a[0]
>>> 'a'

```


### 모든 값 얻기 : values()

### 모든 쌍의 Key, Value 얻기 : items()
```python
list(dic.items())
>>> [('a','b'), ...]            # 각 키밸류는 튜플로 반환됨
```


### 할당, 복사 : copy()
```python
aa = dic.copy()
aa['a'] = 'apple';

# aa와 dic는 별개로, aa의 a만 apple로 바뀜 
```

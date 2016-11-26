# Java Garbage Collection

## stop-the-world
> GC를 실행하기 위해 JVM이 애플리케이션 실행을 멈추는 것
> GC작업 완료 후 중단했던 작업 재실행

__GC튜닝 : stop-the-world 시간을 줄이는 것__


## 영역
- Young영역 (Yound Generation)
  - 새롭게 생성한 객체
  - 객체가 사라질 때를 지칭 : Minor GC 
- Old영역 (Old Generation)
  - Young에서 살아남은 객체가 복사됨
  - Yound보다 크게 할당됨
  - 크기가 크므로 Young보단 GC가 적게 발생
  - 객체가 사라질 때를 지칭 : Major GC
- Permanent Generation 영역
  - Method Area 라고함
  - 객체나 억류된 문자열 정보 저장하는 곳
  - GC가 발생할 수 있음. Major GC 횟수에 포함


### Card Table
- Old영역에 있는 객체 -> Young영역의 객체를 참조할 때 표시됨.
- Young GC를 수행할 때, 이 테이블을 뒤져 GC 대상인지 식별


## Young Generation 영역

- Eden
- Survivor1
- Survivor2

1. 새로 생성 객체 -> Eden에
2. Eden에 GC한번 발생 -> 살아남은 객체는 Survivor1 or 2에 이동
3. Eden에 GC 발생 -> 이미 있는 객체가 존재하는 Survivor에 계속 쌓임
4. Survivor 가득차면 살아남은 것들은 다른 Survivor로 이동
5. 가득찬 Survivor는 No Data!
6. 위의 과정을 반복 -> 계속 살아남으면 Old 영역으로 이동

example)
```
가령 Eden영역과 Survivor영역 A, B가 있다고 하자

GC가 발생하면 Eden영역에 살아남은 것들은 A or B로 이동시킨다
랜덤이니 B에 쌓기로 정함.

GC가 반복되면 데이터가 있는 Survivor B영역에 계속 쌓인다.
Survivor B가 가득차면 GC후 살아남은 것들을 A로 이동
(B영역은 비워있다)

계속 반복 후, 계속 끈질기게 살아남은 객체는 Old 영역으로 이동
```

#### TLABs
멀티쓰레드 환경일 때, Thread-safe 해야함.
여러 쓰레드에서 사용하는 객체를 Eden에 저장하려면 Lock이 발생.
Lock-contention 땜에 성능 저하. 이를 해결한게 TLABs


(to be continue....)

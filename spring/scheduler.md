# Spring Scheduling
주기적으로 뭔가를 실행할 때, 스케줄링 기법을 이용한다. 이때 Spring에서 스케줄링을 거는 방법을 알아보자.

## 애노테이션을 이용한 스케줄링
스프링에서 기본적으로 **@Scheduled** 라는 애노테이션을 통해 스케줄링을 걸수 있다. 스프링 부트로 이루어진 프로젝트의 경우

```java
@SpringBootApplication
@EnableScheduling
public class StartApplication{
	public static void main(String[] args) {
		SpringApplication.run(StartApplication.class, args);
	}
}
```

**@EnableScheduling** 으로 스케줄링을 활성화


```java
@Component
public class MyScheduler {

	@Scheduled(fixedRate=2000)
	public void printTest() {
		System.out.println("schedued...");
	}

	@Scheduled(cron="0 30 * * * *")
	public void printTestEvery30Minutes() {
		System.out.println("check...");
	}
}
```
따로 클래스로 빼든 뭘 하든 주기적으로 수행하고자 하는 메서드에 애노테이션 @Scheduled를 걸면 스케줄링이 된다.

### @Scheduled 속성
 - fixedDelay
 - fixedRate
 - cron
 - initialDelay

#### fixedDelay

# Spring DI 이용한 객체 생성
# Spring Configuration

## XML로 구성하는 방식

```java
GenericXmlApplicationContext ctx = new GenerixXmlApplicationContext(
"classpath:/xxx/*", 
"classpath:/aaa/*", ...);
```

Java Code수정하지 않고 xml설정파일 추가하는 방법.

```xml
<import resource="classpath:/xxx/*" />
<import resource="classpath:/aaa/*" />
```

## Java Config 방식

```@Configuration```, ```@Bean```


## XML + Java Config
<context:annotation-config>

```@ImportResource("classpath:config-xxx.xml")```

## 팩토리 방식 스프링 빈 설정

FactoryBean<T> class를 implement해서 직접 빈을 어떻게 생성할지 정할 수 있다.
```getObject()```
```
@Qualifier("stand")
@Autowired
@Inject
@Name
```

#### **@Component**

```java
@ComponentScan(	basePackages={"com.navercorp.a", "com.navercorp.b"})
```

```includeFilter```, ```excludeFilter``` 적용 가능

Example
```java
@ComponentScan(
	basePackages={"com.navercorp.a", "com.navercorp.b"}, 
	includeFilters = {@Filter(type=FilterType.REGEX, pattern=".*Service")},
	excludeFilters = @Filter(type=FilterType.ASPECTJ, pattern="net..*Dao"))
```

## Spring Container Life Cycle

생성 - 빈 설정 - 사용 - 소멸

```java
AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();

// 빈 추가로 등록
ctx.register();

// 갱신해야 반영됨
ctx.refresh();

// 소멸, 빈도 함께
ctx.close()

// JVM소멸시 자동으로 소멸되게끔
ctx.registerShutdownHook()
```

## Bean Lifecycle
객체 생성 - 초기화 - 사용 - 소멸 순으로 유지된다.
스프링 컨테이너에 의해 객체가 생성되고 초기화와 소멸의 과정을 거친다. 각 초기화와 소멸을 구현하는 방법에는 각각 3가지가 존재한다.

### 초기화
방법에는 3가지가 존재

1. ```@PostConstruct``` 활용
2. ```InitializingBean``` 인터페이스 구현하여 사용, ```afterPropertiesSet``` 메서드 override
3. 커스텀 init 메서드
	- 빈 정의 xml에 ```init-method``` 로 메서드 명 지정
	- ```@Bean(initMethod="init")```, init메서드 활용

### 소멸
1. ```@PreDestroy```
2. DisposableBean 인터페이스
3. 커스텀 destroy 메서드 정의

### 스프링 컨테이너, 빈 이름 가져오기
* ApplicationContextAware
* BeanNameAware
인터페이스를 활용한다. implement한 클래스에서 사용할 수 있다.


### Bean 범위(scope)
* Singleton (default)
* Prototype
	* 매번 호출될 때마다 인스턴스 생성됨
	* 스프링 컨테이너가 소멸되도 인스턴스들은 계속 유지됨

# Environment
설정 값들을 불러올 때 다양한 방법이 존재한다.

1)
```
ctx.getEnvironment()
evn.getProperty("db.name");
```

2) 
```java
class ConfigClass implement EnvironmentAware {
	// ..
	@Override
	public void getEnvironment(Environment env){
		
	}
}
```

3) 

```java
@PropertySource("classpath:/db.properties")
```

4) 
```java
@Configuration
@PropertySource
@Value("${db.url}")
```
그리고 ```PropertySourcePlaceHolderConfigurer``` 클래스를 static한 빈으로 등록

## Profile
```java
@Profile("dev")
```


xxx-dev.properties


## MessageSource를 이용한 메시지 국제화

* ResourceBundleMessageSource
* ReloadedResourceBundleMessageSource

두가지 구현체 클래스를 이용할 수 있다. ```messageSource.getMessage("error.login", null, Locale.getDefault())``` 처럼 사용가능.

### ResourceBundleMessageSource 단점
1. 메시지 파일을 클래스패스 이외의 다른 곳에 위치시킬 수 없다
2. 한 번 읽어오면 수정해도 반영이 안됨

**ReloadedResourceBundleMessageSource** 를 대안으로 활용한다.

### ResourceBundleMessageSource
* basenames의 list, value에 file:/ or classpath:/ 등으로 입력 가능
* cacheSeconds : n 설정하면 n초마다 불러옴 (default : -1, 반영하지 않음)
* defaultEncoding : value = "UTF-8"

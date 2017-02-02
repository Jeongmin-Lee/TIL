# Spring MVC

## 1. Spring MVC 기본 프로젝트 생성해보기
STS에서 생성하는 순서

1. Dynamic Web Project 생성
2. Maven Project 활성화
3. web.xml 추가 후 Servlet 설정


### 1.1. Web.xml 추가
> web.xml이 없는 경우
> 
> **프로젝트 우클릭 - java EE Tools - Generate Deployment Descriptor Stub 클릭**
> src 폴더 내부에 알아서 해줌

### 1.2. Servlet 설정
web.xml 생성 후 서블릿 관련 설정을 추가해야 함.

* Servlet dispatcher 정의
* init-param 으로 ```contextConfigLocation``` 정의. param-value 에는 config xml파일 경로를 입력. 상대경로나 classpath 입력 가능
* Servlet Mapping 설정. url-pattern = "/"

#### 1.2.1. DispatcherServlet 설정
Spring MVC의 핵심이 되는 DispatcherServlet을 정의 해야한다.
Servlet-name과 class를 정의하면 ```[servletname]-servlet.xml``` 파일을 기본적인 스프링 설정 파일로 사용한다.

경로나 설정 파일의 이름이 다르다면 ```contextConfigLocation``` 을 이용하여 설정 파일 목록을 지정해줘야한다.

XML이 아닌 ```@Configuration``` 을 사용했다면,
init-param을 추가하여 ```contextClass``` 이름에 ```AnnotationConfigWebApplicationContext``` 클래스 풀 네임을 지정.
(기본 설정은 ```XmlWebApplicationContext```)

#### 1.2.2. Encoding Filter
파라미터를 올바르게 처리하기 위해 web.xml에 filter를 추가한다. ```CharacterEncodingFilter``` 를 필터 클래스로 정의. encoding은 UTF-8로 정의

#### 1.2.3. ViewResolver 설정
뷰 이름을 실제 뷰와 연결시키기 위해 ```ViewResolver``` 를 설정해야 한다. prefix, suffix 등의 설정을 한다. prefix는 정적파일이 있는 경로, suffix는 확장자.

**Bean xml 설정**
```xml
<bean id="viewResolver" 
	class="org.springframework.web.servlet.view.InternalResourceViewResolver">
	<property name="prefix" value="/WEB-INF/view/" />
	<property name="suffix" value=".jsp" />
</bean>
```

#### 1.2.4. HandlerMapping, HandlerAdapter 설정
```xml
<mvc:annotation-driven>
```

또는 ```@EnableWebMvc``` 로 자동으로 설정할 수 있다.

#### 1.2.5 Spring 설정 파일 작성
스프링 관련 설정 방법은 XML, Java Config 두 가지가 있다. 여기서는 xml로 학습.
Resources 폴더 또는 WEB-INF 폴더 밑에 Spring Bean Configuration file을 생성한다. 

### 1.3. 컨트롤러 구현
```java
@Controller
public class HelloController {
	
	@RequestMapping("/hello")
	public String hello(Model model) {
		model.addAttribute("name", "jeongmin");
		return "hello";
	}
}
```

* @Controller : 컨트롤러 클래스를 의미
* @RequestMapping : URL매핑 등 다양한 속성을 지정.
	* @GetMapping, @PostMapping 등으로 간결하게 사용 가능
	* value는 매핑될 URL, method는 HTTP전송 방식(GET/POST/PUT/DELETE 등)이 사용됨
	* 기본 Method는 GET
	* @Controller 와 함께 적용 가능. 상위 경로가 된다. 
	```java
	
	@Controller
	@RequestMapping("/user")
	public class UserController {
		@RequestMapping("/:id")
		public String getUser(@PathVariable("id") int id) {
			...
		}
	}
	
	// getUser에 매핑되는 URL은 /user/123 의 형태가 된다 
	```

#### 1.3.1. @PathVariable
REST한 URL설계를하면서 URL에 파라미터가 포함된 경우가 많다. 이를 잘 처리해주는 애노테이션.

```java
@RequestMapping("/user/{userId}")
public void getUser(@PathVariable("userId") int userId) {
	...
}
``` 

와 같이 { } 기호로 파라미터를 표시하면 @PathVariable 애노테이션을 이용하여 값을 받아올 수 있다. value로 이름을 표기하면 된다. 만약 변수명과 동일하다면 생략해도 무방.

#### 1.3.2. Request/Response 가능한 ContentType 지정
컨텐트 타입에 따라 요청을 제한할 수 있으며, 응답 컨텐트 타입을 제한할 수 있다. 

```java
@RequestMapping(produces="application/x-www-form-urlencoded", consumes="application/json")
```


#### 1.3.3. Request 파라미터 구하기
1. HttpServletRequest를 이용한 방법
	매 컨트롤러 메서드의 파라미터로 ```HttpServletRequest``` 를 받아 직접 getParameter 로 구한다.
	
2. @RequestParam을 이용한 방법
	```java
	@RequestParam("id") int id 
	```
	와 같이 id를 얻을 수 있다. 쿼리스트링으로 요청되었기 때문에 URL은 ```/user?id=xxx``` 와 같은 형태로 요청된다.

##### required
기본적으로 RequestParam을 선언했으면 반드시 값이 존재해야만 한다. 하지만 필수가 아닌 경우가 있을 수 있는데, 이 때 required 값을 false로 선언하면 된다.

##### defaultValue
값이 존재하지 않을 때 null대신 지정한 값을 넣어준다.

e.g.
```java
@Requestparam("id", required=false, defaultValue="1") int id
```

##### 커맨드 객체
넘겨줘야할 값이 많을 때 편하게 객체 단위로 넘기도록 Spring MVC에서 제공한다. 메서드의 매개변수를 객체로 지정하면 된다. 

뷰에 클래스 명의 카멜 케이스 이름으로 전달된다. 중첩된 객체, 배열 등 가능하며 변수 명으로 접근한다. 자바빈 형태로 구현해야 하며 setter 를 통해 연결된다.

##### @ModelAttribute
클래스 명 대신 별도의 이름으로 접근하도록 해주는 애노테이션
```java
@RequestMapping()
public void xxx(@ModelAttribute("user") UserDto member) {
	...
}
```
UserDto 클래스를 받을 때 userDto 라는 이름대신 _user_라는 이름으로 사용된다.


#### 1.3.4. @CookieValue, @RequestHeader
쿠키값과 헤더를 가져오기 위한 애노테이션이다. ```@RequestParam``` 과 마찬가지로 value, required, defaultValue로 정의할 수 있다.

```java
@RequestMapping()
public void xxx(
	@RequestHeader("Accept") String accept, 
	@CookieValue("auth", required=false) Cookie cookie,
	@ModelAttribute("user") UserDto member) {
	...
}
```

### 1.4. 커맨드 객체 Validation
1.3.3 에서 커맨드 객체로 접근하여 값을 받을 수 있는데, 이 때 서버 측에서 요청받은 객체의 값이 유효한지 체크하는 기능을 제공한다. 

> 클라이언트에서 폼 검사를 통해 검증하는 것 뿐만아니라 서버에서도 요청받은 값에 대해 검증하는 절차가 반드시 필요하다! 악의적으로 잘못된 데이터가 전송되면 문제를 일으킬 수 있기 때문.

#### 1.4.1. @Valid, @initBinder 를 이용한 검증

위 애노테이션을 사용하기 위해서는 별도로 의존을 추가해야 한다.

_**javax.validationAPI 의존성 추가**_
```xml
<dependency>
    <groupId>javax.validation</groupId>
    <artifactId>validation-api</artifactId>
    <version>1.0.0.GA</version>
</dependency>
```

```java
@RequestMapping("/user/{userId}")
public void getUser(
	@Valid User user,
	...) {
	...
}

@InitBinder
protected void initBinder(WebDataBinder binder) {
	binder.setValidator(new UserValidator());
}
```

매개변수로 @Valid가 있는 객체는 InitBinder를 통해 검증을 수행한다. ```UserValidator``` 클래스는 ```validator``` 인터페이스를 구현한 구현체다. 

##### **글로벌 Validator**
하나의 validator를 이용해 모든 객체를 검증할 수 있다.
```xml
<mvc:annotaion-driven validator="validator"/>
<bean id="validator" class="custom.CommonValidator" />
```

글로벌을 사용하지 않고 별도의 validator를 사용하려면 @InitBinder를 통해 setValidator로 지정해야한다.


#### 1.4.2. @Valid, 빈 Validation 애노테이션을 통한 검증
매번 객체 검증을 validator로 구현해서 사용해야 하는데 이 Validator 클래스 작성 없이 애노테이션만으로 검증이 가능하다.

Bean Validation API(JSR303) 에 정의된 @NotNull, @Size, @Digit 등의 Validation 애노테이션을 사용할 수 있다.

1. 객체에 @NotNull, @Size, @Max 등의 검증 규칙을 적용한다.
2. ```LocalValidatorFactoryBean``` 클래스를 이용해 기본 Validator를 등록
	JSR303 규칙을 사용하기 위해 빈으로 등록한다. 별도로 빈을 정의해도 되지만, ```<mvc:annotation-driven>``` 을 사용하면 자동으로 등록된다.
3. 컨트롤러에 적용

> JSR303 주요 애노테이션
>
> * @NotNull
> * @Size
> * @Min / @Max
> * @Digit
> * @Pattern
>
> _문자열의 null 체크를 하는 Validation을 추가할 경우 @NotNull만 사용하는 경우 빈 문자열이 들어올 가능성이 있다._
> ```java
> @NotNull
> @Size(min=1)
> private String title;
> ```
> 길이가 최소 1이라는 검증을 추가하여 방지

### 1.5. Http 세션 사용하기
화면을 전환 시 데이터를 공유하여 사용한다. 이 때 임시로 데이터를 넣어두는 용도로 세션을 활용한다. 세션은 요청한 각 사용자마다 생성이 되기 때문에 접속자가 많아질 경우 세션 객체의 개수도 증가한다. 이에 따라 메모리 부족현상이 발생할 수도 있다.
_사용자가 많아 트래픽이 높아질 경우 세션보다는 DB나 외부 캐시서버를 활용하는 편이 좋다._

* HttpSession
* @SessionAttribute

#### 1.5.1. HttpSession 이용
메서드 파라미터에 HttpSession을 받아서 사용한다.
```httpSession.setAttribute("user", user);```

상황에 따라 세션을 생성하고 싶으면 ```HttpServletRequest``` 를 받아 세션을 생성한다.

```java
...
public String login(..., HttpServletRequest request) {
	...
	HttpSession session = request.getSession();
	session.setAttribute("auth", auth);
}
```


#### 1.5.2. @SessionAttribute
사용할 클래스에 애노테이션을 적용하면 명시한 이름을 통해 세션객체를 사용할 수 있다.
컨트롤러 메서드에 Model 객체를 추가하여 attribute를 사용하는데 이 때,  ```@ModelAttribute``` 을 활용하면 추가할 필요가 없다.

```java
@Controller
@SessionAttribute("event")
public class UserController {
	
	@ModelAttribute("event")
	public EventForm formData() {
		return new EventForm();
	}

	@RequestMapping("/event")
	public String step1(
		@ModelAttribute("event") EventForm formData, ..) {
		// formData 사용
	}
}
```

* 세션 객체 삭제
컨트롤러 메서드에 ```SessionStatus``` 클래스를 받아 ```setComplete()``` 메서드를 호출한다.
> 세션에서만 삭제될 뿐, 모델에서 삭제되진 않는다. 즉, View코드에서는 그대로 사용할 수 있다.

### 1.6. 예외처리
컨트롤러를 수행하다 예외가 발생하면 화면에 에러코드와 함께 trace가 그대로 노출이된다. 예외상황에 따라 적절한 화면을 보여주도록 예외처리를 해줘야만 한다. Spring은 예외처리에 대해 3가지의 방법을 제공한다.

* @ExceptionHandler
* @ControllerAdvice
* @ResponseStatus

#### **@ExceptionHandler**
익셉션 직접 처리. 애노테이션이 붙은 메서드는 @RequestMapping과 유사하게 동작한다. 

```java
@ExceptionHandler(ArithmeticException.class)
public String handleException() {
	return "error";
}
```

ExceptionHandler의 value는 익셉션 클래스의 배열을 갖는다. 

@ExceptionHandler(ArithmeticException.class)

단일로 사용할 경우와 

@ExceptionHandler({ArithmeticException.class, DataAccessException.class})
위와 같이 2개 이상의 익셉션을 적용할 수 있다.

같은 컨트롤러 내에 정의된 요청에서 명시한 익셉션이 발생하면 위의 handleException 메서드를 타고 error 뷰가 보여지게 된다.

##### **Response Code**
기본적으로 위와같이 익셉션을 처리하면 200이 된다. 다른 코드로 처리하고 싶다면 **메서드에 HttpServletResponse를 파라미터로 추가하고 StatusCode 메서드로 지정한다**.

```java
@ExceptionHandler(RuntimeException.class)
public String error(HttpServletResponse response) {
	response.setStatus(HttpSevletResponse.SC_INTERNAL_SERVER_ERROR);
	return "error";
}
```
뿐만 아니라 HttpServletRequest, Model, HttpSession 등을 전달받을 수 있다.
익셉션 객체에 접근하고 싶으면 파라미터를 지정해서 가져올 수 있다.

```java
@ExceptionHandler
public String error(RuntimeException ex) {
	// ex...
	return "error";
}
```

##### **처리 방법**
> 익셉션이 발생하면 ```HandlerExceptionResolver```에서 처리한다.
> 
> HandlerExceptionResolver의 종류는 아래와 같다.
> 
> * ExceptionHandlerExceptionResolver : @ExceptionHandler 이용해서 처리
> * DefaultHandlerExceptionResolver : 스프링이 발생시키는 익셉션 처리. 404 Error의 경우.
> * ResponseStatusExceptionResolver : @ResponseStatus 적용된 경우 응답코드를 전송
> 
> DispatcherServlet은 예외가 발생하면 위에서 3단계를 거치면서 처리를 한다.
> 
> ```<mvc:annotation-driven> ``` 이나 ```@EnableWebMvc``` 를 선언하면
> **ExceptionHandlerExceptionResolver** 을 자동으로 등록하게 된다. 따라서 손쉽게 @ExceptionHandler를 이용할 수 있는 것.



#### **@ControllerAdvice**를 통한 공통 익셉션 처리
@ExceptionHandler는 해당된 컨트롤러만 처리할 수 있었는데 @ControllerAdvice는 해당 컨트롤러 뿐만 아니라 여러 컨트롤러에서 같은 익셉션이 발생한 경우 공통으로 처리한다.

구현 방법은 다음과 같다. 

1. 적용할 클래스를 생성하고 @ControllerAdvice 선언
2. 적용한 클래스를 빈으로 선언
3. 처리할 @ExceptionHandler 선언

```@ControllerAdvice```의 속성을 통해 대상을 지정할 수 있다. 패키지, 특정 애노테이션이 적용된 컨트롤러, 특정 타입이 가능하다.

e.g.
```java
@ControllerAdvice("com.navercorp.study")
```



> ##### **우선순위**
> ```
> 컨트롤러 내 정의된 @ExceptionHandler 
> VS 
> @ControllerAdvice에 정의된 @ExceptionHandler
> ```
> 컨트롤러 내 정의된 핸들러가 먼저 적용된다.


#### **@ResponseStatus**
익셉션에 응답 코드를 설정할 수 있다. 구현방법은 

```java
@ResponseStatus(HttpStatus.NOT_FOUND)
public class NoUserException extends Exception {
	...
}
```
위와 같이 **익셉션 클래스에 선언한다**.

> 컨트롤러 영역의 익셉션에만 @ResponseStatus 를 적용하자.

### 1.7. Spring MVC 설정

#### 1.7.1. WebMvcConfigurer
xml이 아닌 java 코드로 커스텀 설정.
```WebMvcConfigurerAdapter``` 를 상속받아서 사용한다. 이 클래스에서 ```@Configuration```, ```@EnableWebMvc``` 애노테이션을 선언한다. mvc 태그 사용했던 것들을 적용할 수 있다.

##### **뷰 전용 컨트롤러 설정**
addViewController 메서드를 Override하여 별도의 컨트롤러 정의 없이 구현 가능
```java
@Override
public void addViewControllers(ViewControllerRegistry registry){
	registry.addViewController("/index").setViewName("index");
	..
}	
```

##### **디폴트 서블릿 설정**
```java
@Override
public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
	configurer.enable();
}
```

##### **정적 자원 설정**
이미지가 저장될 경로를 선언하고 ```ResourceHandler```, ```ResourceMapping``` 으로 URL에 연결하는 방식을 적용할 수 있다. 또한 웹브라우저에 캐시하여 효율성 증가시킬 수 있다.

> _Resource Handler & Mapping_
이미지 같은 리소스의 경우 다양한 경로에 저장될 수 있다.
META-INT/ 나 resource/static, File경로 등에 저장될 수 있는데 이 경로를 인식하고 URL에 Mapping할 수 있다.

file:/home1/irteam/images/11.png 의 경우 /home1/irteam/images/ 를 ```/resoures/images/**``` 로 매핑해놓으면

```http://localhost:8080/resources/images/11.png``` 로 접근할 수 있다.


```java
@Override
public void addResourceHandlers(ResourceHandlerRegistry registry) {
	registry.addResourceHandler(StorageProperties.RESOURCE_MAPPING_URL + "/**")
		.addResourceLocations("file:" + storageProperties.getLocation(), 
			"file:/Users/Naver/images/", 
			"classpath:/static/images/")
		.setCachePeriod(60);
}
```

### 1.8. HandlerInterceptor를 이용한 인터셉터 구현
여러 컨트롤러에 공통적으로 적용하기 위한 기능. 이와 유사한 기능을 제공하는 AOP는 더 범용적이다. HandlerInterceptor 인터페이스는 아래 3가지 메서드를 지원한다. 구현 클래스를 정의하여 각 시점에서 실행되는 공통기능을 구현할 수 있다.

* preHandler : 컨트롤러 실행 전
* postHandler : 컨트롤러 실행 후, 뷰 실행 전
* afterCompletion : 뷰 다 그리고 난 후

#### **preHandler** 컨트롤러 실행 전
요청하기 전 필요한 정보를 생성하는 등의 작업을 할 수 있다. 리턴값은 ```boolean``` 형이며  false이면 컨트롤러나 다음 HandlerInterceptor를 수행하지 않는다.

#### **postHandler**
컨트롤러가 정상적으로 실행된 이후 추가 기능을 구현할 수 있다.
_만약 예외가 발생하면 실행되지 않는다_
(발생 시, afterCompletion 메서드에 호출됨)

* Object
* ModelAndView

#### **afterCompletion**
컨트롤러 실행 후 클라이언테 뷰를 전송한 다음에 호출된다. 메서드의 파라미터로 HttpServlet을 제외하고 아래 두가지를 받는다.

* Object
* Exception : 컨트롤러에서 발생한 예외, 정상작동하면 null

익셉션의 로그, 실행 시간 등의 기록을 남기는데 적합한 메서드.

> **HandlerInterceptorAdapter**
> 전부 구현할 필요가 없다면 인터페이스를 구현하지 않고 Adapter클래스를 사용
> 내용은 빈 값이다.

#### 1.8.1. HandlerInterceptor 설정
* mvc 태그를 통한 xml설정
* ```WebMvcConfigurerAdapter``` 의 ```addInterceptor``` 를 재정의한 설정

1. ```<mvc:interceptor>```
  ```
	<mvc:interceptor>
		<mvc:mapping path="bb"/>
		<mvc:mapping path="aa"/>
		<bean class="xx.xxx" />
	</mvc:interceptor>
	```
	
2. addInterceptor
	```java

	@Configuration
	@EnableWebMvc
	public class CustomConfig extends WebMvcConfigurerAdapter {
		
		@Override
		public void addInterceptors(InterceptorRegistry registry) {
			registry.addInterceptor(interceptor)
				.addPathPattern("/event/**", "/user/**")
		}
	}
	```

url을 매핑하는 용도로 ```excludePathPattern``` 으로 특정 URL을 제외하는 메서드도 제공.

registry에 여러번 addInterceptor를 적용하여 여러 인터셉터를 추가할 수 있다. 실행순서는 먼저 선언한 인터셉터부터. 컨트롤러의 수행이 끝나면 역순으로 수행된다.

### 1.9. WebApplicationContext
보통 한 개 이상의 DispatcherServlet을 설정하는 것이 가능하다. REST계층과 Front계층으로 나뉘었을 때 각각의 빈 설정 파일을 사용하는데, **다른 곳에 정의되어 있는 빈 객체를 사용할 수는 없다.**

**공통으로 처리할 빈이 필요한 경우?**

1. ```ContextLoaderListener``` 를 ServletListener로 등록
2. contextConfigLocation 컨텍스트 파라미터로 설정 파일을 지정


**@Configuration 설정을 사용한다면**
```contextClass``` 파라미터에 ```AnnotationConfigWebApplicationContext```를 지정한다.

### 1.10. DelegatingFilterProxy
서블릿 필터로 등록할 빈.

?

### 1.11. 핸들러, HandlerMapping, HandlerAdapter

**요청 처리 과정**
Request -> DispatcherSevlet -> ```HandlerMapping``` -> dispatcherSerlvet -> ```HandlerAdapter``` -> Controller -> ViewResolver -> dispatcherServlet -> View -> JSP

DispatcherServlet은 ```ModelAndView``` 를 반환하면 정상동작.
String 을 리턴하는 컨트롤러 메서드가 존재하는데 ```HandlerAdapter```는 String을 ModelAndView로 변환하는 역할을 한다. 

#### 1.11.1. HandlerMapping 우선순위
여러 HandlerMapping이 등록되는데, 우선순위에 따라 매핑이 정해진다. 높은 우선순위를 가진 맵핑부터 처리할 핸들러 객체를 리턴하면 이용하고, null이면 다음 순위를 갖는 맵핑이 처리한다.

모든 맵핑에 대한 핸들러가 null이면 404 NOT_FOUND 에러를 응답.
핸들러 객체를 리턴하면 HandlerAdapter를 찾고 실행을 위임한다. 

#### 1.11.2. HandlerMapping, HandlerAdapter 설정
```<mvc:annotation-driven>```, ```@EnableWebMvc``` 를 사용하면 

* RequestMappingHandlerMapping
* SimpleUrlHandlerMapping : Url과 핸들러 객체를 맵핑
* RequestMappingHandlerAdapter
* HttpRequestHandlerAdapter
* SimpleControllerHandlerAdapter

위와같은 HandlerMapping과 HandlerAdapter를 설정한다.

개발자가 ```@Controller``` 를 구현하면 RequestMappingHandlerMapping, RequestMappingHandlerAdapter를 이용해서 처리한다.
driven, enableWebMvc 등의 설정을 하면 기본값으로 위의 맵핑과 핸들러가 등록이 된다.

```Default Servlet Handler``` 를 설정하면 ```DefaultServletHttpRequestHandler```, ```SimpleUrlHandlerMapping``` 클래스로 등록이 된다.
이들의 우선순위는 기본보다 높아서 요청이 들어오면 RequestMapping 먼저 후 SimpleUrl맵핑이 적용된다.

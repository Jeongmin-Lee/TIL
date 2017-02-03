# Spring MVC 뷰 구현
## 1. ViewResolver 설정
컨트롤러가 지정한 뷰 이름으로 결과 화면을 생성하는 View객체를 구할 때 사용되는 것. DispatcherServlet에서 컨트롤러의 반환값을 받은 후 처리된다.

ViewResolver 구현 클래스의 종류.

* InternalResourceViewResolver
* VelocityViewResolver
* VelocityLayoutViewResolver
* BeanNameViewResolver

### 1.1. ViewResolver 인터페이스
```java
public interface ViewResolver {
	View resolveViewName(String viewName, Locale locale) throws Exception;
}
```

뷰이름과 지역화를 위한 매개변수가 있다. 매핑되는 View를 리턴.

### 1.2. View 객체
응답 결과를 생성하는 역할. 모든 뷰 객체는 View 인터페이스를 구현하고 있다.
```getContentType()``` 메서드는 text/html 과 같은 응답결과의 컨텐트 타입을 리턴.

### 1.3. InternalResourceViewResolver 설정
```InternalResourceView``` 뷰 객체를 리턴.
JSP나 HTML 파일 등을 이용해서 결과를 생성.

설정방법은 InternalResourceViewResolver 클래스를 빈으로 등록한다. Property로 prefix는 해당 경로, suffix는 확장자를 지정.

> prefix = "/WEB-INF/view/", suffix = ".jsp" 일 때,
>
> prefix + {뷰 이름} + suffix 으로 실제 자원 경로를 구한다.
> e.g. 뷰 이름이 hello 일 때 : /WEB-INF/view/hello.jsp

### 1.4. BeanNameViewResolver 설정
뷰 이름과 같은 이름을 갖는 빈을 뷰로 사용. 주로 커스텀 뷰 클래스를 뷰로 사용할 때 이용한다.
```java
// viewResolver가 BeanNameViewResolver로 되어있는 경우

@RequestMapping("xx")
public String download(Model model,...) {
	..
	return "download";
}
```
일 때 download 라는 id로 정의된 빈 클래스를 뷰로 사용한다.

### 1.5. 여러 ViewResolver 설정
두 개 이상의 ViewResolver 설정이 가능하다. 우선순위에 따라 먼저 사용할지 결정된다.
우선순위는 ```@Order``` 또는 Ordered 구현했을때, 값으로 정해진다.
**우선순위 값이 가장 작을수록 우선순위가 높다. (기본값은 가장 낮은순위인 Integer.MAX_VALUE)**

> InternalResourceViewResolver는 마지막 우선순위를 가지도록 주의한다. 항상 뷰 객체를 리턴하기 때문에 우선순위가 높을 경우 낮은 우선순위를 가진 ViewResolver는 사용되지 않는다.

## 2. HTML 특수문자 처리
값에 특수문자가 있을 경우 HTML에서 spring 태그를 이용해서 메시지를 출력할 수 있다.
```html
<title><spring:message code="login.form.title" /></title>
```

받아올 값에 특수문자가 포함되었다면 ```&lt;``` 등의 엔티티 레퍼런스로 변환해줘야 원하는 형태로 표시가 된다.

설정은 ```defaultHtmlEscape``` 를 통해 true, false로 줄 수 있다.

* true : 커스텀 태그나 Velocity 매크로 등으로 '&' 같은 값을 치환 (기본값)
* false : 특수문자 그대로 출력


## 3. JSP를 이용한 뷰 구현

### 3.1. 메시지 출력을 위한 설정
스프링 태그로 메시지 출력하려면 MessageSource 등록해야 한다.
```ResourceBundleMessageSource``` 를 빈으로 등록

```<spring:message>``` 태그로 메시지 읽어오기

### 커스텀 태그
```xml
<form>
<input>
<select>
...

```

## 4. HTML이외의 뷰
### 4.1. 커스텀 뷰
JSP, HTML등의 정적인 페이지 이외에 커스텀으로 구현한 뷰로 나타낼 때.

1. BeanNameViewResolver 로 설정
2. ```AbstractView``` 클래스 상속받아 커스텀 뷰 구현
3. 커스텀 뷰를 빈으로 등록
3. 컨트롤러 ModelAndView의 빈 id를 리턴

과정을 거쳐 구현할 수 있다. 

## 5. Locale 처리
spring:message 커스텀 태그는 언어정보를 이용해 알맞은 언어의 메시지를 출력한다.
해당 언어의 선정은 ```LocaleResolver``` 에서 처리한다. 설정을 통해 Locale을 변경해보자.

### 5.1. LocaleResolver 인터페이스

```java
public interface LocaleResolver {
	Locale resolveLocale(HttpServletRequest request);
	void setLocale(HttpServletRequest request, HttpServletResponse response, Locale locale);
}
```

* resolveLocale
	요청과 관련된 로케일을 리턴.DispatcherServlet이 호출하여 웹 요청 처리할 때 사용.
* setLocale
	로케일 변경할 때 사용. 쿠키나 HttpSession의 로케일 정보를 저장할 때 사용.

### 5.2. LocaleResolver의 종류

* AcceptHeaderLocaleResolver : 설정없을 때 기본. Accept-Language 헤더로부터 추출. _setLocale 사용 불가_
* CookieLocaleResolver : 쿠키를 담아서 정보 저장. 기본 로케일을 Locale사용. null이면 Accept-Language 사용
	* 쿠키 설정 관련 Property
		* cookieName, cookieDomain, cookiePath, cookieMaxAge, cookieSecure
* SessionLocaleResolver : HttpSession에 정보 저장. 기본 로케일은 Locale 사용. null이면 Accept-Language 사용.
* FixedLocaleResolver : 요청에 상관없이 기본 로케일로 설정한 값을 사용.
* 커스텀 Resolver : LocaleResolver 구현하여 사용. 빈 등록을 LocaleResolver로 해야 한다.

### 5.3. LocaleResolver 등록
```xml
<bean id="localeResolver"
	class="org.springframework.web.servlet.i18n.SessionLocaleResolver" />
```

빈 이름을 반드시 ```localeResolver``` 여야만 한다.

### 5.4. LocaleResolver 이용한 Locale변경
컨트롤러의 빈 프로퍼티에 정의한 LocaleResolver를 등록.
```property ref```

컨트롤러에서 LocaleResolver를 정의하고  setLocale로 변경
```java
@Controller
public void xxController {

	private LocaleResolver localeResolver;

	@RequestMapping(..)
	public String change() {
		...
		Locale locale = new Locale(language);
		localeResolver.setLocale(..., locale);
	}

	public void setLocaleResolver(LocaleResolver localeResolver) {
		this.localeResolver = localeResolver;
	}
}
```

* RequestContextUtils 클래스를 활용
```java
LocaleResolver localeResolver = RequestContextUtils.getLocaleResolver(request);
```

> LocaleResolver의 setLocale 메서드를 지원하지 않는 리졸버도 있다. 호출하면 익셉션 발생

### 5.5. LocaleChangeInterceptor를 이용한 Locale 변경
Locale을 변경하기 위해 컨트롤러를 개발했어야 했다. 요청에 대해 로케일 변경을 손쉽게 해주는 ```LocaleChangeInterceptor``` 클래스를 이용한다. 

1. 빈으로 등록 후, property name에 ```paramName```, value를 ```language``` 로 지정
2. language 파라미터로 변경할 수 있다. 
	e.g. http://..../login?**language=en**


## 6. XML/JSON 변환 처리
API형태로 제공하기 위해 응답으로 XML/JSON을 이용한다. 이 응답을 위해 

* 뷰 클래스를 사용하거나
* HttpServletResponse를 이용하거나

두 방법을 사용할 수 있지만, **Spring MVC에서는 더 쉬운 방법을 제공한다.**

* @RequestBody
* @ResponseBody

를 살펴보자.


### 6.1. @RequestBody/@ResponseBody/HttpMessageConverter
@RequestBody와 @ResponseBody는 요청, 응답 바디를 자바 객체로 변환하는 역할을 한다.

#### **HttpMessageConverter**
@Request/ResponseBody가 있으면 자바 객체와 요청/응답 사이의 변환을 담당. HttpMessageConverter의 구현체로는 StringHttpMessageConverter를 포함해 여러가지 존재한다.

mvc태그의 annotation-driven 이나 @EnableWebMvc를 사용하면 이러한 컨버터들이 자동 등록된다.

**MessageConverter의 종류**

* StringHttpMessageConverter :  문자열
* Jaxb2RootElementHttpMessageConverter : XML변환. application/xml
* MappingJackson2HttpMessageConverter : JSON변환. application/json
* ByteArrayHttpMessageConverter : 바이트배열
* ResourceHttpMessageConverter : 리소스
* AllEncompassingForm... : 폼 데이터로 전송. MultiValueMap으로 변환.

### 6.2. Jackson2를 이용한 JSON 처리
Jackson2 의존성 추가
@ResponseBody 선언 후 객체를 리턴하면 변환됨.

> **커스텀 HttpMessageConverter 사용**
> 
> 극히 드물지만, 사용하려면 구현 클래스를 생성하고
> ```
> <mvc:message-converter>
>     <bean class="aa.customConverter" />
>     ..
> ```
> 빈으로 등록한다.
>
> @EnableWebMvc 사용하는 경우,
> ```WebMvcConfigurerAdapter``` 에서 ```configureMessageConverter``` 를 재정의하여 설정한다.
> 이럴 때는 기본으로등록한 컨버터가 없으므로 직접 추가해줘야 한다.


## 7. 파일 업로드
파일 업로드의 경우 HTML Form태그의 enctype을 ```multipart/form-data``` 로 지정.

### 7.1. MultipartResolver 설정
RequestParam으로 들어온 multipart 데이터를 변환해주는 역할을 한다. 구현체를 빈으로 등록시키면 설정이 완료된다.

* CommonsMultipartResolver : _commons-fileupload 의존_을 추가하여 설정해야 함.
* StandardServletMultipartResolver

**이 때, 빈의 이름을 multipartResolver로 설정해야 한다**
(DispatcherServlet이 이름이 multipartResolver인 빈을 사용하기 때문)

#### Servlet3의 파일 업로드 사용 설정

* DispatcherServlet이 Servlet3의 Multipart를 처리하도록 설정
	```<multipart-config>``` 태그를 web.xml에 정의한다.
	
	* location : 저장할 위치
	* max-file-size : 업로드 가능한 최대 크기. (기본 -1)
	* file-size-threshold : 이 크기 보다 크면 임시파일 생성
	* max-request-size : 전체 요청 최대 전송 크기. (기본 -1)
* StandardServletMultipartResolver을 MultipartResolver로 등록


### 7.2. 업로드한 파일 접근
* MultipartFile 인터페이스를 사용한다. 이 인터페이스로 업로드한 파일의 데이터를 읽을 수 있다.

```getBytes()``` 를 통해 파일을 받아올 수 있으며, ```transferTo(file)``` 을 이용하여 간결하게 업로드한 파일을 지정한 파일에 저장할 수 있다.


* @RequestParam
HTML input 태그의 name으로 받아온다.
```@RequestParam("file") MultipartFile file```

* MultipartHttpServletRequest
컨트롤러 메서드의 매개변수로 정의해서 받아올 수 있다.

* 커맨드 객체를 통한 접근
클래스의 변수로 MultipartFile 타입의 프로퍼티를 추가하면 사용 가능하다.
클래스의 get 메서드로 접근 가능.

* 서블릿3의 Part사용
```java
@RequestParam("report") Part part
```
MultipartFile 처럼 선언하여 사용 가능.


## 8. WebSocket
HTTP프로토콜 기반으로 브라우저와 서버간의 양방향 통신을 지원하기 위한 표준. 마치 소켓을 사용하는것처럼 자유롭게 메시지를 주고 받을 수 있다. 실시간 알림, 채팅 등 구현할 때 사용된다.

스프링 4의 웹소켓 기능을 사용하기 위해 ```spring-websocket``` 의존을 추가한다.

### 8.1. WebSocketHandler를 이용한 서버 구현
스프링 웹소켓기능은 스프링MVC를 지원하기 때문에 손쉽게 구현 가능하다.

* WebSocketHandler 인터페이스 구현
* ```<websocket:handler>``` or ```@EnableWebSocket``` 을 이용해서 구현 객체를 등록

#### WebSocketHandler 구현
실질적인 구현은 여기서 이루어진다. WebSocketHandler를 직접 쓰기보단 일부 제공하는 클래스를 상속받아 구현한다.

_제공하는 클래스_

* TextWebSocketHandler
* AbstractWebSocketHandler

_주요 메서드_

* afterConnectionEstablished : 연결된 후 
* handleMessage : 데이터를 전송하면 호출된다.
* handlerTransportError : 연결에 문제가 발생할 때
* afterConnectionClosed : 연결이 종료된 후
* supportPartialMessages : 파일을 쪼개서 받을 수 있는지

#### websocket handler 등록
bean 설정 파일에서

```xml
<bean id="echoHandler" class="xxx.EchoHandler" />

<websocket:handlers>
	<websocket:mapping handler="echoHandler" path="/echo-ws" />
</websocket:handlers>

```
websocket 태그로 핸들러와 엔드포인트 경로를 정의한다.
위의 경우 ```ws://localhost:8080/echo-ws``` 로 접속하면 echoHandler빈을 이용해서 처리한다.

#### WebSocketMessage
스프링 웹소켓에서 주고 받는 데이터를 담기 위한 용도.

```java
public interface WebSocketMessage<T> {
	// message를 리턴
	T getPayload();

	// message 길이. 포함된 binary의 수
	int getPayloadLength();

	// 파일 분할해서 보내는 경우, 받은 메시지가 마지막 조각인지 여부
	boolean isLast();
}
```
구현한 하위 타입으로 TextMessage, BinaryMessage가 존재한다.


### 8.2. [SockJS 지원](https://github.com/sockjs/sockjs-client)
웹소켓을 지원하기 전에 클라이언트 서버간의 데이터 통신을 위해 다양한 방법을 사용했다. Long-Polling, iFrame 등의 방법이 있는데 각 방식에 따라 다른 코드를 작성해야 하는 문제가 있었다.

SockJS는 이런 기법들을 추상화하여 웹소켓과 유사한 API로 제공하여 이런 불편함을 해소해 준다.

> Tomcat6 버전은 웹소켓을 지원하지 않는데, SockJS를 이용해 서버를 구성할 수 있다.

#### 서버 설정
* 웹소켓 핸들러 설정에 ```<websocket:sockjs />``` 부분을 추가
* Config 설정 클래스를 ```WebSocketConfigurer```로 구현,  ```@EnableWebSocket``` 로 설정
* registerWebSocketHandler 메서드를 재정의할 때, addHandler시 ```.withSockJS()``` 를 추가

#### 클라이언트
sockjs 자바스크립트 파일을 임포트한 HTML로 사용가능하다.
```js
var sock = new SockJS("http://xxxx/echo.sockjs");
```


## 9. Spring MVC 서블릿3 기반 설정
지금까지 Spring MVC설정방식을 보면 web.xml을 정의하여 DispatcherServlet, filter 등의 설정을 지정했었다. 

서블릿3 부터 web.xml 대신 자바 코드로 설정하는 것이 가능하게 되었다.
web.xml 대신 ```WebApplicationInitializer``` 인터페이스를 상속받아 구현하면 된다.

### WebApplicationInitializer 인터페이스
```java
public interface WebApplicationInitializer {
	void onStartup(ServletContext context) throw ServletException;
}
```
너무 추상적이라 설정해줘야 할 것이 많다.
위 인터페이스를 구현한 추상 클래스가 마련되어 있는데 

* AbstractDispatcherServletInitializer : xml로 설정
* AbstractAnnotationConfigDispatcherServletInitializer : @Configuration 자바 기반의 설정을 위한.
 
이들 중 하나를 상속받아 설정하는 것이 더 편리하다.

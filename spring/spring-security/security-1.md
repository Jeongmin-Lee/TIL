# Spring Security
## 1. 웹 보안과 스프링 시큐리티
웹 어플리케이션을 개발할 때 보안 관련 부분을 신경써야한다.

* 인증(Authentication) : 현재 사용자가 누군지 확인하는 과정. 보통 ID/Password 기반
* 인가(Authorization) : 특정 대상(URL, 기능 등)을 사용할 권한이 있는지 검사
* UI처리 : 알맞은 에러화면 보여주거나, 로그인 폼 등 인증화면 호출

보통 로그인을 통해 인증을 처리한다.
성공하면 정보를 세션이나 쿠키에 저장하여 보관하고 이걸로 사용자를 식별한다.
위 세가지 기능을 처음부터 구현해야 하는데 이러한 불편함을 덜어주고자 스프링 시큐리티가 개발되었다. 정해진 틀 안에서 인증 부분을 구현하는 방식으로 되어있어 쉽고 빠르게 3가지 기능을 구현할 수 있다.

> Spring Security 3 버전 사용. 4는 개발중

## 2. 스프링 시큐리티 프로젝트 스타트
### 2.1. Maven Dependency
스프링 시큐리티 관련 의존을 설정해야 한다.

1. 스프링 Web MVC 관련 의존 설정
2. Spring Security의 web, config, tablibs 정의
3. javax.servlet, javax.servlet.jsp, jstl 설정


### 2.2. XML 설정
src/main/resource 폴더에 Spring Bean Configuration XML파일 생성

```xml
<sec:http use-expressions="true">
	<sec:intercept-url pattern="/admin/**" access="hasAuthority('ROLE_ADMIN')"/>
	<sec:intercept-url pattern="/manager/**" access="hasRole('ROLE_MANAGER')"/>
	<sec:intercept-url pattern="/member/**" access="isAuthenticated()" />
	<sec:intercept-url pattern="/**" access="permitAll"/>
	<sec:form-login />
	<sec:logout />
</sec:http>
```
와 같은 형태로 설정. 자바 설정으로 할 수 있지 않을까?
세부적으로 어떤 역할을 하는지는 다음 장에서 보자

```xml
<sec:authentication-manager>
	<sec:authentication-provider>
		<sec:user-service>
			<sec:user name="test" password="1234" 
			          authorities="ROLE_USER" />
			<sec:user name="manager" password="qwer" 
			          authorities="ROLE_MANAGER" />
			<sec:user name="admin" password="asdf" 
			          authorities="ROLE_ADMIN,ROLE_USER" />
		</sec:user-service>
	</sec:authentication-provider>
</sec:authentication-manager>
```

사용자 아이디, 비번은 DB로 빼지만 이번은 시큐리티에서 인메모리DB로 설정한다.

### 2.3. web.xml 설정

* context-param 으로 spring-security.xml 지정
* 이름이 *springSecurityFilterChain* 인 DelegatingFilterProxy 정의

```xml
<filter>
	<filter-name>springSecurityFilterChain</filter-name>
	<filter-class>
		org.springframework.web.filter.DelegatingFilterProxy
	</filter-class>
</filter>
<filter-mapping>
	<filter-name>springSecurityFilterChain</filter-name>
	<url-pattern>/*</url-pattern>
</filter-mapping>
```

> **빈을 정의하지 않았는데 왜 filter-name 이 _springSecurityFilterChain_ 인가?**
> 
>
> 위에서 설정했던 spring-security.xml 에서 시큐리티 네임스페이스를 처리하는 과정에서 등록되기 때문.
>
> 내부적으로 FilterChainProxy 객체를 빈으로 등록하는데 이 이름이 _springSecurityFilterChain_ 이다.
> 
> 보안 관련 서플릿 필터들을 묶어서 실행해주는 역할
> 
> - interceptor-url 정의한 부분은 ```FilterSecurityInterceptor``` 필터 생성
> - form-login 부분은 ```UsernamePasswordAuthenticationFilter``` 를 생성
> - logout 은 ```LogoutFilter``` 생성하는데 사용된다. 
> 
> FilterChainProxy는 요청이 들어오면 위 체인을 이용해서 처리한다.

### 2.4. JSP코드
```jsp
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>

<sec:authorize access="isAuthenticated()">
	<sec:authentication property="name"/>님 환영합니다.
</sec:authorize>

<sec:authorize access="isAuthenticated()">
	<li><a href="<c:url value='/j_spring_security_logout' />">/j_spring_security_logout</a></li>
</sec:authorize>
```
스프링 시큐리티에서 제공하는 tag를 이용하여 선언한다.
authorize 태그를 이용해서 인증 여부를 판단하고 인증된 사용자만 태그 내 코드를 처리한다.

로그인 폼, 인증실패 시 403처리 등은 시큐리티 내부에서 처리한다.


## **3. 스프링 시큐리티 구조**
스프링 시큐리티가 지원하지 않는 인증방식, HttpSession이 아닌 다른 장소에 인증 객체를 보관하고 싶을 때 (customize)

동작 방식을 이해하고 변경할 수 있어야 한다.

### 3.1. SecurityContext, SecurityContextHolder, Authentication, GrandedAuthority

* Authentication : 스프링 시큐리티에서 현재 접근한 사용자의 보안 관련 정보를 보관하는 역할 (사용자의 인증 여부, 권한, 이름 및 접근 주체)

* SecurityContextHolder : 
* SecurityContext : _Authentication을 보관하는 역할_. holder에서 getContext를 통해 가져올 수 있다. 여기서 getAuthentication() 메서드를 통해 Authentication을 가져올 수 있음. 

웹 요청 -> 스프링 시큐리티의 서블릿 필터(SecurityContextPersistenceFilter) -> SecurityContext에 Authentication 객체 설정

이 과정을 소스로 구현할 수 있지만 ```SecurityContextPersistenceFilter```
를 통해 간결하게 구현 가능.

#### 3.1.1. Authentication 인터페이스
직접 구현한 객체를 사용하기 위해서는 SecurityContextHolder 를 이용해서 객체를 구한다.

```java
Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
```

이후 메서드를 통해 정보를 얻어올 수 있다.

* getName :
* getCredential : 인증 대상 주체, 비밀번호 등
* getPrinciple : 주체 표현하는 객체 
* isAuthentication : 인증 여부 리턴
* **getAuthorities()** : 주체가 가진 권한의 목록. ```GrantedAuthority``` 가 권한

등의 메서드가 있다.

**목적** 

* AuthenticationManager에 인증 요청할 때 필요한 정보를 담는 용도
* 접속한 사용자에 대한 정보를 표현

스프링 시큐리티는 Authentication이 지정한 자원(URL 경로)에 접근할 수 있는지 검사. 

* UsernamePasswordAuthenticationToken
* AnonymousAuthenticationToken

등의 구현체를 제공하고 있는데 필요에 따라 직접 구현할 수 있다.


#### 3.1.2. GrantedAuthority 인터페이스
Authentication의 getAuthorities() 는 사용자가 가진 권한의 목록을 리턴한다고 했는데 이때 권한을 표시할 때 사용한다.

```java
public interface GrantedAuthority extends Serializable {
    String getAuthority();
}
```

스프링 시큐리는 모든 권한을 문자열로 처리하는데 (```ROLE_ADMIN``` 과 같이) 이 문자열을 리턴한다.

```xml
<sec:interceptor-url pattern="/admin/**" access="hasAuthority('USER_MANAGER')"
```
```USER_MANAGER``` 처럼 사용된다.

**SimpleGrantedAuthority**
GrantedAuthority 타입의 객체를 직접 생성할 때 사용할 수 있는 클래스

### 3.2. 보안 필터 체인
스프링 보안 처리의 핵심 기능.

* 로그인 폼을 제공
* 권한 없는 요청에 403 코드 응답
* 로그아웃 링크로 로그아웃 처리

등의 보안 관련 작업을 처리하는 역할을 한다.

web.xml에 DelegatingFilterProxy를 설정한 바 있다.
스프링 시큐리티가 ```FilterChainProxy``` 를 생성하는데 여기로 처리를 위임.
이것은 여러 필터 체인 형식으로 가지고 있는 ```SecurityFilterChain```으로 위임.

```
DelegatingFilterProxy --> 
FilterChainProxy --> 
SecurityFilterChain
```

* 보안 필터 체인(SecurityFilterChain)
	* Authentication 생성, 접근 권한 검사 등 보안 관련 처리
	* 여러 필터가 모여 형성
	* 스프링 시큐리티는 기본적인 필터를 제공
		1. SecurityContextPersistenceFilter
		2. WebAsyncManagerIntegrationFilter
		3. LogoutFilter, ...
		4. UsernamePasswordAuthenticationFilter 등 순서대로 거쳐서 수행됨

_보안 체인 필터에 정의된 순서대로 필터가 적용_

직접 구현한 필터를 보안 필터 체인에 추가할 경우 추가될 위치를 지정해야함
(이미 순서대로 정의된 필터를 이용)

### 3.3. AuthenticationManager 인증 처리
인증 처리를 담당하는 인터페이스

```java
public interface AuthenticationManager {
	Authentication authenticate(Authentication authentication) throws AuthenticationException;
}
```

인증하는데 필요한 정보를 authentication 을 통해 받아 처리한다.

* 성공 : Authentication 리턴
* 실패 : AuthenticationException 익셉션 발생

구현체는 ```ProviderManager``` 클래스가 있고 아이디/비밀번호 인증과 같은 처리를 ```AuthenticationProvider``` 로 위임한다.

> **스프링 시큐리티의 인증 부분을 커스터마이징 하고 싶다면??**
>
> AuthenticationManager를 구현할 수 있지만 ProviderManager를 그대로 사용하여 
> _AuthenticationProvider를 확장하여 구현_ 한다.
> (하지만 기본 구현체로도 충분)
> 
> #### AuthenticationProvider 구현체의 종류
> * DaoAuthenticationProvider : Dao를 이용해 사용자 정보를 읽어서 처리
> * LdapAuthenticationProvider : LDAP서버, 액티브 디렉토리 이용한 인증
> * OpenIdAuthenticationProvider : 오픈ID 이용한 인증
>
> spring-security.xml 에서 정의한 ```authentication-provider``` 부분은 
> 
> 1. DaoAuthenticationProvider 를 자체 생성
> 2. 내부적으로 ```UserDetailsService``` 이용해서 정보 로딩
> 
> 순서로 동작. 설정한 정보는 ```InMemoryUserDetailsManager``` 를 사용하도록 했다.


### 3.4. FilterSecurityInterceptor와 AccessDecisionManager 인가 처리

```<sec:interceptor-url>``` 설정을 통해 권한을 지정해 주는데 

1. FilterSecurityInterceptor
2. FilterInvocationSecurityMetadataSource
3. AccessDecisionManager

이 때 세 요소도 설정됨. 순서대로 처리되면서 경로에 대한 접근 가능 여부를 판별한다.

_실행 순서_
```
필터체인의 이전 필터 -> 1 -> 
FilterSecurityInterceptor -> 2 -> FilterInvocationSecurityMetadataSource -> 3 -> FilterSecurityInterceptor -> 4 -> 
AccessDecisionManager
```
1 .체인 실행 : SecurityContext에 Authentication 객체를 저장
2. getAttributes : 인터셉터는 요청 경로에 대한 보안 설정 정보 요청
3. 보안 설정 목록을 인터셉터에 리턴
4. decide() 메서드 호출해서 요청 경로에 대한 보안 설정을 충족하는지 검사

4번에서 지정한 자원에 접근권한이 없으면 **익셉션 발생시킴(AccessDeniedException)** 


#### 3.4.1. AccessDecisionManager & AccessDecisionVoter
decide메서드를 통해 인증 검사. 실패하면 익셉션 발생

실질적으로 체크하는 로직은 ```AccessDecisionVoter``` 클래스에 위임.

##### ```AccessDecisionVoter``` 인터페이스

* ACCESS_GRANTED = 1 : 권한
* ACCESS_ABSTAIN = 0 : 권한 여부를 판단할 수 없으면
* ACCESS_DENIED = -1 : 없음

vote 메서드를 수행할 구현체를 통해 검사한다.
AccessDecisionVoter의 구현체로는 ```WebExpressionVoter``` 가 있는데 xml파일에서 정의한 

```
<sec:http use-expression="true">
	<sec:interceptor-url ...
		access="hasAuthority('ROLE_ADMIN')"
```

access 와 같은 표현식을 검증. ```use-expression``` 값이 true이면 자동으로 활성화

## 4. 웹 요청 인가
접근 제어를 표시하는 표현식

* hasRole('권한'), hasAuthority('권한') : 권한을 가졌는지
* hasAnyRole('권한'), hasAnyAuthority('권한') : 하나라도 가졌는지
* permitAll : 모두 허용
* denyAll : 모두 거부
* isAnonymous : 임의 사용자인지
* isAuthenticated : 인증된 사용자인지, 기억된 사용자도 인증자로 처리
* isRememberMe : 기억된 사용자인지



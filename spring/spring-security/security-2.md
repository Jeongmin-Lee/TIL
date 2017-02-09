## 5. 상황별 스프링 시큐리티 설정

### 5.1. 일부 경로 적용 안하기
모든 경로에 보안 필터 체인을 적용할 필요는 없다. `CSS, JS, 이미지 등` 은 제어 대상이 아님

```xml
<sec:http pattern="/css/**" security="none"/>
<sec:http pattern="/js/**" security="none"/>
```
와 같이 설정한다.

/css, /js 로 시작하는 경로에 대해 보안 필터 체인을 적용하지 않는다.
`SecurityContextPersistenceFilter` 적용안되므로 `SecurityContextHolder` 를 통해 `SecurityContext` 를 구할 수 없게된다.

### 5.2. DB를 이용한 인증처리
보통 사용자 정보를 외부 DB에 저장하는데 간단하게 설정할 수 있다.

**1) 매핑테이블 설정**

User와 Authority테이블 생성
Authority 테이블에는 `authority` 권한 문자열이 들어갈 필드를 지정

**2) 스프링 시큐리티 설정**

실습 시 사용한 user-service 대신 `jdbc-user-service` 를 활용하여 설정
```xml
<sec:authentication-manager>
	<sec:authentication-provider>		
		<sec:jdbc-user-service data-source-ref="dataSource"/>
	</sec:authentication-provider>
</sec:authentication-manager>

<bean id="dataSource" class="com.xxxx.dataSource">
	<property name="driverClass" value="com.mysql.jdbc.Driver" />
	...
</bean>
```
**3) 데이터 준비, Spring MVC 설정**

1. 유저 테이블에 유저 데이터를 입력하고 유저에 맞는 ROLE을 입력한다.
2. security xml파일 설정
3. Spring MVC의 DispatcherServlet, web.xml 설정
4. 각 권한에 따라 보여줄 JSP파일 작성


### 5.3. DB를 이용한 인증 처리 구조

AuthenticationManager 인터페이스의 구현 클래스 = ProviderManager는 `AuthenticationProvider` 에 위임

`<jdbc-user-service>` 태그를 설정하면 `AuthenticationProvider`의 구현체인 `DaoAuthenticationProvider`를 사용

`DaoAuthenticationProvider` 는 `UserDetailsService`를 이용해서 사용자 정보를 불러온 후 `authenticate()` 메서드로 인증을 처리한다.

1. UserDetailsService의 `loadUserByUsername()` 메서드로 사용자 이름 해당하는 `UserDetails` 객체를 얻음 (존재하지 않으면 UsernameNotFoundException)
2. 입력한 암호와 UserDetails의 `getPassword` 를 이용해서 비교 (일치하지 않으면 BadCredentialsException)
3. 일치하면 UserDetails한테 Authentication 객체를 리턴

실제 DB에서 사용자 정보를 읽어오는 부분 : `UserDetailsService`

`<jdbc-user-service>` 태그를 이용하면, 위 인터페이스를 구현한 `JdbcUserDetailsManager` 이용.
이 클래스는 `JdbcDaoImpl` 클래스를 상속받는데 실질적인 DB연동 처리 역할을 하므로 `DataSource` 가 필요하다. 

`<jdbc-user-service>`의 data-source-ref 에서 DataSource를 지정한다.


#### 5.3.1. 사용자 정보 조회를 위한 필드 변경
유저의 정보를 읽어올 때 사용하는 쿼리는 `JdbcUserDetailsManager`의 부모 클래스인 `JdbcDaoImpl` 클래스에 정의되어 있다.

```java

public class JdbcDaoImpl extends JdbcDaoSupport implements UserDetailsService {
    public static final String DEF_USERS_BY_USERNAME_QUERY =
            "select username,password,enabled " +
            "from users " +
            "where username = ?";
    public static final String DEF_AUTHORITIES_BY_USERNAME_QUERY =
            "select username,authority " +
            "from authorities " +
            "where username = ?";
    public static final String DEF_GROUP_AUTHORITIES_BY_USERNAME_QUERY =
            "select g.id, g.group_name, ga.authority " +
            "from groups g, group_members gm, group_authorities ga " +
            "where gm.username = ? " +
            "and g.id = ga.group_id " +
            "and g.id = gm.group_id";
	...
```

위와 같이 테이블명과 컬럼명 등이 정해져 있다.

테이블 명명규칙 등의 이유로 다를 수 있는데 이럴 때 `<jdbc-user-service>` 속성을 활용한다.

* users-by-username-query : 사용자 이름으로 UserDetails를 찾을 때 쿼리 입력. (Select 결과 3개 컬럼이 이름, 암호, 가능여부로 사용)
* authorities-by-username-query : 이름으로 권한 목록을 찾을 때 쿼리. (select 결과 두번째 컬럼이 권한으로 사용


#### 5.3.2. UserDetailsManager를 이용한 사용자 관리: 추가
시큐리티는 UserDetailsManager의 구현체인 `JdbcUserDetailsManager` 를 빈으로 등록한다. UserDetailsManager의 createUser, updateUser 등의 CRUD메서드가 있어서 DB연동을 처리할 수 있다.

> 등록된 쿼리를 변경하기 위한 설정을 지원하지 않아 _테이블 이름, 컬럼 등을 변경하고 싶으면 `UserDetailsService`를 커스터마이징하는 구현체를 정의해야 한다.

#### 5.3.3. 커스텀 UserDetailsService 구현 (사용자 정보조회)
스프링 시큐리티는 Jdbc지원을 통해 쉽게 DB연동을 통한 인증 기능을 구현할 수 있지만 _지정한 형식의 스키마를 가진 테이블만을 사용해야하는 한계_가 있다.

환경에 맞게 커스텀 인증 기능을 구현하려면?

* AuthenticationManager 인터페이스 구현
* AuthenticationProvider 인터페이스 구현
* UserDetailsService 인터페이스 구현

세 방법 중 최대한 활용할 수 있는 `UserDetailsService` 를 이용하여 구현한다.
`loadUserByUsername` 메서드를 아래 규칙을 지켜 직접 구현.

* username 존재 : UserDetails 객체 리턴
* username 존재, but 권한 없으면 : UserNotFoundException
* username 존재하지 않으면 : UserNotFountException

**커스텀 UserDetailsService 구현**
```java
class CustomUserDetailsService implements UserDetailsService {
	public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
		UserInfo user = userRepository.findByUsername(username); 
		
		if (user == null) {
			throw new UsernameNotFoundException(username);
		}
		
		...
		
		List<GrantedAuthority> authorities = new ArrayList();
		
		
		return new User(username, userInfo.getPassword(), authorities);
	}
}

```

이 후 이 객체를 빈으로 등록하고 
```xml
<bean id="customUserDetailsService" class="com.navercorp.xx.CustomUserDetailsService" />

<sec:authentication-manager>
	<sec:authentication-provider user-service-ref="customUserDetailsService">
	</sec:authentication-provider>
</sec:authentication-manager>
```


#### 5.3.4. 커스텀 AuthenticationProvider 구현(암호 비교)

사용자 아이디/비번 일치 여부는 LDAP에서, 권한은 DB에서 불러와야 한다면 UserDetailsService만으로는 제어 불가하다. 이 때 `AuthenticationProvider`를 직접 구현

* 파라미터 authentication 인증 처리를 지원하지 않으면 null
* 인증 실패면 AuthenticationException
* 성공하면 인증 정보를 담은 Authentication 리턴

```java
class CustomAuthenticationProvider implements AuthenticationProvider {

	public Authentication authenticate(Authentication authentication) throws AuthenticationException {
		UsernamePasswordAuthenticationToken token = (UsernamePasswordAuthenticationToken) authentication;
		
		// 정보 조회
		UserInfo userInfo = findByUserId(token.getName());
		
		// 암호비교
		if (!matches(userInfo.getPassword(), token.getCredentials()) {
			throw new BadCredentialsException("not matched password");
		}
		
		// 사용자가 가진 권한 목록 읽어온다
		List<GrantedAuthority> authorities = getAuthorities(userInfo.getId());
		
		
		// 인증된 사용자에 대한 Authentication 객체 생성해서 리턴
		return new UsernamePasswordAuthenticationToken(
				new UserInfo(id, name, null), 
				null, 
				authorities);
	}

	public boolean supports(Class<?> authentication) {
		return UsernamePasswordAuthenticationToken.class.isAssignableFrom(authentication);
	}
}
```

여기서 `UsernamePasswordAuthenticationToken` 말고 직접 `Authentication`을 구현해서 사용해도 무방.

```java
UsernamePasswordAuthenticationToken(Object principle, Object credentials, Collection<? extends GrantedAuthority> authorities)
```

생성자를 보면 

1. Principle : 주체의 정보를 넘긴다. 보통 UserDetails, Principle 객체를 넘기는데, 여기선 UserInfo 객체 그대로 전달
2. credential : 인증 증명에 사용된다. **메모리에 남기지 않도록 null, 또는 생성 후 `eraseCredential()`**
3. authorities : 인증된 사용자가 갖는 권한 목록


AuthenticationProvider를 직접 만들었으므로 빈으로 정의하고 
```xml
<sec:authentication-provider ref="customAuthenticationProvider"/>
```

로 설정


### 5.4. 비밀번호 암호화
`DaoAutheticationProvider` 클래스에서 평문인 비밀번호를 암호화해주는 기능을 제공한다.

`DaoAutheticationProvider` 클래스는 사용자가 입력한 암호와 `UserDetailsService`에서 구한 `UserDetails` 암호가 일치하는지 판단하기 위해 `PasswordEncoder` 를 사용.

> 처리 절차
> 
> 1. DaoAuthenticationProvider --> UserDetailsSeriver : loadByUsername() 으로 정보 요청하고 리턴
> 2. DaoAuthenticationProvider --> PasswordEncoder : `isPasswordValid(password, presentedPassword, salt)` 

별도로 설정하지 않는 경우 `PlaintextPasswordEncoder` (x) (Deprecate된 PasswordEncoder를 사용할 경우)

`NoOpPasswordEncoder` 가 설정된다.



**_PasswordEncoder_ 인터페이스**
org.springframework.security.crypto.password 패키지에 포함된 인터페이스.
org.springframework.security.authentication.encoding 에 포함된 버전은 deprecate 됨.

아무래도 암호화를 담당하는 salt값을 직접 입력하도록 구성한 것이 보안상 문제가 되어 바뀐듯 하다.

```java
public interface PasswordEncoder {
    String encode(CharSequence rawPassword);
    ...
    boolean matches(CharSequence rawPassword, String encodedPassword);
}
```

PasswordEncoder 인터페이스의 형태이다. 이를 사용할 수 있는 구현체로는 
- BCryptPasswordEncoder
- NoOpPasswordEncoder
- Pbkdf2PasswordEncoder
- StandardPasswordEncoder

대략 4가지가 존재함.


#### 설정
1. PasswordEncoder의 구현체를 빈 등록
2. `<sec:authentication-provider>` 내에 password-encoder 설정

```xml
<bean id="passwordEncoder" class="o.s.security.crypto.bcrypt.BCryptPasswordEncoder"/>

<sec:authentication-manager>
	<sec:authentication-provider>
		<sec:jdbc-user-service data-source-ref="..."/>
		<sec:password-encoder ref="passwordEncoder" />

...
```


#### Example

* Password Encoding
PasswordEncoder 인터페이스를 이용해서 encode를 수행하면 암호화 완료.
어떤 방식으로 암호화 할 것인지는 구현체의 종류를 선택하여 설정하면 된다.
가령 StandardPasswordEncoder로 암호화를 진행하고 싶은 경우 맞게 생성하면 됨

```java
String rawPassword = "abcd1234";

PasswordEncoder encoder = new BCryptPasswordEncoder();
String encodedPassword = encoder.encode(rawPassword);
```



* Matches
암호화를 했으면 평문이 입력되었을때, 일치한지 검사해야만 한다.
이를 확인하는 메서드. 리턴값은 Boolean. 일치하면 true, 아니면 false를 반환한다.

> matches([비밀번호 평문], [Encode된 비밀번호 문자열])

```java
String encodedPassword = "...xxxxx..";
String rawPassword = "abcd1234";

PasswordEncoder encoder = new BCryptPasswordEncoder();

boolean isRight = encoder.matches(rawPassword, encodedPassword);
```

#### BCryptPasswordEncoder
Bcrypt 해싱 함수를 이용한 구현체. 
스프링에서는 신규 시스템을 개발할 때 StandardPasswordEncoder대신 사용할 것을 권장한다.
보안성과 타 언어와의 상호호환성 측면에서 더 낫기 때문.

#### StandardPasswordEncoder
SHA-256(1024) 해싱과 8Byte 랜덤 salt값을 이용한 암호화 방식.
전반적으로 많이 사용하는 방식. 기존 시스템에서 사용하고 있다면 그대로 이 암호화 방식을 사용하는 것이 좋다.
Salt, secret, password의 바이트를 연결지어 수행되는 Digest알고리즘을 이용함.


### 5.5. 로그인/로그아웃 UI/에러 응답 설정 변경

#### 5.5.1. 로그인 폼과 인증 요청 경로 변경
제공하는 로그인 폼과 URL 경로가 있지만 변경하고 싶을때,
`<sec:form-login>` 태그로 쉽게 변경 가능

##### 속성

* login-page : 인증 처리를 위해 이동할 폼 경로(기본값 : /spring-security-login)
* login-processing-url : 로그인 요청을 위한 경로 지정, POST로 들어오면 처리 (기본 : /j_spring_security_check)
* username-parameter : 로그인 요청에서 사용자이름 지정 (j_username)
* password-parameter : 로그인 요청 시 비밀번호 지정(j_password)
* default-target-url : 로그인 성공 시 이동할 기본 경로 (기본값 : /)
* authentication-failure-url : 실패 시 이동할 경로 (기본값 : /spring_security_login?login_error)

e.g.
```xml
<sec:http use-expression="true">
	...
	<sec:form-login
		login-page="user/loginform"
		login-processing-url="/user/login"
		..
		default-target-url="/index"
	/>
```

login-page에 정의된 `user/loginform` 은 `permitAll` 로 지정해서 누구나 보여줄 수 있도록.

#### 5.5.2. 로그인 처리 관련 필터의 동작 방식
인증되지 않은 사용자가 권한이 필요한 경로로 접근했을때

1. 보안 필터 체인의 `FilterSecurityInterceptor` 에서 AuthenticationException 발생
2. 이전 필터 체인인 `ExceptionTranslationFilter`에서 처리하는데, 
3. 인증 전이면 요청 정보를 `RequestCache` 에 저장
4. LoginUrlAuthenticationEntryPoint의 `commence()` 로 인증 요청 : form-login 태그의 login-page 지정한 값으로 리다이렉트

로그인 폼에서 login-processing-url로 지정한 값으로 로그인 요청을 하면,

1. `UsernamePasswordAuthenticationFilter` 로 요청
username-parameter 등의 값을 불러옴
2. AuthenticationManager의 `authenticate()` 를 통해 인증 수행하여 결과 또는 익셉션 리턴
	3. 인증 성공
		4. Authentication 정보를 `SecurityContext`에 설정
		5. 인증 성공 후처리를 `AuthenticationSuccessHandler` 에서 처리. 구현체는 SavedRequestAwareAuthenticationSuccessHandler
		6. RequestCache에서 요청정보를 구함, 보관된 객체 or Null을 리턴
		7. 요청 정보의 리다이텍트
	4. 인증 실패
		5. `AuthenticationFailureHandler` 에서 후처리. 구현체는 SimpleUrlAuthenticationFailureHandler
		6. form-login 태그의 `authentication-failure-url` 속성에 정의된 경로로 리다이렉트


> 1) 
> 
> * AuthenticationSuccessHandler
> * AuthenticationFailureHandler
> 
> 기본으로 제공하는 클래스가 아닌 커스터마이즈 하고 싶다면 
> 구현한 클래스를 빈으로 등록하고 
> 
> `form-login` 태그의 
> authentication-success-handler-ref, authentication-failure-handler-ref 에 빈 Id로 정의
> (default-target-url, authentication-failture-url 이 적용안됨)
> 
> 
> 2) http태그의 `entry-point-ref` 를 사용하면
> `AuthenticationEntryPoint`로 사용할 객체 생성
> 
> `form-login` 태그의 login-page속성이 적용안됨


#### 5.5.3. 로그아웃 URL 및 로그아웃 이동경로
`<logout>` 태그를 사용하면 `/j_spring_security_logout` 경로로 로그아웃 처리된다.

`LogoutFilter`가 로그아웃 처리 담당.

경로를 변경하고 싶으면,
```xml
<sec:logout logout-url="/user/logout"/>
```
로그아웃 후 리다이렉트는 logout-success-url 속성값으로 지정한다. (지정하지 않으면 기본값 : /)



#### 5.5.4. 권한 없음 응답화면
권한 없을 땐 403 상태코드를 응답한다. 별도의 안내페이지를 작성하고 싶다면, 

```xml
<sec:http use-expression="true">
	<sec:access-denied-handler error-page="/security/accessDenied" />
	...
```

와 같이 경로를 지정해주면 된다.
`AccessDeniedHandler` 의 기본 구현체는 `AccessDeniedHandlerImpl`인데 error-page를 지정한 경우에만 포워딩한다. (포워딩이므로 웹브라우저 주소는 유지)
직접 정의하고 싶으면 빈으로 정의하고 ref속성으로 지정


### 5.6. HTTPS 및 포트 매핑 설정
데이터의 안전한 전송을 위해서 HTTPS 프로토콜을 사용하는데, 경로별로 HTTPS 프로토콜을 사용하도록 할 수 있다.

`intercept-url` 태그의 `requires-channel` 속성 사용.
```xml
<sec:intercept-url pattern="/member/**" access="isAuthenticated()" requires-channel="https"/>
```

/member/ 로 시작하는 모든 경로는 HTTPS로 인증된 사용자만 접근을 허용한다. 

> requires-channel에 들어갈 값은 http, https, any



#### 포트 매핑 설정
리다이렉트 시 HTTP와 HTTPS의 포트가 다를 경우 `<port-mapping>` 태그를 이용해서 번호를 지정할 수 있다. 

```xml
<sec:http use-expressions="true">
	<sec:port-mappings>
		<sec:port-mapping http="8080" https="8443"/>
	</sec:port-mappings>
	
	...
```

### 5.7. 세션 대신 쿠키 사용

_대규모 트래픽이 발생하는 서비스는 HttpSession 대신 쿠키 또는 별도 외부의 세션 서버에 세션 정보를 저장_

스프링 시큐리티의 기본 기능으로 사용자 인증정보를 HttpSession에 담아서 사용
**위와 같이 쿠키, 외부 서버를 이용할 경우 커스텀으로 정의해야 함.**

#### 5.7.1. 로그인 성공 후 이동 경로를 파라미터로 지정

로그인 성공 시 이동할 경로를 HttpSession이 아닌 RequestParameter 로 전달하고 싶을 때 [로그인 처리 관련 필터 동작방식 참고](/#Example) 부분에서 언급된 부분들을 직접 커스터마이징을 하면된다.

* 커스텀 AuthenticationEntryPoint : 로그인 폼 경로로 리다이렉트 할 때, 현재 요청 경로를 . `returl` 파라미터로 붙여서 보냄
* 커스텀 AuthenticationSuccessHandler : 로그인 성공 시, `returl`값이 있으면 여기로 리다이렉트
* 커스텀 AuthenticationFailureHandler : 로그인 실패 시, 로그인 경로로 포워딩
* 로그인 폼에서 `returl` 파라미터 전송하도록 구성
* `NullRequestCache` 사용 : 아무 기능도 하지않는 RequestCache사용



**AuthenticationEntryPoint 구현**
commence 재정의하여 리다이렉트

```java
public class CustomAuthenticationEntryPoint implements AuthenticationEntryPoint {
	
	public void commence(HttpServletRequest request, HttpServletResponse response,
			AuthenticationException authException) throws IOException, ServletException {
		
		String redirectUrl = UrlUtils.buildFullRequestUrl(request);
		String encoded = response.encodeRedirectURL(redirectUrl);
		response.sendRedirect(request.getContextPath() + loginPath + "?returl" + encoded);
	}
	..
}
```

**AuthenticationSuccessHandler 구현**
구현체 클래스에서 ``onAuthenticationSuccess` 메서드를 재정의한다.

```java
@Override
public void onAuthenticationSuccess(HttpSevletRequest...) {
	String retUrl = request.getParameter("returl");
	if (retUrl == null || retUrl.isEmpty()) {
		response.sendRedirect(request.getContextPath());
		return;
	}
	response.sendRedirect(retUrl);
}
```
returl 값을 받도록 구현.


#### 5.7.2. 인증 상태 쿠키에 보관
대규모 포털 등의 서비스는 인증 상태를 쿠키에 보관하기 위해 다음 작업을 처리해야 한다.

* 로그인 성공 시점
	* AuthenticationSuccessHandler에서 쿠키 생성
* SecurityContextPersistenceFilter 가 사용하는 SecurityContextRepository 커스텀 구현
	* loadContext 메서드 : 인증 쿠키로부터 Authentication 생성
	* saveContext 메서드 : 아무 동작하지 않는다
* 로그아웃 성공 시 쿠키삭제


**AuthenticationSuccessHandler 구현**
```java
@Override
public void onAuthenticationSuccess(HttpServletRequest request, ...) {

	// authentication 객체에서 principle 가져옴
	...

	// 이름과 권한들을 뭉쳐 쿠키로 생성
	String cookieValue = user.getUsername();
	for(GrantedAuthority auth : authentication.getAuthorities()) {
		cookieValue += ", " + auth.getAuthority();
	}
	
	// 쿠키 생성 및 암호화
	Cookie cookie = new Cookie("AUTH", URLEncoder.encode(cookieValue, "utf-8"));
	cookie.setPath("/");
	response.addCookie(cookie);
	...
{
```


**SecurityContextRepository 구현**
쿠키에서 Authentication정보를 얻어오는 부분 구현.
인증 성공 후 쿠키값을 이용해서 Authentication 객체를 생성하면 된다.

```java
@Override
public SecurityContext loadContext(HttpRequestResponseHolder holder) {
	
	SecurityContext ctx = SecurityContextHolder.createEmptyContext();

	// holder에서 쿠키를 추출하고
	// 이름과 권한을 얻음
	// Authentication 생성
	...

	Authentication auth = new UsernamePasswordAuthenticationToken(user, "", authorities);
	ctx.setAuthentication(auth);
	
	...
	
	return ctx;
}
```


**LogoutSuccessHandler로 로그아웃 구현**

```onLogoutSuccess``` 메서드를 재정의하여 쿠키를 삭제한다.

```java
@Override
public void onLogoutSuccess(HttpServletRequest request, ...) .. {

	Cookie cookie = new Cookie("AUTH", "");
	cookie.setPath("/");
	cookie.setMaxAge(0);
	response.addCookie(cookie);
	response.sendRedirect(request.getContextPath() + "/");
}

```

> logout 태그의 `delete-cookies` 속성을 사용하면 '/' 경로가 아닌 컨텍스트 해당 경로의 쿠키만 삭제된다. 이런 이유로 커스텀 핸들러를 구현한 것임


**설정**
커스텀 구현을 마친 후 security.xml 설정에서 변경해준다.
각 커스텀 구현체들을 빈으로 등록하고, ref로 연결해준다. 

```xml
<sec:http use-expression="true" entry-point-ref="커스텀" security-context-repository-ref="커스텀">
	
	...
	<sec:form-login authentication-success-handler-ref="커스텀">
	...
	
	<sec:logout logout-url="/user/logout" success-handler-ref="커스텀" />	
```

> 개선사항
> 
> 쿠키에는 사용자 식별할 수 있는 값만 넣고 `SecurityContextRepository` 커스텀 구현을 통해 권한 등을 DB나 외부 저장소를 이용하도록 구현해 볼 수 있다.


## 6. JSP 태그 라이브러리
스프링 시큐리티는 JSP에서 사용할 수 있는 커스텀 태그를 제공.

```jsp
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
```

`<sec:authorize>` : access속성에 지정한 권한값에 따라 태그의 몸체 내용을 보여준다. (가장 많이 사용되는 태그)

e.g) 인증된 경우에만 로그아웃 링크를 보여주고 싶다면

```jsp
<sec:authorize access="isAuthenticated()">
	<li><a href="<c:url value='/user/logout' />">로그아웃</a></li>
</sec:authorize>
```

**access 속성** : hasRole(), isAuthenticated(), hasAuthority() 

특정 경로에만 처리하고 싶으면 ```url```속성 이용
```jsp
<sec:authorize url="/admin/main">
```

`<sec:authentication>` 태그는 SecurityContext에 보관된 Authentication 객체의 값을 불러올 때 사용한다.

e.g) Authentication의 getPrincipal() 메서드의 리턴타입이 UserDetails라면
```jsp
<sec:authentication property="principal.username" />
```

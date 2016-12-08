# (Spring-Security) Password Encode

웹서비스를 개발하다보면 회원가입, 로그인 등 계정 관련하여 개발할 것들이 생긴다. 이 때, 비밀번호는 평문이 아닌 반드시 암호화를 하여 데이터베이스에 저장해야하는데, Spring Framework에서 비밀번호 암호화하는 방법을 알아본다.

Spring은 인증, 권한 등을 쉽게 개발하게 해주는 Spring Security를 제공한다. 내부에 비밀번호 암호화하는 기능도 포함이 되어 있어 이를 활용한 비밀번호 암호화를 해보자.

### PasswordEncoder

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


### Example

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



# Java Practice & JUnit Test

maven scope : test로 ! 실수할 여지 많음

Run Test code
```maven
mvn dependency:tree
```
말 그대로 dependency를 tree구조로 보여주는 명령어


* show white character space option ON
* github 소스 볼 때, 공백 기본값은 스페이스 8개. 이때 **?ts=4**
* .editorconfig 파일로 설정 가능
* yobi/common/git 참조


### Template 기능



# Servlet & JSP
* 웹서버 : apache, nginx
* 웹 애플리케이션 서버(WAS) : Tomcat

수많은 요청을 안정적으로 처리하기 위한 Scale out 고려.


## Tomcat
Web Application Server
웹 서버로부터 받은 요청은 개발한 Web Project에 전달하는 역할
####폴더 구조
* log : 톰캣 관련 폴더
* temp : 웹 프로젝트를 띄울 때 임시로 저장하는 공간
* work : webapps에 포함된 jsp파일 등을 컴파일하기 위해 필요한 파일들이 존재


### web.xml
WEB-INF/web.xml에 위치
웹 프로젝트와 관련된 설정파일, 없으면 안됨. 가장 중요

### Configuration
이클립스 상의 Server - tomcat 더블클릭.
Tomcat의 web.xml, conf 등의 파일을 불러와서 보여줌
Runtime config 은 사용할 JRE
Open launch configuration 에서 VMware부분에서 톰캣 메모리 설정 할 수 도 있음
Module탭에서 Base path등을 설정할 수 있다.

> **Tomcat에 바로 반영하는 기능 운영에서는 반드시 OFF !!**
> Tomcat 설정에서 변경가능. Server Option - Module auto reload by default

## Servlet
web.xml 에 servlet 태그에 추가한 서블릿을 등록해줘야한다.
마치 안드로이드에서 액티비티 추가할 때 매니페스트에 등록하는 것 처럼..

* servlet
	* servlet-name, servlet-class
* servlet-mapping
	* url-pattern, servlet-name

> jsp 페이지 위치에 따른 용도
> 
> * web 폴더 밑에 바로 둘 때 : 사용자에게 바로 보여줄 용도. Html, css 정도..
> * web/WEB-INF/ 폴더 밑에 : 사용자가 Direct로 접근을 할 수없다. 데이터를 정제해서 보여주는 용도, **보안 상**


## Logging & Exception
1. 에러를 볼 때 cause by 단위로 맨 아래부터 근본적인 원인을 확인하라
2. 에러가 나도 파악하기 힘든 것들은 **멀티 쓰레드** 환경
3. 뭔가를 파악하기 위해, 반드시
	4. 로그를 찍었나?
	5. 디버깅 해봤나?


### Logging
#### Log4J
로그 레벨이 어느정도 존재 fatal, error, warn, info, debug 로 나눠 찍는데,
너무 Debug레벨로 찍지는 않는다. 빈번하게 찍게되면 File IO때문에 성능 저하가 발생.

* Configuration
log4j.xml 설정에서 logger태그를 이용해서 클래스마다 로그레벨 설정 가능.
```xml
<logger name....
	<level>debug</level>
	....
```





# 보안
## 취약점
### SQL injection
1. or
2. 강제적인 주석 처리
3. union
4. 고의적인 Error

#### 해결책
PreparedStatement : 자체적으로 쿼리의 특수문자를 검증해줌

### XSS cross-site 취약점
사용자가 입력한 데이터의 검증없이 표시할 때 악의적인 스크립트를 삽입, 문제 발생
Form에 직접 스크립트를 입력했을 때 적용.

* Reflected XSS
URL, Cookie 탈취 기법, 스크립트 파일 삽입 등, 이미지 태그 등, alert 등

* 해결책
	* 입력된 값의 특수문자 검증을 통한 필터링

### CSRF(Cross-site Request Forgery) 취약점
블로그 친구추가, 공감, 스크랩 등의 상황에서 의도적인 Request스크립트를 작성하여 공격이 가능.


* Get Method 제한, 가급적 Post로
* Referer확인 : 자사 도메인 내에서의 입력만 받아들임. <img> 태그로 공격시 취약
* Security Token 활용 : 폼 생성 시 token발급. but, 개발 공수가 많이 든다. 

> **권장사항 : Get제한과 Referer확인**


#### 파라메터 변조를 이용한 공격
개인별 세션을 통한 검증으로 해결 가능하다

#### 파일 업로드 취약점
webshell.jsp를 통한 공격
위 파일을 업로드 구문을 통해 공격할 곳에 삽입. 웹서버의 권한으로 공격이 가능.

#### 해결책
1. 확장자 제한 : 그러나, 변조가능해서..
2. 암호화 등

#### 파일 다운로드 취약
다운로드 Url에 ../../../etc/passwd 등을 삽입하여 노출되는 취약점.

##### 해결책
1. 입력값에 대한 검증 필요.
2. 파일명 대신 글 번호 등의 Unique한 번호를 전달

#### Redirect 취약점
url 파라메터에 리다이렉트로 악성코드의 사이트로 강제 이동할 수 있기 때문에.
주소 필터링으로 해결 가능.

#### 브루트 포스 취약점
네이버 일회용 번호 로그인을 이용하여 8자리 번호를 브루트포스로 뚫릴 수 있음
입력 제한을 두거나 타임아웃 제한 등의 필터링 적용

#### SSRF 취약점
취약점이 존재하는 url을 통해 내부망으로 접근할 수 있다.

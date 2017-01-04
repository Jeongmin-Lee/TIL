# Maven

## Mac
####mvn 명령어 활성화 체크 
.bash_profile 에서 환경변수 변경

### Project 생성
Maven Project


### Lift Cycle
mvn command로 빌드 및 배포 가능
각 단계는 그 전 단계를 전부 수행완료된 후 수행됨.

1. compile
2. test
3. package : jar 또는 war
4. install : Local Repository에 배포, target 및 로컬 m2에도 배포됨.
5. deploy : Remote Repository에 배포

> e.g) mvn package
> ```maven
> mvn compile -> mvn test -> mvn package
> ```
> 
> 순으로 수행

#### 테스트를 skip하고 싶을 때
```maven
mvn -Dmaven.test.skip=true package
```
Bugfix시 수행하는데 상당히 오래걸림. 순식간에 반영할 때 Test를 스킵할 수 있다.


### Pom.xml
기본적으로 간단한 구조.
mvn 명령어를 통한 빌드 스크립트는 effective POM에 정의되어 있음

### STS에 내장된 Maven Version
별도로 설치한 maven과 STS자체에 내장된 maven은 엄연히 다름
__maven version은 통일하는 것이 좋다.__

### properties
1. version : 1.5.6 -> "major, minor, patch"
2. packaging : jar or war
3. groupId : company 단위, 그룹 단위 (e.g. com.navercorp)
4. artifactId : 세부적인 project명 같은
> 


### Dependency
Maven은 Dependency를 받을 때 일단 로컬부터 체크,
대용량의 파일을 네트워크로부터 받을 경우 중도에 끊겼을 때,
이어받게 되면 라이브러리가 불완전할 경우가 있음.
이때 __.m2 폴더에서 직접 Delete__
> m2 폴더경로는 "cd ~" 
> home에 숨김파일로 되어있음

pom.xml 의 규칙이 있음. dependency의 위치 지켜야.

* 의존성 제거
dependency할 라이브러리 내부의 특정 라이브러리를 제외할 때

```xml
<exclusions>
	<exclusion>
		//....
```
> exclusion은 dependency내부에 선언해야만 한다. 그리고 다른 dependency에 포함시키거나 단독적인 dependency를 정의하면 안됨. 같은 dependency에 포함시켜야 한다.

* 명시적인 Dependency
같은 라이브러리의 버전이 여러개 있을 경우,
우선순위를 가져갈 라이브러리나 특정한 버전 가져올 때

1. dependency의 순서
위에 포함된 라이브러리, 가장 위 부터 우선순위 

2. 명시적인 방법
가장 우선순위를 가짐


#### 디펜던시 문제 발생 case
* 라이브러리 파일 이상. 네트워크 불안정으로 인해
-> 클린해야
* 원하지 않은 라이브러리로 동작이 됨
-> 같은 라이브러리의 다른 버전이 동시에 존재하게 됨. 중복 존재 발생.

### Build Automatically
Eclipse의 project - Build Automatically 가 체크가 되어 있음. 

#### clean
* eclipse - project : Build auto로 된 결과물들을 깔끔하게 지움
* tomcat : 웹 프로젝트의 결과물을 지워. 뭔가 웹에 반영이 안될 때..

#### Maven - update
Gradle의 update dependency와 같은 역할.
빌드과정의 clean과정.

### Plugin
메이븐의 플러그인 설정. 부모 Effective POM에 설정된 플러그인 상속받아 사용하는데
__Override가능!!__
Plugin Repository에서 평소 라이브러리 가져오듯.

##### 플러그인 종류
1. surefire : JUnit Test 같은 플러그인
2. checkstyle : coding convention을 체크하는 플러그인
3. reporting : 각종 테스트 및 체크스타일 등의 수행 후 결과를 리포트 형식으로 

플러그인 내부 configuration tag 내부에 있는 exclude같은 속성은 자동완성이 안된다.


### Profile
각각의 다른 환경에 맞는 각 빌드를 커스터마이즈 할 수 있는 기능 제공

e.g. Local, dev, alpha, beta, real

* 다른 DB
* properties 파일
* Log4J.xml

> 예전에 푸르덴셜에서 SmallDB 를 만들어 개발 서버 환경 구축한 것과 비슷한 맥락

main/resource 밑에 각 환경에 따른 폴더와 파일을 생성해서 관리한다
예를 들어, resource-beta, ... 각 폴더에 properties파일과 각종 xml설정파일.
폴더 작명 규칙은 <build> 태그 밑에 resource 속성에서 resource-{env} 와 같이 설정 가능.

##### 프로젝트에 profile적용 방법
1. 각 설정파일들을 포함한 폴더를 src/main/resource에 생성
2. src/main/resource-local or dev, real 과 같이 형식에 맞는 폴더를 생성하고 profile종류에 맞는 설정파일을 생성한 후 폴더에 옮긴다.
3. pom.xml 에서 profiles 태그에 각 profile을 정의
4. build tag에 resources, resource의 각 디렉토리를 정하고 프로필 파일의 properties-env 값을 불러와야 하므로 ${env} 처럼 지정한다.

##### **example**
```xml
  <profiles>
  	<profile>
  		<id>dev</id>
  		<properties>
  			<env>dev</env>
  		</properties>
  	</profile>
  
  	<profile>
  		<id>release</id>
  		<properties>
  			<env>release</env>
  		</properties>
  	</profile>
  </profiles>
  
  <build>
  	<finalName>mywebproject</finalName>
  	<sourceDirectory>src/java</sourceDirectory>
  	<testSourceDirectory>src/test</testSourceDirectory>
  	<resources>
  		<resource>
  			<directory>src/main/resources</directory>
  		</resource>
  		<resource>
  			<directory>src/main/resources-${env}</directory>
  		</resource>
  	</resources>
  </build>
```

dev와 real 2개의 profile을 정한 후 maven-build configuration을 이용하여 maven build를 수행한다. Edit configuration의 Profile값에 빌드할 환경을 입력.


## JDK Version
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.6.0</version>
    <configuration>
        <source>1.8</source>
        <target>1.8</target>
    </configuration>
</plugin>
```

default로 1.5로 잡힌다. 1.8로 하려면 위와같이 pom.xml을 수정

or

```
mvn clean compile -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8
```

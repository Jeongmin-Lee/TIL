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

### Dependency
Maven은 Dependency를 받을 때 일단 로컬부터 체크,
대용량의 파일을 네트워크로부터 받을 경우 중도에 끊겼을 때,
이어받게 되면 라이브러리가 불완전할 경우가 있음.
이때 __.m2 폴더에서 직접 Delete__


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

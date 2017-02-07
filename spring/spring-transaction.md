# 스프링 트랜잭션
## 1. 트랜잭션?
여러 과정을 하나의 행위로 묶을 때 사용된다.
여러 단계를 수행했을때, 하나라도 실패하면 모두 취소되어야 한다. 이렇게 함으로써 데이터의 무결성을 보장한다. 모두 반영하거나 반영하지 않음.

## 2. 스프링의 트랜잭션 지원
선언적 트랜잭션 지원. 
트랜잭션의 범위를 코드 수준으로 정의 가능, 설정 파일 or 애노테이션을 이용한 규칙 및 범위 설정 가능

### 2.1. PlatformTransactionManager
트랜잭션은 PlatformTransactionManager 인터페이스를 이용해 추상화 했다.
DB연동 기술에 따라 각각의 구현 클래스가 제공된다.

실제 트랜잭션 처리할 때 PlatformTransactionManager를 사용하진 않는다. **선언적 트랜잭션** 방식으로 처리한다.

### 2.2. JDBC기반의 트랜잭션 설정
JDBC, MyBatis 등의 JDBC를 이용하는 경우 ```DataSourceTransactionManager``` 를 관리자로 등록한다.

이 클래스는 ```dataSource``` 프로퍼티를 통해 전달받은 Connection으로 commit, rollback을 수행하면서 관리한다.

### 2.3. JPA 트랜잭션 설정
JPA를 사용하는 경우는 ```JpaTransactionManager``` 를 사용한다.

이 클래스는 프로퍼티를 통해 전달받은 ```EntityManagerFactory``` 를 이용해서 트랜잭션을 관리한다.

### 2.4. JTA 트랜잭션 설정
다중 자원에 접근하는 경우 JTA(Java Transaction API)을 사용하는데, 이 때 ```JtaTransactionManager``` 를 사용한다.

빈으로 등록할 때 ```transactionManagerName``` 프로퍼티를 이용해서 JNDI 이름을 설정한다.

### 2.5. 트랜잭션 전파와 격리 레벨
현재 진행중이 트랜잭션이 있는 중 새 트랜잭션을 시작하고 싶다면?
새 커넥션으로 트랜잭션 시작할 수 있다.

스프링은 여러가지의 전파 지원과 격리레벨을 제공하고 있다. 각 지원 방식에 따라 값이 달라질 수 있다.

**트랜잭션 전파**

*  REQUIRED : 트랜잭션 필요. 진행 중이라면 해당 트랜잭션 사용. 없으면 생성
* MANDATORY : 트랜잭션 필요. 트랜잭션 존재하지 않으면 익셉션 발생
* NEVER : 트랜잭션이 불필요. 진행중인 트랜잭션 존재하면 익셉션 발생
* NESTED : 기존 트랜잭션 존재하면 중첩된 트랜잭션에서 메서드 실행
..


**트랜잭션 격리 레벨**
* DEFAULT : 기본 설정
* READ_UNCOMMITED : 다른 트랜잭션에서 커밋하지 않는 데이터 읽기 가능
* READ_COMMITED : 다른 트랜잭션에 의해 커밋된 데이터 읽기 가능
* REPEATABLE_READ : 처음 읽은 데이터와 두 번째 읽은 데이터가 동일
* SERIALIZABLE : 동일한 데이터에 대해 두 개 이상의 트랜잭션 수행 불가



## 3. TransactionTemplate을 이용한 트랜잭션
### 3.1. TransactionTemplate, TransactionCallback으로 처리하기
직접 처리하려면 템플릿 클래스를 이용한다.

구현방법.
1. ```TransactionTemplate``` 을 빈으로 설정
2. 프로퍼티에 ```DataSourceTransactionManager``` 입력
3. 코드에 적용

트랜잭션을 적용할 클래스에 ```TransactionTemplate``` 을 선언하고 트랜잭션을 묶을 지점에서 

```java
transactionTemplate.execute(
	new TransactionCallback<xx>() {
		@Override
		public xxxResult doInTransaction() {
			// 트랜잭션 처리할 로직들
		}
	});
```

execute 메서드로 처리할 로직들을 감싼다.

TransactionTemplate의 트랜잭션 처리 과정은 다음과 같다.

```sequence
내 코드->TransactionTemplate:1.execute(action)
TransactionTemplate->PlatformTransactionManager:2.getTransaction()
PlatformTransactionManager-->status:
PlatformTransactionManager-->TransactionTemplate:3.return status
TransactionTemplate->TransactionCallback:4.doInTransaction(status)
TransactionCallback-->TransactionTemplate:5.return result
TransactionTemplate->PlatformTransactionManager:6.commit
TransactionTemplate-->내 코드:7.return result

```

만약 doInTransaction 내에서 익셉션일 발생하면 TransactionTemplate에서 PlatformTransactionManager의 rollback 시킨 후, TransactionTemplate의 execute 메서드를 호출한 코드에 익셉션 전달한다.

throws를 통해 익셉션 발생을 설정하지 않기 때문에, ```RuntimeException```, ```Error타입의 익셉션``` 만 발생시킬 수 있다.

만약 다른 익셉션을 발생시킨다면, try-catch를 걸어 

```java
@Override
public Object doInTransaction(TransactionStatus status) {
	try {
		...
	} catch (Exception ex) {
		status.setRollbackOnly();
		return ex;
	}
}

```
롤백 여부를 설정해야 한다. 
익셉션 객체를 리턴함으로써 외부에서 접근 가능하다.

### 3.2. TransactionTemplate의 트랜잭션 설정

* 트랜잭션 전파 속성 : 필요(REQUIRED)
* 트랜잭션 격리 레벨 : DEFAULT
* 타임아웃 : 없음
* 읽기 전용 아님

템플릿 클래스는 위 4가지 속성을 가진다.
만약 다르게 지정하고 싶다면 관련 속성을 다르게 지정해야 한다. 

**트랜잭션 속성 관련 프로퍼티**

* propagationBehaviorName
	* 트랜잭션 전파 범위 설정.
	* PROPAGATION_REQUIRED(0)
	* PROPAGATION_SUPPORTS(1) 등
* isolationLevelName
	* ISOLATION_DEFAULT(-1)
	* ISOLATION_READ_UNCOMMIT (1) 등
* timeout : 초 단위로 타임아웃 값. 기본값은 -1 무제한.
* readOnly : true 지정하면 읽기전용 트랜잭션. false는 쓰기/읽기 트랜잭션 (default : false)

## 4. 트랜잭션과 DataSource
JDBC는 동일한 Connection인 경우에 트랜잭션 처리를 할 수 있다.

각 DAO에서 묶여 트랜잭션 실행이 되는 과정을 살펴보면,

```java
return transactionTemplate.execute(new TransactionCallback<T>..) {
	@Override
	public T doInTransaction(TransactionStatus status) {
		Adao.insert();
		..
		Bdao.insert();
		
		return new T(..);
	}
}
```

```JdbcTemplate``` 의 execute 메서드는 내부적으로 ```DataSourceUtils.getConnection(getDataSource())``` 를 수행하면서 Connection을 구해온다.

트랜잭션 범위에 있지 않으면 새로운 Connection을 리턴.
SimpleJdbcInsert 포함 다른 템플릿 클래스도 내부적으로 jdbcTemplate을 사용하므로 
_트랜잭션 진행 중일 때 같은 Connection_ 을 이용하게 된다.

getConnection 메서드는 ```DataSourceTransactionManager``` 처리를 통해 트랜잭션 범위 내에 있는지 알 수 있다. (jdbcTemplate이 내부적으로 Connection을 구할 때 사용)

```DataSourceTransactionManager```
트랜잭션 시작하면 DataSourceUtils에 알림
getConnection() 호출 시, 매니저가 시작한 트랜잭션과 연결된 Connection을 리턴.

> 주의!
> DataSource를 직접 사용하면서 스프링 트랜잭션 지원 기능을 사용할 때.
> 
> DAO에서 직접 DataSource를 통해 connection을 얻어올 때,
> ```java
> conn = dataSource.getConnection();
> ```
> 으로 가져올 경우 스프링 트랜잭션 범위에 해당하지 않는다.
> 
> 이 때는 
> ```java
> conn = DataSourceUtils.getConnection();
> ```
> 을 사용해서 Connection 을 가져와야한다.


## 5. 선언적 트랜잭션 처리
트랜잭션 템플릿과 달리 트랜잭션 처리를 코드에서 직접 하지 않고, _설정 파일이나 애노테이션_ 을 이용해서 범위, 롤백 등을 정의한다.

* ```<tx:advice>``` 태그
* @Transactional 애노테이션

### 5.1. tx 네임스페이스 이용한 설정
빈 설정 파일에서 tx 네임스페이스를 추가하여 트랜잭션 속성을 정의.

```xml
<bean id="transactionManager" class="o.s.jdbc.datasource.DataSourceTransactionManager"

...

<tx:advice id="txAdvice" transaction-manager="transactionManager">
	<tx:attributes>
		<tx:method name="order" propagation="REQUIRED" />
		<tx:method name="get*" read-only="true" />
	</tx:attributes>
</tx:advice>
```

advice 태그를 통해 advisor를 설정
attributes 내에 method를 설정한다.

**tx:method 태그의 속성**

* name : * 로 설정이 가능하다.
* propagation : 전파 규칙 설정. ex) REQUIRED, SUPPORTS..
* isolation : 격리 레벨
* read-only : 읽기 전용 여부
* no-rollback-for : 롤백하지 않을 익셉션 타입
* rollback-for : 롤백할 익셉션 타입
* timeout : 타입아웃 시간

실제로 트랜잭션 적용하는 것은 AOP를 통해 행해진다.

이전에 학습한 AOP를 이용해서 트랜잭션을 적용한다.

```xml
<aop:config>
	<aop:pointcut expression="execution(public *com.my.test..*())" id="servicePublicMethod"/>
	<aop:advisor advice-ref="txAdvice" pointcut-ref="servicePublicMethod"/>
</aop:config>
```

> tx:method 태그의 rollback-for / no-rollback-for 속성을 통한 롤백처리
>
> * rollback-for : 익셉션 발생 시, 롤백 작업을 수행할 익셉션 타입을 설정
> * no-rollback-for : 익셉션이 발생하더라도 롤백하지 않을 익셉션 타입
>
> ```xml
> <tx:method name="regist" rollback-for="Exception" no-rollback-for="MemberNotFoundException" />
> ```
> 
> MemberNotFountException 이 Exception을 상속받았다고 해도 익셉션이 발생하면 수행하지 않는다.
> 

### 5.2. 애노테이션 기반 설정
```@Transactional ``` 애노테이션은 메서드나 클래스에 적용되며 속성 설정이 가능.

```java
@Transactional(propagation=Propagation.REQUIRED)
```
propagation의 기본값은 REQUIRED.


#### 5.2.1. XML로 설정
애노테이션으로 트랜잭션을 적용하기 위해서는 
```<tx:annotation-driven>``` 태그를 설정해야 한다.

```xml
<tx:annotation-driven transaction-manager="transactionManager" />
```

annotation-driven 태그 속성은

* transaction-manager
* proxy-target-class : 클래스에 대해 프록시 적용할지 여부. true이면 ```CGLIB``` 을 이용하여 프록시 생성. false이면 자바의 ```다이나믹 프록시```를 이용 (기본 : false)
* order : Advice 적용 순서 (기본 : Integer.MAX_VALUE, 가장 낮은순위)

#### 5.2.2. 자바 설정
```@EnableTransactionManager``` 를 Config파일에 추가하여 트랜잭션 애노테이션을 사용할 수 있다.

```java
@Configuration
@EnableTransactionManagement
..
public class AppConfig {
	@Autowired
	private DataSource dataSource;
	
	@Bean
	public PlatformTransactionManager txManager() {
		DataSourceTransactionManager txMgr = new DataSourceTransactionManager();
		txMgr.setDataSource(dataSource);
		return txMgr;
	}
}
```

> @EnableTransactionManagement와 tx:annotation-driven 태그의 차이점
> 
> * tx 태그 : PlatformTransactionManager 빈의 _이름_으로 지정
> * 애노테이션 : PlatformTransactionManager _타입_의 빈을 지정. 만약 사용할 매니저를 직접 지정하고 싶을 경우, ```TransactionManagementConfigurer``` 인터페이스를 상속. ```annotationDrivenTransactionManager``` 메서드를 재정의해서 빈으로 등록.
> 


@EnableTransactionManager 속성

* proxyTargetClass
* order

#### 5.2.3. 트랜잭션 관리자 지정
2개 이상의 트랜잭션 관리자를 선언할 경우. 선택해서 지정할 수 있다.
@Transactional의 경우 value속성을 이용해서 빈의 id로 지정할 수 있다.

### 5.3. 트랜잭션과 프록시
트랜잭션 처리를 위해 빈 객체를 위한 프록시 객체를 생성. 이 프록시 객체는 PlatformTransactionManager 를 통해 트랜잭션 시작한 후 실 객체의 메서드를 수행 후 커밋을 한다.
하나의 객체에 대해 두 개 이상의 프록시 객체가 생성될 수 있다.

## 6. TransactionsEssentials 분산 트랜잭션
두 개 이상의 자원에 동시에 접근하는데 트랜잭션이 필요한 경우가 있음.
각 DAO마다 다른 데이터베이스를 접근하는 경우가 그 경우이다. DataSource는 서로 다르지만 하나의 트랜잭션으로 처리되야 한다.

자바에서 분산 트랜잭션 처리를 위해서는 서비스를 제공해주는 트랜잭션 관리자가 필요하다. (WebLogic, JBoss 자체적으로 지원 / 톰캣 같은 서블릿 컨테이너는 X)

이럴때, TransactionsEssentials 같은 트랜잭션 매니저를 사용한다.

> 최근 추세는 하나의 트랜잭션으로 묶어 처리하는 것 보다는, 메시징 시스템을 두고 비동기로 데이터를 동기화하는 방식을 선택. (성능 우선)
> 성능보단 트랜잭션 보장이 더 중요하다면 _글로벌 트랜잭션_

### 6.1. Maven설정
pom.xml에 두 개의 의존을 설정해야한다.

```
groupId : com.atomikos
artifactId : transactions-jdbc 3.9.3

groupId : javax.transaction
artifactId : jta 1.1
```

### 6.2. 스프링 연동

* JtaTransactionManager 설정
	http://www.atomikos.com/Documentation/JtaProperties 참고
* XADataSource 설정
	* AtomikosDataSourceBean : XA를 지원하는 JDBC 드라이버를 위한 DataSource설정
	* AtomikosNonXDataSourceBean : 지원하지 않는 드라이버를 위한 설정. XA에 호환되지 않아 트랜잭션의 원자성을 보장 X
* DAO등 빈에서 XADataSource 사용하도록
	* DAO 빈에 등록, 두 개 이상의 AtomikosDataSourceBean 등록해서 DataSource를 사용하도록 설정
	* 각 DAO에서 각각 정의한 DataSource 빈을 주입.
	* @Transactional 정의하여 트랜잭션 범위를 설정하면 끝. 각 DAO마다 다른 DataSource가 설정되어 있고 트랜잭션을 보장해준다.

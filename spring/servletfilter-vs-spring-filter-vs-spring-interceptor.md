# ServletFilter, Spring filter, Spring Interceptor의 차이점

# Spring Filter & Interceptor

Spring MVC 의 인터셉터의 설정파일은

```xml
<mvc:interceptors>
	<mvc:interceptor>
		<mvc:mapping path="/user/*">
		..	
		<bean class="com.xxx.인터셉터 클래스"/>
	</mvc:interceptor>
</mvc:interceptors>
```

필터의 설정파일은 
```xml
<filter>
	<filter-name>필터1</filter-name>
	<filter-class>com.xxx.필터클래스</filter-class>
</filter>
<filter-mapping>
	<filter-name>필터이름</filter-name>
	<url-pattern>/*</url-pattern>
</filter-mapping>
```

두 설정 모두 어떤 호출이던지 간에 매핑된 URL에 대한 필터나 인터셉터를 호출한다.
여기까진 비슷하다만, 차이점이 있다.


# RestTemplate

HTTP기반의 통신하는 경우 스프링에서 이를 위해 RestTemplate를 제공
RestTemplate은 동기적인 Http Client 클래스
RESTfult HTTP Server와의 커뮤니케이션을 간단하게 해준다.
HTTP Connection으로 작동되며, URL과 결과를 제공하는 코드가 있다.

기본 RestTemplate은 HTTP connection을 맺기 위해 기본 JDK에 의존한다. 개발자는 setRequestFactory 속성을 통해 Apache HttpComponents, Netty, OkHttp 등 같이 다른 HTTP 라이브러리로 바꿀 수 있다.

## 1. RestTemplate 기본 사용법

1. RestTemplate 객체 생성
2. 접근 메서드 사용해서 결과 받음

```java
RestTemplate template = new RestTemplate();
String body = template.getForObject("http://www.naver.com", String.class);
```

보통 필드로 많이 사용


`getForObject()` 메서드는 HTTP GET 방식으로 URL에 연결하여 결과를 String으로 구한다. 

String 말고 `HttpMessageConverter` 를 사용하면 JSON이나 XML응답으로 바로 자바 객체로 변환하는것이 가능.

```
postForObject()
put()
delete()
headForHeaders()
```
등 각 HTTP 방식별 메서드 존재

**RESTful 방식의 URL을 쉽게 구성할 수 있다**
경로 변수를 사용할 수 있는 메서드 제공

`http://localhost:8080/stores/1` 경로를 통해 데이터를 가져올 경우,
 
```java
String response = template.getForObject("http://localhost:8080/stores/{storesId}", String.class, "1");
```

마지막 매개변수가 `String...` 형 이므로 여러 경로 변수를 입력받을 수 있다.

```java
String response = template.getForObject("http://../users/{userId}/stores/{storesId}", String.class, "333", "1");
```

가변인자 대신 **Map** 사용
```java
Map<String, Object> params = new HashMap<>();
params.put("userId", "333");
params.put("storesId", "1");

String response = template.getForObject("http://../users/{userId}/stores/{storesId}", String.class, params);
```


### 1.1. 서버 에러 응답 처리
HTTP 통신하는 과정에서 문제 발생하면 `RestClientException` 을 발생시킨다.

상황별로 발생되는 `RestClientException`의 종류

* HttpStatusCodeException : 응답 코드가 에러
	* HttpClientErrorException : 응답 코드가 4xx
	* HttpServerErrorException : 응답 코드가 5xx
* ResourceAccessException : 네트워크 연결에 문제가 있을 경우
* UnknownHttpStatusCodeException : 알 수 없는 응답코드일 경우


에러처리할 때 해당 코드를 익셉션 처리한다.

```java
try {
	String response = template.getForObject("http://localhost:8080/stores/{storesId}", String.class, "1");
	...
} catch (HttpStatusCodeException e) {
	if (e.getStatusCode() == HttpStatus.NOT_FOUND) {
		...
	}
}
```


각 익셉션 마다 제공하는 메서드

1) 
```
HttpStatusCodeException
HttpClientErrorException
HttpServerErrorException
```
은 상태 코드를 구할 수 있도록 `HttpStatus getStatus()` 메서드 제공, 


2)
```
UnknownHttpStatusCodeException
```
은 `int getRawStatusCode()` 제공


3)
`ResourceAccessException` 을 제외한 나머지 익셉션에서 제공하는 메서드들

* String getStatusText() : 상태 문자값
* HttpHeaders getResponseHeaders() : 응답 헤더 리턴
* String getResponseBodyAsString() : ResponseBody 리턴



### 1.2. RestTemplate 주요 메서드 : GET/POST/PUT/DELETE

#### GET

`getForObject` 메서드 사용.

결과를 `ResponseType으로 지정한 타입` 으로 가져오거나 `ResponseEntity` 타입으로 가져올 수 있다.

> ResponseEntity
> 
> * getStatusCode() : HttpStatus 상태 코드
> * getHeaders() : HttpHeaders 리턴
> * getBody()
> 
> 메서드 제공


#### POST

```
postForObject
postForEntity
postForLocation
```
메서드를 사용할 수 있다.

request 파라미터는 Body로 전송되며 나머지는 GET과 동일.

```
postForObject
postForEntity
```
메서드는 ReponseBody를 구할 때 사용되고,
`postForLocation` 메서드는 결과로 응답의 `Location` 헤더값을 구할 때 사용된다.

> **Location**
> 
> 새로 생성된 데이터에 접근할 수 있는 URL을 Location 헤더에 담아 주는 경우.

#### PUT
```
void put(String url, Object request, Object... uriVariables)
void put(String url, Object request, Map<String, ?> uriVariables)
void put(String url, Object request)
```

#### DELETE
```
void delete(String url, Object... uriVariables)
void delete(String url, Map<String, ?> uriVariables)
void delete(URI url)
```


### 1.3. HttpMessageConverter를 이용한 타입 변환

GET/POST는 Body를 특정 객체로 변환하여 리턴.
POST/PUT을 위한 메서드로 전달한 객체를 Body로 변환.


`getForObject`, `postForLocation` 메서드에서 
```
JSON ==> Object

or 

Object ==> JSON 
```
방식으로 변환해주는 역할.

기본으로
```java
MappingJackson2HttpMessageConverter
Jaxb2RootElementHttpMessageConverter
```
컨버터가 사용되는데, _'RestTemplate'이 사용하는 'MessageConverter' 구현체를 변경하고 싶으면 ``setMessageConverter` 메서드를 사용한다._

### 1.4. exchange() 메서드로 RequestHeader 설정
RequestHeader 직접 설정할 때 사용.

```java
template.exchange("http://www.naver.com", HttpMethod.GET, requestEntity, Void.class);
```

HttpMethod, HttpEntity를 이용해서 설정

* HttpMethod : 전송 방식, GET/POST/PUT/DELETE/PATCH/OPTIONS/TRACE ...
* HttpEntity : RequestHeader, RequestBody를 설정할 수 있다.

사용 예
```java
HttpHeaders headers = new HttpHeaders();
headers.add("AUTHKEY", "myKey");
headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
HttpEntity<Void> requestEntity = new HttpEntity<Void>((Void) null, headers);
```


### 1.5. URIBuilder 이용한 URI 생성
연결할 URL을 지정하는 메서드로 사용할 수 있다. `UrlComponentsBuilder` 클래스와 함께 쉽게 생성할 수 있다.

```java
UriComponentsBuilder builder = UriComponentsBuilder.newInstance();
UriComponents uriComp = builder.scheme("http")
		.host("localhost")
		.port(8080)
		.path("/users/{userId}/stores/{storeId}")
		.build();

uriComp = uriComp.expand("333", "1").encode();
Uri uri = uriComp.toUri();


// 채이닝 방식으로
URI uri = UriComponentsBuilder.newInstance()
				.scheme("http")
				.host("localhost")
				.path("/users/{userId}/stores/{storeId}")
				.build()
				.toUri();
```


### 1.6. AsyncRestTemplate 이용한 비동기 처리
RestTemplate와 동일한 메서드를 지원하나 차이점은 _결과를 바로 받지 않고 `ListableFuture`를 타입으로 받는다_. 그리고 _RestTemplate은 동기 처리 방식_

```java
AsyncRestTemplate template = new AsyncRestTemplate();

template.getForEntity("http://www.naver.com", String.class)
	.addCallback(new ListenableFutureCallback<ResponseEntity<String>>() {
		
		public void onSuccess(ResponseEntity<String> result) {
			...
		}

		public void onFailure(Throwable ex) {
			...		
		}
	});
```

`ListableFuture` 타입 리턴하는데 결과 타입은 `ResponseEntity` 를 사용한다.

```java
@Override
public <T> ListenableFuture<ResponseEntity<T>> getForEntity(String url, Class<T> responseType, Object... uriVariables)
		throws RestClientException {

	...
```

## startActivity를 외부에서 시도할 경우

해당 액티비티가 아닌 타 액티비티에서 실행할 경우. 해결방법엔 3가지가 있다.

1. IntentFlag를 NewTask로
2. PendingIntent 사용
3. context가 아닌 activity로 전달


### Context가 아닌 activity로

```java
// 외부 클래스

public void startNewActivity(Context context) {
	Intent intent = new Intent(context, MainPagerActivity.class);
    intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
    context.startActivity(intent);
}

// 호출
startNewActivity(getApplicationContext());   // 실패

startNewActivity(AA.this); 		// Activity 자체를 넘김. 이러면 가능

```
위 처럼 액티비티 자체를 넘긴다.

.
.
.

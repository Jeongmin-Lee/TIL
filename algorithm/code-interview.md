# **Code-Interview 문제들 정리**

### Binary Tree에서 최대 Depth 구하기
Root노드 기준으로 좌측 노드들의 총 Depth와 우측 노드들의 총 Depth 중 가장 큰 값에 1을 더한 값
> MaxDepth = max(좌측Node의 maxDepth, 우측Node의 maxDepth) + 1

```java
int maxDepth(Node node) {
	if (node == null) {
		return 0;
	}

	int left = maxDepth(node.left);
	int right = maxDepth(node.right);

	return Math.max(left, right) + 1;
}
```

### Binary Tree에서 모든 노드의 갯수 구하기
Root노드 기준으로 좌측 노드들의 총 갯수에 우측 노드들의 총 갯수의 합에 1을 더한다

> 총 노드 수 = (좌측 총 노드 수 + 우측 총 노드 수) + 1

```java
int getAllNodeCount(Node node) {
	if (node == null) {
		return 0;
	}

	return getAllNodeCount(node.left) + getAllNodeCount(node.right) + 1;
}
```



### 문자열 뒤집기
문자열을 뒤집는 메서드를 만들어라. 가령 EFFECT를 입력했다면 TCEFFE를 출력해야한다.

```java
public String reverseString(String str) {
	StringBuffer sb = new StringBuffer();
	char[] chs = str.toCharArray();
	Stack stack = new Stack();

	for (char c : chs)
		stack.push(c);

	while(!stack.isEmpty())
		sb.append(stack.pop());

	return sb.toString();
}
```


### 문자열 압축
문자열을 압축하는 메서드를 구현하라.
> 예를들어, <br>
> A -> A1 <br>
> AAAABB -> A4B2 <br>
> AAAAABBBCDDAAA -> A5B3C1D2A3

위와 같이 반복되는 문자의 수를 포함하여 문자열을 만든다.

```java
public String compactString(String input) {
	if (input.isEmpty()) {
		return "";
	}

	char[] chs = input.toCharArray();
	char temp = chs[0];
	int count = 0;
	StringBuffer sb = new StringBuffer();

	for (char ch : chs) {
		if (ch != temp) {
			sb.append(temp).append(count);
			count = 0;
			temp = ch;
		}
		count++;
	}

	sb.append(temp).append(count);

	return sb.toString();
}
```


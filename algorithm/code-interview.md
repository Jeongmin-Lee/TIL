# **Code-Interview 문제들 정리**

###Binary Tree에서 최대 Depth 구하기
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

###Binary Tree에서 모든 노드의 갯수 구하기
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

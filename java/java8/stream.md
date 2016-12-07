# Java8 Stream API
Java에서 제공하는 Collection들을 더욱 효과적으로 다룰수 있도록 도와준다.


#### List Collection에 있는 요소들의 합 구하기
가령 Player 리스트에서 각 Player가 가진 돈의 합을 구하고자 할 때, 단 몇 줄로 손쉽게 계산할 수 있다.

```java

// Player class
class Player {
	String name;
	int money;
	//....
	
	int getMoney() {
		return money;
	}
	//...
}


// Money의 합 구하기
public int sumOfPlayers(List<Player> players) {
	int sum = players.stream()
				.mapToInt(player -> player.getMoney())
				.sum();
	return sum;
}

```





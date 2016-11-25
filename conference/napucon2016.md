# 나는 프로그래머다 컨퍼런스(NapuCon 2016)

## 참석한 세션
1. 스칼라와 함수형 프로그래밍 기초 (케빈 리)
2. Machine Intelligence at Google Scale (Kaz Sato)
3. 지적 프로그래밍을 위한 넓고 얕은 습관 (서지연)
4. 본격 서버리스 개발기 (데니스)
5. '스타트업 1인 개발 극복기'와 'Javascript VS Scala, (함수형 언어 관점으로) 방황기'

### 스칼라와 함수형 프로그래밍 기초 (케빈 리)
Functional Programming, 동시성, 간결함
간단한 하스켈의 시연과 함께 스칼라 시연

```
1.toString()
```
위의 예제에서 Java는 불가하지만 Scala는 가능, 왜? Primitive type 또한 Object로 판단


### Machine Intelligence at Google Scale (Kaz Sato)
NN의 간략한 소개와 함께 약 60개의 Google Service에 Machine Learning 서비스를 녹여냄. Tensorflow의 소개. Speech API를 시연하였는데, 굉장히 신선했음. 임백준님이 한국어로 이런저런 이야기를 하자마자 내용을 인식하고 Text영역에 그대로 문장을 출력함.

### 지적 프로그래밍을 위한 넓고 얕은 습관
#### 코드리뷰 관련 툴
- SonarQube(http://www.sonarqube.org/)
- Pull Approve(https://about.pullapprove.com/) : Github PR관련 플러그인
- CI(Continuous Integration)
  - Jenkins
  - Travis CI(https://travis-ci.org/)
  - goCD(https://www.go.cd/)


#### 기타 등등
- Github Ranking : 한국 사용자 순위(http://rankedin.kr/users), 전세계(https://github-ranking.com/)
- 책 : 그림자 노동의 역습
- Devnews(devnews.kr) : 새로운 기술 관련 뉴스들


### 본격 서버리스 개발기
SLA 중요함. 지진이 발생했을 때 국가안전처 사이트 마비 사례 예시 듬. CDN을 놓으면서 해결하는것이 어떨까? 클라우드의 자원을 적극활용하면서 비용을 절약하고 (AWS Lambda를 여러 계정으로 돌려가며 비용을 절감) 개발에 집중해야 한다.
Google App Engine도 괜찮다.


### '스타트업 1인 개발 극복기'와 'Javascript VS Scala, (함수형 언어 관점으로) 방황기'
스타트업 개발자들에게 함수형 언어의 필요성을 전파함. 매주마다 개발자 세미나를 열어 지속적으로 공유 및 세뇌(?). Javascript를 함수형 언어처럼 짜면서 익숙해지도록. 점점 개발자들이 흥미를 느껴 서비스에 도입하기 시작. Test를 작성할 때 Mock를 만들어 Test를 해보는데 함수형 언어의 불변성을 활용하니 좋음. Mock이 필요없음. Test를 쉽게 할 수 있음.


#### 후기
사실 그닥 끌렸던 세션들은 아님. Deview나 NDC등의 컨퍼런스와 비교한다면 기술적인 디테일은 약함. 하지만 라이브 코딩하면서 친숙하게 접근할 수 있도록 한것은 좋았음. 확실히 Scala, Haskel 등등 함수형 프로그래밍의 중요성을 더욱 커지는 것 같음. 패러다임을 익힐 겸 대표적인 함수형 언어를 배울 필요성을 느낌. 의외로 서지연님의 세션이 도움이 됨. 당연한 말들처럼 느껴지지만 초보 개발자가 초고수로 가기위해 취해야 할 행동들, 습관들을 정의하고 하나씩 해나가야 한다는 것에 공감이 됨. 다양한 코드리뷰 툴을 알게되었고 아름다운 코드를 위한 노력 등을 보며 주니어 개발자인 나도 점진적으로 노력해야겠다는 생각이 듬.
마지막 네트워킹 이후 남은 캔맥주를 많이 챙겨서 상당히 만족 :)

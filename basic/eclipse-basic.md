# Eclipse 의 기본 사용법

## STS 메모리 설정
Eclipse는 메모리를 잡고 들어감
ini 설정 파일에서 xms, xmx 설정이 필요
default 512 -> 4g 정도
작게 설정하면 gc 수행빈도 상승, stop the world의 시간이 길어짐으로 인해 성능 저하....
> 두 값은 같게, 어차피 최소값으로 해도 넘어갈 때 다시 할당하므로 그냥 두 값을 같게 해버림.. 

## Package Exploror
Flat이 권장된다고..???
클래스가 많을 경우 찾을 depth를 줄이기 위해
근데 난 계층형이 좋음.!

## Plug-in

## Configuration
각 폴더마다 값이 달라짐
encoding : UTF8 설정해야함, eclipse default : MS949
> DB, apache, tomcat, raw data, eclipse, class file, etc.... 인코딩 통일, 깨질 수 있기 때문. 중도에 변경하기가 굉장히 까다로움.
> 왜 ? 
 __General - content Types 에서 인코딩 설정해야 매번 생성하는 파일에 대해서도 적용됨. 중요!__ 


### console buffer size
콘솔에 찍는 로그의 수는 실 프로젝트 수행시 엄청나게 클 경우가 많음. max값으로

### Server 설정
Tomcat 8.0 기본으로 감. 교육에서는

## Java Version 통일
minor version 조차도.

## Debug
#### View 활용
window - show view의 Variable, Expression 등의 뷰를 잘 활용하기
Inspector, display, watch 는 우클릭 또는 단축키로
Step Over, Step Into등 사용법, 단축키 익히기
Drop to Frame - 디버크 콘솔에서 우클릭해서 사용

#### Hit Count
특정 for문 n번째를 확인하고 싶을때, Hit Count ⇒ Suspend Thread, VM

#### Exception Debugging
익셉션으로 디버깅 : J! 모양의 아이콘 클릭. -> 어떤 익셉션일지 고를 수 있음

### 단축키
Quick Fix, 등등 익혀두면 좋음

1. Resource 검색 : ctrl + shift + R
2. 클래스 검색 : c + shift + T

## Tip
Clean : 결과물 반영 잘 안될 때

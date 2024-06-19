# 2024-1-DSCD-BLINK-5

## [최적의 포트폴리오 구성을 위한 심층 강화학습 알고리즘 개발 : 시장규모 및 산업군 세분화를 고려한 접근]

### Team Info
- 멘토 : 고려대학교 김성진 (고려대 인공지능학부 박사과정)
- 팀장 : 김남민 (경영학과)
- 팀원 : 박정민 최연아 (산업시스템공학과)

### 과제 개요
- 시장 규모에 따른 자산 종류 (Big, Mid, Small Cap) 의 다양성 확보와 산업군 세분화를 통한 접근법으로 시가, 고가, 저가, 종가, 거래량 5가지 데이터 특성을 모두 고려하여 기존 연구의 한계점을 극복한 “최적 포트폴리오 구성을 위한 심층 강화학습 DQN 모델"을 개발하였다.

### 기존 연구의 한계점
- 시장 규모가 큰 Big-Cap의 일부 종목만을 고려하여 종목(자산)의 다양성 부족하다는 한계가 있으며, 각 종목의 특징적인 요소들을 함께 고려하지 않았고, 여러 주가 데이터 중 종가 데이터만을 가지고 연구했다는 점에서 한계점이 명확하다.

### 한계점 극복을 위한 접근법
- 선행 연구의 한계점 극복을 위해 본 연구는 시장규모가 큰 Big-Cap, Mid-Cap, Small-Cap 종목을 모두 고려하여 종목(자산)의 다양성을 확대하였고, 각 종목을 산업군(섹터) 별로 세분화 및 클러스터링하여 산업군의 특성 또한 실험에서 고려하였으며, 종가 뿐만 아니라 Open시가, High고가, Low저가, Close종가, Volume거래량을 모두 고려한 실험을 진행하였다.

### DB 구축 (한국 - KOSPI, KOSDAQ, 미국 - NYSE, NASDAQ)
- investing.com, stockanalysis.com, KRX(한국거래소) 홈페이지에서 KOSPI, KOSDAQ, NYSE, NASDAQ 주식 DB를 구축하였다. 
- 데이터베이스는 종목코드 DB, 종목별 시가총액 DB, 종목별 과거주가 DB로 구성되어 있으며 데이터 수집 방법으로는 POSTMAN을 이용한 API request, Google API를 이용한 SpreadSheet 자동화 방법을 채택하였다. 
- 선정된 최종 데이터는 각 거래소 별 시가총액 상위 500개(Big- Cap 100개, Mid-Cap 200개, Small-Cap 200개)의 종목이며, 한국 주식의 경우 2012년~2022년을 Train Data, 2023년을 Test Data로 세팅하였고, 미국 주식의 경우 2010년~2022년을 Train Data, 2023년을 Test Data로 세팅하였다.

### 모델 구축 & 실험
- Pytorch의 Lightning 프레임워크를 활용한 DQN(Deep Q-Network) 모델 구현 (모델 학습의 주요 목표는 포트폴리오의 수익률을 극대화하고 위험을 최소화하는 것)
- Loss Function (5가지 투자전략) 수립 및 거래소별 실험을 통한 최적의 손실함수 도출 : 강화 학습에서 손실 함수는 에이전트가 환경과의 상호작용을 통해 얻은 경험을 학습하는 데 중요한 역할을 하고 다른 학습 관점을 제공하는데 본 연구에서는 최적의 손실 함수 세팅을 위한 실험을 진행하였다 ; (1) Action-Amount Value Combined Loss (action X amount), (2) Action-Only Loss (action), (3) Amount-Only Loss (amount), (4) Combined Action-Only and Amount-Only Loss (action + amount), (5) Comprehensive Loss (action * amount + action + amount).
- 각 거래소별 최적의 Loss Function을 적용한 모델 채택 및 산업군별 투자 전략 적용 : 총 11가지 산업군 기반으로 산업군 인덱스를 할당하고 산업군별 계층적 softmax를 적용하여 최종 PROPOSED 모델 수립. (섹터 : 금융 / 기술 / 부동산 / 산업 / 소비순환재 / 소재 / 아카데믹 및 교육 서비스 / 에너지 / 유틸리티 / 필수소비재 / 헬스케어)

### 실험 결과
- Proposed의 수익률과 종합주가지수(INDEX) 비교

1. [한국] KOSPI
=> 수익률 : 28.17%, INDEX : 14.31 %, 샤프 지수 : 0.94
<img width="451" alt="image" src="https://github.com/CSID-DGU/2024-1-DSCD-BLINK-5/assets/128684050/900aa9ae-06f1-4407-959f-7006e1a38fe0">

2. [한국] KOSDAQ
=> 수익률 : 34.74%, INDEX : 25.18 %, 샤프 지수 : 1.25
<img width="470" alt="image" src="https://github.com/CSID-DGU/2024-1-DSCD-BLINK-5/assets/128684050/553c5224-e05c-428c-9ff1-346da69e187f">

3. [미국] NYSE
=> 수익률 : 17.06%, INDEX : 9.60 %, 샤프 지수 : 0.58
<img width="451" alt="image" src="https://github.com/CSID-DGU/2024-1-DSCD-BLINK-5/assets/128684050/2f2a1496-9bc3-4b90-bb17-3da51e9ac9ec">

4. [미국] NASDAQ
=> 수익률 : 152.82%, INDEX : 42.62%, 샤프 지수 : 3.73
<img width="450" alt="image" src="https://github.com/CSID-DGU/2024-1-DSCD-BLINK-5/assets/128684050/6fa5b500-e69f-4c21-8c39-6e627ec9d198">

4가지 거래소 모두, 단위 리스크당 수익률(샤프지수)이 인덱스에 비해 더욱 안정적인 현상을 보임.


### 향후 계획
- 미국 시장 테스팅 및 PPO 알고리즘으로 디벨롭 후, 2024.08-09월 중 IEEE ACESS submit 예정.

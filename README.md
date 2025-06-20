# Big-Data-Analysis-Professional
빅데이터 분석기사 실기 준비

# 1 유형

## Pandas 문법 기초

### 기본 활용 문법
  - 데이터 읽어오기 : read_csv(“”,sep=“\t”), 한국어는 encoding="euc-kr" 추가
  - 각 칼럼 내 고유값 수 출력 : nunique( )
  - 각 항목별 개수 : value_counts( )
  - 자료형 변경 : astype( )
  - 특정 행 삭제 : df.drop(1, axis = 0) → 1번 행만 선택해서 삭제*df = df.drop(~~)과 같이 기존 객체명에 적용해야 삭제 반영됨
  - csv로 저장 : to_csv(’파일명’, index=False) → 인덱스값 저장하지 않음
  - 인덱싱/슬라이싱
    - loc vs iloc- loc : 인덱스 이름 / 마지막 선택자 포함 o- iloc : 인덱스 번호 / 마지막 선택자 포함 x

### 수치형 변수
  - describe() : 개수, 평균, 표준편차, 25%, 50%, 75%, 최솟값, 최댓값
  - agg(['mean', 'var', 'min', 'max']) : 주어진 값만 계산

### 인덱싱 예시
  - loc는 True 인 경우만 인덱싱 함
  - df.loc[1:2, '가격':'칼로리']
  - df.iloc[1:3, 1:]

  - 데이터 추가
    - import numpy as np

#### 결측치로만 이루어진 ‘원두’ 칼럼 추가
  - df['원두'] = np.nan

#### 리스트 형태로 데이터(행) 추가
  - df.loc['시즌'] = ['크리스마스라떼', 6000, 500, '한국']

#### 딕셔너리 형태로 데이터(행) 추가
  - df.loc[5] = {'메뉴':'에소프레소', '가격':2000, '칼로리':10}

### 정렬 (sorting)
  - sort_index(ascending=False)→ ‘인덱스’ 기준 내림차순 정렬
  - sort_values(’칼럼명’, ascending=False)→ ‘칼럼’ 기준 내림차순 정렬
 
#### 여러 칼럼을 기준으로 할 경우 칼럼명과 옵션 모두 list로 묶어줘야 함
  - df = df.sort_values(['가격', '메뉴'],ascending=[False, True])
  - reset_index(drop=True)→ 정렬한 기준대로 새로운 인덱스값 생성, 기존 인덱스값은 지움
  - set_index(’칼럼명’, inplace=True, drop=True)→ inplace=True (원본에 바로 반영) / drop=True (해당 칼럼을 데이터프레임에서 삭제)

### 조건필터
1. 1개 조건
    - df.loc[df['할인율'] > 0.2]

2. 2개 조건
    - cond1 = df['할인율'] >= 0.2
    - cond2 = df['칼로리'] < 400
    - df.loc[cond1 & cond2]
    - df.loc[cond1 | cond2]

3. 조건 부정
    - df.loc[~cond1]
      - cond1의 true를 false로, false를 true로 바꿔 true만 인덱싱

#### 결측치 & 값 변경
  - 문제 풀 때는 결측치 제거 전후로 shape를 print하여 데이터 형식 변화 비교해보기
  - 칼럼별 결측치 확인 : df.isnull().sum()
  - 결측치 채우기 : df[’칼럼명’].fillna(’채울 값’), loc[df['컬럼명'].isnull(), '컬럼명'] == '채울값'
  - 값 변경 : replace(’기존 값’, ‘변경할 값’)

#### 여러 문자 변경 : 아메리카노 -> 룽고, 녹차 -> 그린티
  - df.replace('아메리카노', '룽고').replace('녹차','그린티')

#### 딕셔너리 활용
  - d = {'아메리카노':'룽고', '녹차':'그린티'}
  - df = df.replace(d)
    * 결측치 제거 : df.dropna()
    * 특정 칼럼을 기준으로 할 경우 df.dropna(subset=[’칼럼명’])

#### 내장함수
  - 왜도
    - df[’칼럼명’].skew()
  - 첨도
    - df[’칼럼명’].kurt()

#### 하위 25% 값
  - df[’칼럼명’].quantile(.25)
#### 상위 25% 값
  - df[’칼럼명’].quantile(.75)

#### 최빈값
  - df[’칼럼명’].mode()[0]
    - [0]이라고 인덱스를 지정해줘야 값만 추출됨

#### groupby
  - '원두' 칼럼 기준 평균
    - df.groupby('원두').mean()

  - '원두'와 '할인율' 기준, 가격 평균
    -  df.groupby(['원두', '할인율'])['가격'].mean()

  - 1개 인덱스 형태로 리셋 -> 이렇게 해야 기존 df의 인덱스 형태를 띔
    - df.groupby(['원두', '할인율']).mean().reset_index()

  - 항목별 빈도수 구하기
    - df.groupby('컬럼명').size()
    - count() 와 비슷하지만 모든 행을 다 세어줌

  - 계층적 인덱스
    - df.groupby(['컬럼명', '컬럼명'])
      - 이 경우 두 컬럼 모두 인덱스로 사용되어 계층적 인덱스 사용
    - df.groupby(['컬럼명', '컬럼명'], as_index=False)
      - 인덱스를 사용하지 않겠다. 컬럼으로 유지
    - df.groupby(['컬럼명', '컬럼명']).unstack()
      - 두번째 인덱스를 컬럼으로 바꿔줌

### 시계열 데이터
  - object에서 날짜형 데이터로 변환 : pd.to_datetime(df[’칼럼명’])
#### 연도가 4자리일 때 : %Y (대문자), 연도가 2자리일 때 : %y (소문자)
  - df['Date2'] = pd.to_datetime(df['Date2'], format="%Y:%m:%d")

  - '%Y년%m월%d일', '%y-%m-%d %H:%M:%S', '%Y-%m-%d %H-%M-%S' 등 다양한 포맷에 맞춰 변환 가능
  - 시계열 데이터 칼럼에서 년/월/일/시간/요일 정보 각각 출력 가능df[’칼럼명’].dt.year (혹은 month, day, hour, minute, second, dayofweek)
  - 요일 출력 (숫자로 반환) : df[’칼럼명’].dt.dayofweek
  - 영문 요일명 출력 : df[’칼럼명’].dt.day_name()
  - datetime 간의 연산 결과를 기간(시, 분, 초..)으로 변환 : dt.total_seconds()timedelta 자료형에만 적용 가능
  - diff = df['100일'] - df['100시간'] # 94 days 20:00:00

  - print(diff.dt.total_seconds()) # 초 : 8193600.0
  - print(diff.dt.total_seconds()/60) # 분
  - print(diff.dt.total_seconds()/60/60) # 시간
  - print(diff.dt.total_seconds()/60/60/24) # 일

#### 주의
  - print(diff.dt.seconds) # 72000
  - dt.seconds는 '시간'에 대해서만 계산한 것이므로 '일'은 포함하지 않고 20시간을 초로 환산한 값만 반환
  - 따라서 'total_seconds'를 사용해야 정확히 계산 가능

### 문자열 데이터
  - 문자열 값 변경 : replace()
  - 변경하고자 하는 전체 문자값이 일치해야 정상 변경됨
  - 일부 문자만 변경하고자 할 땐 ‘str’이라는 접근자 사용해야 함
  
  - str[0] : string 변수의 첫문자
  - str.len() : string 변수의 문자 길이 반환

  - 어절 나누기 : split()
    - A 칼럼 띄어쓰기 기준 어절 나누기
      - df['A'].str.split()

  - 어절 나눈 후 첫 번째 값 선택
    - df['A'].str.split().str[0]
  
  - 접근자를 한번 더 사용해야 첫번째 값들만 출력 가능
  - 접근자 사용하지 않을 경우 첫번째 행이 출력됨

  - 슬래시'/' 기준 어절 나누기
    - df['C'].str.split('/')
    - 특정 문자 찾기 : df.str.contains(’찾을 문자’)
    - df.isin([’문자열1’, ‘문자열2’…])⇒ isin 함수는 여러 단어를 한번에 찾을 수 있는 장점이 있으나 일부 단어만 찾는 건 불가능

출처 : https://1020archive.tistory.com/3

## 데이터프레임

  - df['new_price'] -> series 형식
  - df[['new_price']] -> dataframe 형식
  - df.to_frame() -> frame 형식으로 바꿈
    - to_frame('새로운 컬럼명'), to_frame().rename(columns= {'count' : '새로운 컬럼명'})   (여기서 count는 만든 컬럼명의 디폴트값)

#### 데이터프레임 연산 (어려움)
  - 일단 차원이 맞는지 확인
    - .shape
  - reshape(-1,1)를 통해 1차원을 2차원으로 변경
    - (5, ) -> (5, 1)

#### 중복행 제거
  - 컬럼을 기준으로 중복행 제거(첫번째 케이스만 남김)
    - drop_duplicates('컬럼명', keep='first')   // keep='first' 디폴트값
  - 컬럼을 기준으로 중복행 제거(마지막 케이스만 남김)
    - drop_duplicates('컬럼명', keep='last')


























# 2유형

실기 대비 명령어 정리

데이터 불러오기
import pandas as pd
data = pd.read_csv("위치/파일명.csv")
 
행렬 몇x몇인지 확인, 데이터 열 확인
print(data.shape)
print(data.columns)
 
데이터의 기초통계량 확인 (데이터 개수, 평균, 표준편차, 사분위수, 최댓값, 최솟값)
데이터의 요약정보 확인 (컬럼별 null 여부, 타입, 데이터 크기 등)
print(data.describe())
print(data['특정컬럼'].describe())

print(data.info())
 
데이터 정렬하기
 // 컬럼명1을 기준으로 내림차순 후 컬럼명2를 기준으로 오름차순
target = data.sort_values(by=['컬럼명1', '컬럼명2'], ascending=[False, True])
 
데이터 중복제거 값 구하기 (전처리 가공 대상 확인을 위함)
print(data['컬럼명'].unique())
 
컬럼 간 상관관계 구하기 (-1~1 사이 값을 가지며, 절댓값 0.6 이상의 경우 상관관계가 있다고 봄)
print(data.corr())
 
독립변수와 종속변수 만들기
X = data.drop(columns = '종속변수 컬럼명')
Y = data['종속변수 컬럼명']
 
행, 열 다듬기
X = data.iloc[:,:] # [행범위,열범위]
 
결측치 확인 후 대치하기
print(data.isnull().sum()) # 결측치 확인

target_col_mean = data['타겟'].mean()
data['타겟'] = data['타겟'].fillna(target_col_mean) # 평균값 대치

target_col_median = data['타겟'].median()
data['타겟'] = data['타겟'].fillna(target_col_median) # 중위값 대치

data.drop(columns=['타겟']) # 결측치 삭제
 
잘못된 값 바꾸기
print(data['타겟'].unique()) # 잘못된값 있는지 확인
data['타겟'] = data['타겟'].replace('잘못된값', '올바른값')
 
이상값 처리하기
# 사분범위 활용
iqr = data.describe().loc['75%'] - data.describe().loc['25%']

print(data.loc['75%'] + (1.5 * iqr)) # 최대 경계값 확인
print(data.loc['max']) # 최댓값 확인
data.loc[[타겟인덱스], '타겟컬럼'] = 최대 경계값 # 최대 경계값보다 최댓값이 큰 경우, 값을 최대 경계값으로 수정

# 최소이상값은 25%에서 1.5*iqr 빼서 동일하게 처리

# 평균과 표준편차 활용
# 최대 경계값 = 평균+1.5*표편,  최소 경계값 = 평균-1.5*표편
def outlier(data, column) :
    mean = data[column].mean()
    std = data[column].std()
    lowest = mean - (1.5*std)
    highest = mean + (1.5*std)
    outlier_index = data[column][(data[column]<lowest) | (data[column]>highest)].index
    return outlier_index
 
스케일링 
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

temp = data[['타겟컬럼']]
# 아래 셋 중 적절히 선택
scaler = StandardScaler() # 표준크기변환 - 평균0 표편1
scaler = MinMaxScaler() # 최소-최대 크기변환 최소0 최대1
scaler = RobustScaler() # 로버스트 크기변환 중앙0 IQR 1

scaler_result = pd.DataFrame(scaler.fit_transform(temp))
 
데이터 타입 변경
data['타겟컬럼'] = data['타겟컬럼'].astype('int64')
 
인코딩
# 원 핫 인코딩
print(pd.get_dummies(data['타겟컬럼'])
print(pd.get_dummies(data['타겟컬럼'], drop_first=True) # 타겟컬럼 값이 두가지일 경우 하나 드롭해서 사용 가능

# 라벨 인코딩
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
print(encoder.fit_transform(data['타겟컬럼']))

# 수동(replace) 인코딩
data['타겟컬럼_new'] = data['타겟컬럼'].replace('값1', 0).replace('값2', 1)
 
파생변수 생성
condition = data['타겟변수'] < 3.3
data.loc[condition, '파생변수'] = 0
data.loc[~condition, '파생변수'] = 1

data['파생변수2'] = data['타겟변수2'] * 4
 
train, test 분리
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(data_X, data_Y, test_size=0.3)
 
선형회귀 (연속형 종속변수)
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(x_train, y_train)
y_train_predicted = model.predict(x_train)
y_test_predicted = model.predict(x_test)

# 도출된 y 절편 값
print(model.intercept_)

# 독립변수별 도출된 기울기 값
print(model.coef_)
 
랜덤 포레스트 회귀 (연속형 종속변수)
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor()

# 트리 1000개 생성, 평가지표를 MAE 활용하라 등의 요구가 있을 경우 하이퍼파라미터 활용
model = RandomForestRegressor(n_estimators=1000, criterion='mae')

model.fit(x_train, y_train)
y_train_predicted = model.predict(x_train)
y_test_predicted = model.predict(x_test)
 
그레디언트 부스팅 회귀, 익스트림 그레디언트 부스팅 회귀 (연속형 종속변수)
from slearn.ensemble import GradientBoostingRegressor
from xgboost import XGRegressor

# 택1
model = GradientBoostingRegressor()
model = XGRegressor()

model.fit(x_train, y_train)
y_train_predicted = model.predict(x_train)
y_test_predicted = model.predict(x_test)
 
평가지표 (연속형 종속변수)
from sklearn.metrics import r2_score, mean_absolute_error, mean_sqared_error
import numpy as np

# train은 1에 가까우나 test가 낮으면 과적합

# 결정계수 (0~1, 1에 가까울수록 좋음)
print(model.score(x_train, y_train))
print(model.score(x_test, y_test))

# r2_score (0~1, 1에 가까울수록 좋음)
print(r2_score(y_train, y_train_predicted))

# MSE (0에 가까울수록 좋음)
print(mean_sqared_error(y_test, y_test_predicted))

# RMSE (0에 가까울수록 좋음)
print(np.sqrt(mean_sqared_error(y_test, y_test_predicted)))

# MAE (0에 가까울수록 좋음)
print(mean_absolute_error(y_test, y_test_predicted))
 
의사결정나무 분류, 랜덤 포레스트 분류, 익스트림 그레디언트 부스팅 분류 (범주형 종속변수)
from sklearn.tree import DecisionTreeClassifier, RandomForestClassifier
from xgboost import XGClassifier

# 택1
model = DecisionTreeClassifier()
model = RandomForestClassifier()
model = XGClassifier()

model.fit(x_train, y_train)
y_train_predicted = model.predict(x_train)
y_test_predicted = model.predict(x_test)
 
서포트 벡터 분류, 배깅 분류, KNN 분류, 다층 퍼센트론 분류
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

# 택1
model = SVC()
model = BaggingClassifier()
model = KNeighborsClassifier()
model = MLPClassifier()

model.fit(x_train, y_train)
y_train_predicted = model.predict(x_train)
y_test_predicted = model.predict(x_test)
 
로지스틱 회귀 (범주형-이진 종속변수)
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(x_train, y_train)
y_test_predicted = model.predict(x_test)
 
예측값이 아닌, 예측에 대한 확률값 계산
y_test_proba = model.predict_proba(x_test)
 
평가지표 (범주형 종속변수)
# 평가지표 (ROC-AUC, 정확도, 정밀도, 재현율) -> 1에 가까울수록 좋음
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score

print(roc_auc_score(y_test, y_test_predicted))
# ...  사용법 동일
 
csv로 저장
# 값을 데이터프레임 타입으로 변경 후 행번호 제외하고 저장
pd.DataFrame(y_test_predicted).to_csv('경로/12345.csv', index = False)
 
--------------------------------
3유형 대비
https://in0-pro.tistory.com/90

# 3유형

소문제 6문제 (문제당 5점)

6회 : 카이제곱검정 / 다중선형회귀    
7회 : 로지스틱회귀 / 다중선형회귀     
8회 : 로지스틱회귀 / 다중선형회귀    

- F 검정통계량 : var1 / var2
- 합동 분산 추정량 : ((n1 - 1)*var1 + (n2 - 1)*var2) / (n1 + n2 - 2)
- pooled_var = 합동 분산 추정량
- T 검정통계량 : (mean1 - mean2) / np.sqrt(pooled_var*(1/n1 + 1/n2))
    - p값
        ```python
        from scipy import stats
        p_value = 2*(1-stats.t.cdf(abs(t_value), df=n1+n2-2))
        ```

```python


## 통계검정
from scipy.stats import ttest_1samp # 단일표본
from scipy.stats import ttest_ind   # 독립표본
from scipy.stats import ttest_rel   # 대응표본
s,p = ttest_1samp(df1,n)
s,p = ttest_ind(df1,df2)

from scipy.stats import shapiro     # 정규성검정
from scipy.stats import levene      # 등분산검정

pd.crosstab(df1,df2) # 범주형 변수 교차테이블
from scipy.stats import chi2_contingency # 카이제곱 독립성검정 - > 변수들이 독립한지
from scipy.stats import chisquare        # 카이제곱 적합도검정 - > 분포가 기대분포를 따르는지


## 그 외 통계검정을 물을 경우
import scipy.stats
dir(scipy.stats) # 관련 패키지 찾아서 데이터 입력

## 분산분석
from scipy.stats import f_oneway # anova f-검정
f_oneway(df1,df2,df3)

import statsmodels.api as sm # 이원 분산 분석
from statsmodels.formula.api import ols # 범주형 변수는 C()로 감싼다
model = ols('Y ~ C(X1) * X2', data=df).fit()
sm.stats.anova_lm(model)

## 다중선형회귀분석
import statsmodels.api as sm
X = sm.add_constant(X) # 상수항 추가
model = sm.OLS(Y, X).fit()
print(model.summary())

## 로지스틱 회귀
# 방법1
from statsmodels.formula.api import logit
import numpy as np
model = logit("종속변수 ~ 독립변수1 + 독립변수2", data=df).fit() # 로지스틱 회귀 분석 모델
print(model.summary())

model.params # 각 회귀 계수
model.pvalues # 각 회귀 계수에 대한 p-values

odds_ratios = np.exp(model.params) # 오즈비
print(odds_ratios)

# 방법2
import statsmodels.api as sm
X = sm.add_constant(X)
model = sm.Logit(y, X).fit() # 로지스틱 회귀 모델 적합
print(model.summary()) # 로지스틱 회귀 모델 적합


# 방법3
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X,Y)
lr.coef_



odds_ratios = np.exp(model.params) # 오즈비
print(odds_ratios)


-2 * model.llf # 잔차이탈도


```

예시문제 참고 : https://www.datamanim.com/dataset/97_scipy/scipy.html
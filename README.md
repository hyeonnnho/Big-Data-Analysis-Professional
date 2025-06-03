# Big-Data-Analysis-Professional
빅데이터 분석기사 실기 준비

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


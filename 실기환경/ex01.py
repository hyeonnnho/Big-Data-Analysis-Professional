# 출력을 원할 경우 print() 함수 활용
# 예시) print(df.head())

# getcwd(), chdir() 등 작업 폴더 설정 불필요
# 파일 경로 상 내부 드라이브 경로(C: 등) 접근 불가

import pandas as pd

df = pd.read_csv("data/employee_performance.csv")

df['고객만족도'] = df['고객만족도'].fillna(df['고객만족도'].mean())
df = df.dropna(subset='근속연수')

Ans1 = df['고객만족도'].quantile(0.75)
print(Ans1)

Ans2 = round(df.groupby('부서')['연봉'].mean().sort_values().values[-2],0)
print(Ans2)
# print(df.isnull().sum())


# 사용자 코딩

# 해당 화면에서는 제출하지 않으며, 문제 풀이 후 답안제출에서 결괏값 제출

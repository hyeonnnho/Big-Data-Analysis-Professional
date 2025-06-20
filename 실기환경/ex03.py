# 출력을 원할 경우 print() 함수 활용
# 예시) print(df.head())

# getcwd(), chdir() 등 작업 폴더 설정 불필요
# 파일 경로 상 내부 드라이브 경로(C: 등) 접근 불가

import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("data/bcc.csv")
df['log_Resistin'] = np.log(df['Resistin'])

A = df.loc[df['Classification'] == 1]['log_Resistin']
B = df.loc[df['Classification'] == 2]['log_Resistin']

var_A = A.var()
var_B = B.var()
dof_A = len(A) - 1
dof_B = len(B) - 1
n_A = len(A)
n_B = len(B)
mean_A = A.mean()
mean_B = B.mean()
# print(dof_A, dof_B)
# 51 63
Ans1 = var_B / var_A
print(Ans1.round(3))
# 1.3479569769029498

Ans2 = ((dof_A * var_A) + (dof_B * var_B))/(n_A + n_B - 2)
print(Ans2.round(3))
# 0.448994051143797

# 방법 1
t_stat = (mean_A - mean_B) / np.sqrt(Ans2*(1/n_A + 1/n_B))
Ans3 = 2*(1 - stats.t.cdf(abs(t_stat), df=n_A + n_B - 2))
print(Ans3.round(3))

# 방법 2
from scipy.stats import ttest_ind
s, p = ttest_ind(A, B, equal_var = True)
Ans3 = p.round(3)
print(Ans3)

# 사용자 코딩

# 해당 화면에서는 제출하지 않으며, 문제 풀이 후 답안제출에서 결괏값 제출

# 출력을 원하실 경우 print() 함수 활용
# 예시) print(df.head())

# getcwd(), chdir() 등 작업 폴더 설정 불필요
# 파일 경로 상 내부 드라이브 경로(C: 등) 접근 불가
import pandas as pd
train = pd.read_csv("data/customer_train.csv")
test = pd.read_csv("data/customer_test.csv")

# 결측치 , 이상치 처리
remove_col = ['회원ID', '환불금액']
train_pre = train.copy()
train_pre = train_pre.drop(columns = remove_col)
# a= train_pre['구매주기'].value_counts()
# print(a)
# print(train_pre.describe())
from sklearn.preprocessing import LabelEncoder

le_1 = LabelEncoder()
le_2 = LabelEncoder()
le_1.fit(train_pre['주구매상품'])
le_2.fit(train_pre['주구매지점'])
train_pre['주구매상품'] = le_1.transform(train_pre['주구매상품'])
train_pre['주구매지점'] = le_2.transform(train_pre['주구매지점'])

from sklearn.preprocessing import StandardScaler
# 1단계: 해당 컬럼들 float으로 변경 (경고 제거용)
cols_to_scale = ['최대구매액','방문일수','방문당구매건수','구매주기']
train_pre[cols_to_scale] = train_pre[cols_to_scale].astype('float64')
scaler_df = train_pre[cols_to_scale]
ss = StandardScaler()
ss.fit(scaler_df)

# 2단계: 스케일링 적용
train_pre.loc[:,['최대구매액','방문일수','방문당구매건수','구매주기']] = ss.transform(scaler_df).astype('float64')

# 분리
x = train_pre.drop(columns=['총구매액'])
y = train_pre['총구매액']
from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.3, random_state=42)

#모델링
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(random_state=1)
rf.fit(x_train, y_train)
rf_val_predict = rf.predict(x_val)

from sklearn.metrics import mean_squared_error
import numpy as np
# 평균제곱오차
rmse = np.sqrt(mean_squared_error(y_val, rf_val_predict))

print("RMSE:", rmse)

# test
test_pre = test.copy()
test_pre = test_pre.drop(columns=remove_col)

le_1.fit(test_pre['주구매상품'])
le_2.fit(test_pre['주구매지점'])
test_pre['주구매상품'] = le_1.transform(test_pre['주구매상품'])
test_pre['주구매지점'] = le_2.transform(test_pre['주구매지점'])

test_pre[cols_to_scale] = test_pre[cols_to_scale].astype('float64')
scaler_df_test = test_pre[cols_to_scale]

# 2단계: 스케일링 적용
test_pre.loc[:,['최대구매액','방문일수','방문당구매건수','구매주기']] = ss.transform(scaler_df_test).astype('float64')


rf_test_predict = rf.predict(test_pre)

result = pd.DataFrame(rf_test_predict, columns=['pred'])
result.to_csv('result.csv', index=False)
df4 = pd.read_csv('result.csv')
print(df4)



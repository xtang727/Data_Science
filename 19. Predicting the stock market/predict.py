import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('sphist.csv')
df['DateTime'] = pd.to_datetime(df.Date)
df_ordered = df.sort_values('DateTime', ascending=True)
df_ordered['index'] = range(0,df.shape[0],1)
df_ordered = df_ordered.set_index(['index'])


df_ordered['date_after_april1_2015'] = df_ordered.DateTime > datetime(year=2015, month=4, day=1)

data_mean_5day = df_ordered.Close.rolling(5).mean().shift(1)
data_mean_365day = df_ordered.Close.rolling(365).mean().shift(1)
data_mean_ratio = data_mean_5day/data_mean_365day

data_std_5day = df_ordered.Close.rolling(5).std().shift(1)
data_std_365day = df_ordered.Close.rolling(365).std().shift(1)
data_std_ratio = data_std_5day/data_std_365day

df_ordered['data_mean_5day'] = data_mean_5day
df_ordered['data_mean_365day'] = data_mean_365day
df_ordered['data_mean_ratio'] = data_mean_ratio
df_ordered['data_std_5day'] = data_std_5day
df_ordered['data_std_365day'] = data_std_365day
df_ordered['data_std_ratio'] = data_std_ratio


df_new = df_ordered[df_ordered["DateTime"] > datetime(year=1951, month=1, day=2)]
df_no_NA = df_new.dropna(axis=0)

df_train = df_no_NA[df_no_NA['DateTime'] < datetime(year=2013, month=1, day=1)]
df_test = df_no_NA[df_no_NA['DateTime'] >= datetime(year=2013, month=1, day=1)]


from sklearn.linear_model import LinearRegression
model = LinearRegression()
features = ['data_mean_5day', 'data_mean_365day', 'data_mean_ratio', 'data_std_5day', 'data_std_365day', 'data_std_ratio']
X = df_train[features]
X_test = df_test[features]
y = df_train.Close
y_test = df_test.Close

model.fit(X, y)
pred = model.predict(X_test)

MAE = sum(abs(pred - y_test))/len(pred)
print(MAE)
print(model.score(X, y))
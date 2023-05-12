# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BXmPQyHj1N8z5XX3twe-LpSW9HqDiGab
"""

import pickle
import pandas as pd
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("AMZN.csv")


df.set_index(df["Date"],inplace=True)
x = df.iloc[:, 1:5].values
y = df.iloc[:, 4].values



print(df)

print(x)

print(y)

x_train , x_test,y_train,y_test = train_test_split(x,y,test_size = 0.4,random_state = 42)

x_train.shape , y_train.shape,x_test.shape,y_test.shape

model = RandomForestRegressor(n_estimators=100, random_state=42)

model.fit(x_train,y_train)

predicted = model.predict(x_test)

import matplotlib.pyplot as plt
#plt.plot(x_test)
plt.plot(y_test,label = 'ydata')
plt.plot(predicted,label = 'predicted')
plt.legend()

#Evaluate the model MSE = (1/n) * ∑(y - y_pred)^2
#  R^2 = 1 - (SS_res / SS_tot)
mse = mean_squared_error(y_test, predicted)
r2 = r2_score(y_test, predicted)
errors = abs(predicted - y_test)
mape = 100 * (errors / y_test)
accuracy = 100 - np.mean(mape)
print("accuracy of the model is :",accuracy)
print("MEAN SQUARED ERROR : " , mse)
print("R-squared error" , r2)

predictions = pd.DataFrame({"Predictions": predicted,"Date":pd.date_range(start=df.index[-1], periods=len(predicted), freq="D")})
predictions.to_csv("Predicted-price-data.csv")
#colllects future days from predicted values
oneyear_df = pd.DataFrame(predictions[:252])
oneyear_df.to_csv("Amazon-one-year-predictions.csv")
onemonth_df = pd.DataFrame(predictions[:21])
onemonth_df.to_csv("one-month-predictions.csv")
fivedays_df = pd.DataFrame(predictions[:5])
fivedays_df.to_csv("five-days-predictions.csv")

predictions.index.values

oneyear_df_pred = pd.read_csv("Amazon-one-year-predictions.csv")
oneyear_df_pred.set_index("Date", inplace=True)
buy_price = min(oneyear_df_pred["Predictions"])
sell_price = max(oneyear_df_pred["Predictions"])
oneyear_buy = oneyear_df_pred.loc[oneyear_df_pred["Predictions"] == buy_price]
oneyear_sell = oneyear_df_pred.loc[oneyear_df_pred["Predictions"] == sell_price]
print("Buy price and date")
print(oneyear_buy)
print("Sell price and date")
print(oneyear_sell)
oneyear_df_pred.plot(y='Predictions',figsize=(10, 5), title="Forecast for the next 1 year", color="blue")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()

onemonth_df_pred = pd.read_csv("one-month-predictions.csv")
onemonth_df_pred.set_index("Date", inplace=True)
buy_price = min(onemonth_df_pred["Predictions"])
sell_price = max(onemonth_df_pred["Predictions"])
onemonth_buy = onemonth_df_pred.loc[onemonth_df_pred["Predictions"] == buy_price]
onemonth_sell = onemonth_df_pred.loc[onemonth_df_pred["Predictions"] == sell_price]
print("Buy price and date")
print(onemonth_buy)
print("Sell price and date")
print(onemonth_sell)
onemonth_df_pred.plot(y='Predictions',figsize=(10, 5), title="Forecast for the next 1 month", color="blue")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()

five_days_df_pred = pd.read_csv("five-days-predictions.csv")
five_days_df_pred.set_index("Date", inplace=True)
buy_price = min(five_days_df_pred["Predictions"])
sell_price = max(five_days_df_pred["Predictions"])
oneweek_buy = five_days_df_pred.loc[five_days_df_pred["Predictions"] == buy_price]
oneweek_sell = five_days_df_pred.loc[five_days_df_pred["Predictions"] == sell_price]
print("Buy price and date")
print(oneweek_buy)
print("Sell price and date")
print(oneweek_sell)
five_days_df_pred.plot(y='Predictions',figsize=(10, 5), title="Forecast for the next 1 week", color="blue")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()

pickle.dump(model,open("model.pkl","wb"))
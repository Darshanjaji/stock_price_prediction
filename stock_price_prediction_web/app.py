from flask import Flask,render_template,request
import pickle
import pandas as pd
import matplotlib.pyplot as plt
app = Flask(__name__)

RFmodel = pickle.load(open('model.pkl','rb'))
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prediction',methods=['post'])
def prediction():
    stock = request.form.get('stocks')
    print("stocks ", stock)
    if stock == 'NETFLIX':
        oneyear_df_pred = pd.read_csv("one-year-predictions.csv")
        oneyear_df_pred.set_index("Date", inplace=True)
        buy_price = min(oneyear_df_pred["Predictions"])
        sell_price = max(oneyear_df_pred["Predictions"])
        oneyear_buy = oneyear_df_pred.loc[oneyear_df_pred["Predictions"] == buy_price]
        oneyear_sell = oneyear_df_pred.loc[oneyear_df_pred["Predictions"] == sell_price]
        print("Buy price and date")
        print(oneyear_buy)
        print("Sell price and date")
        print(oneyear_sell)
        oneyear_df_pred.plot(y='Predictions', figsize=(10, 5), title="Forecast for the next 1 year", color="blue")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()
        return ["buy_price",list(oneyear_buy.index),list(oneyear_buy.iloc[:,1]),"sell_price",list(oneyear_sell.index),list(oneyear_sell.iloc[:,1])]


if __name__ == '__main__':
    app.run(debug=True)



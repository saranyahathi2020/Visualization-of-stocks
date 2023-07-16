from flask import Flask, render_template, request, send_file ,Response
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import plotly.graph_objs as go

import json

app = Flask(__name__)
@app.route('/')
def hello_world():
	return render_template("index.html")
# main driver function


@app.route('/login')
def login():
	return render_template("login.html")

@app.route('/welcome', methods=["GET", "POST"])
def validate():
	if request.method == 'POST' :
		un = request.form.get("user")
		if un== "hello" :
			return render_template("project.html")
		else :
			return "Fail"

@app.route('/get_details', methods=["GET", "POST"])
def produce():
  if request.method == 'POST':
    stock = request.form.get("cname")
    yf.pdr_override()

    # Create input field for our desired stock
    #stock=input("Enter a stock ticker symbol: ")

    # Retrieve stock data frame (df) from yfinance API at an interval of 1m
    df = yf.download(tickers=stock,period='1d',interval='1m')

    print(df)

    # Declare plotly figure (go)
    fig=go.Figure()

    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'], name = 'market data'))

    fig.update_layout(
        title= str(stock)+' Live Share Price:',
        yaxis_title='Stock Price (USD per Shares)')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return render_template('extra.html', graphJSON=fig.to_json())
    '''output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')'''
    #fig.show()	
    
  
   	
	   	
     
        

if __name__ == '__main__':

	app.run(debug=True)

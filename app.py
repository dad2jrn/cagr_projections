from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

def calculate_cagr(start_value, end_value, periods):
    return ((end_value / start_value) ** (1 / periods) - 1)

def fetch_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        ticker = request.form['ticker']
        period = int(request.form['period'])
        future_period = int(request.form['future_period'])
        initial_investment = float(request.form['initial_investment'])

        data = fetch_stock_data(ticker, f"{period}y")
        if not data.empty:
            start_price = data['Close'].iloc[0]
            end_price = data['Close'].iloc[-1]
            cagr = calculate_cagr(start_price, end_price, period)
            future_value = initial_investment * ((1 + cagr) ** future_period)
            result = {
                'ticker': ticker,
                'period': period,
                'cagr': cagr,
                'initial_investment': initial_investment,
                'future_period': future_period,
                'future_value': future_value
            }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

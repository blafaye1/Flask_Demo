# noinspection PyInterpreter
from flask import Flask, render_template, request, redirect
import pandas as pd
from bokeh.plotting import figure, output_file, show, save
import requests
import simplejson

app = Flask(__name__)

## Set variables for plotting function ##

app.api_key = 'X27HC5SP5PEJ5F9B'
app.base_url = "https://www.alphavantage.co"
app.months_dict = {'January': 1,
               'February': 2,
               'March': 3,
               'April': 4,
               'May': 5,
               'June': 6,
               'July': 7,
               'August': 8,
               'September': 9,
               'October': 10,
               'November': 11,
               'December': 12}

def get_daily_data(ticker_symbol):
    query_func = "TIME_SERIES_DAILY"
    req_param = "{0}/query?function={1}&symbol={2}&outputsize=full&apikey={3}".format(app.base_url, 
                                                                                      query_func, 
                                                                                      ticker_symbol, 
                                                                                      app.api_key)
    data = requests.get(req_param)
    return simplejson.loads(data.text)

def plot_closing_month():
    
    api_data = get_daily_data(stock_symbol)
    df_time_series = pd.DataFrame(api_data['Time Series (Daily)']).T
    closing_data = df_time_series.reset_index()[['index', '4. close']]

    closing_data['dates'] = pd.to_datetime(closing_data['index'])
    closing_data['stock_values_float'] = closing_data['4. close'].astype(float)
    closing_data = closing_data.drop(columns = ['index', '4. close'])

    selected_year_closing_data = closing_data[closing_data.dates.dt.year == int(year)]
    selected_month_closing_data = [selected_year_closing_data.dates.dt.month == app.months_dict[month]]
    ordered_closing_data = selected_month_closing_data.sort_values('dates')
    
    output_file("templates/plot_closing_{0}_{1}.html".format(month, year))
    p = figure()
    p.line(ordered_closing_data['dates'], ordered_closing_data['stock_values_float'])
    save(p)
    
    return

## Routed pages ##

@app.route('/')
def home_page():
  return render_template('home_page.html')

@app.route('/user_input')
def user_input():
    return render_template('userinfo_lulu.html')

@app.route('/plot')
def plotting_page():
    return render_template("plot_closing_{0}_{1}.html".format(month, year)) # TODO: month and year are not yet defined

# @app.route('/about')
# def about():
#   return render_template('about.html')

# @app.route('/hello_page_test')
# def hello_world():
#     return 'Hello world'

if __name__ == '__main__':
  app.run(port=33507)

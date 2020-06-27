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
app.params = {}
app.successful_query = {0: "error_invalid_symbol.html",
                        1: "error_invalid_date.html",
                        2: ""}

def get_daily_data(ticker_symbol):
    query_func = "TIME_SERIES_DAILY"
    req_param = "{0}/query?function={1}&symbol={2}&outputsize=full&apikey={3}".format(app.base_url, 
                                                                                      query_func, 
                                                                                      ticker_symbol, 
                                                                                      app.api_key)
    data = requests.get(req_param)
    return simplejson.loads(data.text)

def plot_closing_month():
    
    api_data = get_daily_data(app.params['symbol'])
    if 'Error Message' in api_data:
        return 0  
    df_time_series = pd.DataFrame(api_data['Time Series (Daily)']).T
    closing_data = df_time_series.reset_index()[['index', '4. close']]

    closing_data['dates'] = pd.to_datetime(closing_data['index'])
    closing_data['stock_values_float'] = closing_data['4. close'].astype(float)
    closing_data = closing_data.drop(columns = ['index', '4. close'])

    selected_year = closing_data[closing_data.dates.dt.year == int(app.params['year'])]
    selected_month = selected_year[selected_year.dates.dt.month == app.months_dict[app.params['month']]]
    ordered_closing_data = selected_month.sort_values('dates')
    
    output_file("templates/plot_closing_{0}_{1}.html".format(app.params['month'], app.params['year']))
    p = figure(title = "{0}, {1}".format(app.params['month'], app.params['year']),
               plot_width = 700,
               plot_height = 500,
               x_axis_type = "datetime")
    p.line(ordered_closing_data['dates'], 
           ordered_closing_data['stock_values_float'],
           line_color = "olivedrab",
           line_width = 2)
    p.circle(ordered_closing_data['dates'], 
             ordered_closing_data['stock_values_float'],
             color = "olivedrab",
             fill_color = "white",
             size = 6)
    save(p)
    
    return 2

def file_find_and_replace(fname, old_string, new_string):
    
    f = open(fname, "r")
    file_content = f.read()
    file_content = file_content.replace(old_string, new_string)
    f.close()
    f = open(fname, "w")
    f.write(file_content)
    f.close()
    
    return

## Routed pages ##

@app.route('/')
def home_page():
  return render_template("home_page.html")

@app.route('/plot', methods = ['POST'])
def plotting_page():
    app.params['symbol'] = request.form['input_symbol']
    app.params['month'] = request.form['input_month']
    app.params['year'] = request.form['input_year']
    app.successful_query[2] = "plot_closing_{0}_{1}.html".format(app.params['month'], app.params['year'])
    query_key = plot_closing_month()
    return render_template(app.successful_query[query_key]) 

# @app.route('/about')
# def about():
#   return render_template('about.html')

# @app.route('/user_input')
# def user_input():
#     return render_template('userinfo_lulu.html')

# @app.route('/hello_page_test', methods = ['POST'])
# def hello_world():
#     file_name = "templates/hello_world.html"
#     form_input = request.form['user_response']
#     file_find_and_replace(file_name, 'HelloWorld', form_input)
#     app.params['symbol'] = request.form['input_symbol']
#     app.params['month'] = request.form['input_month']
#     app.params['year'] = request.form['input_year']
#     return render_template("hello_world.html")

if __name__ == '__main__':
  app.run(port=33507)

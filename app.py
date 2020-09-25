import flask
import pickle
import pandas as pd
import numpy as np
import datetime
import math
import plotly.graph_objs as go
import mpld3


import time
import matplotlib.pyplot as plt

# Use pickle to load in the pre-trained model.
with open(f'model/bd_prediction_model.pkl', 'rb') as f:
    model = pickle.load(f)
app = flask.Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))
    if flask.request.method == 'POST':
        s_date = flask.request.form['s_date']
        s_month = flask.request.form['s_month']
        s_year = flask.request.form['s_year']

        e_date = flask.request.form['e_date']
        e_month = flask.request.form['e_month']
        e_year = flask.request.form['e_year']
        # Start - End
        from sklearn.preprocessing import PolynomialFeatures
        poly = PolynomialFeatures(degree = 4)
        start = datetime.datetime.strptime("08-09-20", "%m-%d-%y")
        end = datetime.datetime.strptime("12-07-20", "%m-%d-%y")
        date = start
        date_list = []
        final_prediction  = {}
        date_comparison = []
        while(date.timestamp()<=end.timestamp()):
            date += datetime.timedelta(days = 1)
            date_comparison.append(date)
            date_list.append(date.timestamp())

        #input_variables = pd.DataFrame([[s_date, s_month, s_year,e_date,e_month,e_year]],
#columns=['s_date', 's_month', 's_year','e_date','e_month','e_year'],
                                       #dtype=float)
        prediction = model.predict(poly.fit_transform(np.array(date_list).reshape(len(date_list), 1)))
        plt.plot(  predictions[10:], lw = 3, color = "red", alpha = 0.6)

        plt.text(86, 1600, "Infections", fontsize=14, color="red", alpha = 0.6)
        plt.yticks(fontsize = 14)
        ax.set_xticks([3, 27 , 58, 88 ])
        ax.set_xticklabels(['Sep', 'Oct', 'Nov', 'Dec'])
        plt.xticks(fontsize = 14)
        plt.title("Predictions: Number Of infected Cases In Bangladesh (Sep - Dec)", fontsize = 16)

        plt.tight_layout()
        plt.savefig('prediction.png')



        return flask.render_template('main.html',
                                     original_input={'s_date':s_date,
                                                     's_month':s_month,
                                                     's_year':s_year,
                                                     'e_date':e_date,
                                                     'e_month':e_month,
                                                     'e_year':e_year},
                                     result=prediction,
                                     )




if __name__ == '__main__':
    app.run()

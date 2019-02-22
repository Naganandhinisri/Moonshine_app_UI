import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

from modules.posting_data_to_database import post_data

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=mobile_app user=techops")


def __init__(self, employee_id):
    self.employee_id = employee_id


@app.route('/')
def homes():
    return render_template('welcome_page.html')


@app.route('/login_page')
def page2():
    return render_template('login_page.html')


@app.route('/list_of_cold_beverages')
def page3():
    return render_template('list_of_cold_beverages.html')


@app.route('/list_of_hot_beverages')
def page4():
    return render_template('list_of_hot_beverages.html')


@app.route('/post-data', methods=['POST'])
def post_user():
    post_data(connection, request.form)
    return render_template('displaying_data.html', shared=request.form)


if __name__ == '__main__':
    app.run()

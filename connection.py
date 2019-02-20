import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

from modules.posting_data_to_database import post_data

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=app user=techops")


def __init__(self, employee_id):
    self.employee_id = employee_id
@app.route('/')
def home():
    return render_template('welcome_page.html')


@app.route('/post-data', methods=['POST'])
def get_data():
    post_data(connection, request.form)
    return render_template('displaying_data.html', shared=request.form)


if __name__ == '__main__':
    app.run()

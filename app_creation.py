import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=staffs user=techops")


@app.route('/')
def homes():
    return render_template('login_page.html')


@app.route('/ordering_page')
def page2():
    return render_template('ordering_page.html')


def validate_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from staff_details where employee_id=%(id)s",
                   {'id': user_data['numeric']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('login_page.html')
    else:
        return render_template('ordering_page.html')


@app.route('/ordering_page', methods=['POST'])
def data():
    return validate_data(connection, request.form)


@app.route('/items', methods=['GET'])
def hello_():
    table = database_connect()
    return render_template("items_display.html", items=table)


@app.route('/availability', methods=['POST'])
def hello():
    table = database_connect()
    return render_template("items_display.html", items=table)


def database_connect():
    try:
        cursor = connection.cursor()
        cursor.execute("select  Available_juices from list_juices" )
        record = cursor.fetchall()

        return record
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


@app.route('/post-data', methods=['POST', 'GET'])
def get_data():
    post_data(connection, request.form)
    return render_template('employee_flow.html', shared=request.form)


def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute(" insert into cold_beverages(employee_id) values(" + user_data['numeric'] + ") ")
    connection.commit()
    cursor.close()


@app.route('/employee_flow', methods=['POST'])
def hello():
    row = table_connect()
    return render_template("employee_flow.html", items=row)


def table_connect():
    try:
        cursor = connection.cursor()
        cursor.execute("select  employee_id from cold_beverages" )
        records = cursor.fetchall()

        return records
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)



if __name__ == '__main__':
    app.run()

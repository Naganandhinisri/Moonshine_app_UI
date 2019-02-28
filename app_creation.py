import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=staffs user=techops")


@app.route('/')
def homes():
    return render_template('login_page.html')


@app.route('/ordering_page', methods=['POST'])
def get_data():
    post_data(connection, request.form)
    return render_template('ordering_page.html', shared=request.form)


def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into guest(name) values(%s);""", (user_data['name'],))
    connection.commit()
    cursor.close()


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


@app.route('/availability', methods=['POST'])
def hello():
    table = database_connect()
    items = []
    for row in table:
        items.append(row[0])

    return render_template("items_display.html", items=items)


def database_connect():
    try:
        cursor = connection.cursor()
        cursor.execute("select Available_juices from list_juices")
        record = cursor.fetchall()
        return record
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


@app.route('/available_hot_beverages', methods=['POST'])
def hot_drinks():
    table = connect_database()
    items = []
    for row in table:
        items.append(row[0])

    return render_template("hot_beverages.html", items=items)


def connect_database():
    try:
        cursor = connection.cursor()
        cursor.execute("select Available_hot_drinks from hot_drinks ")
        record = cursor.fetchall()
        return record
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


@app.route('/selected_beverages', methods=['POST'])
def beverages():
    return render_template('flow.html', shared=request.form)


def selected_beverages(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from cold_beverages where employee_id=%(id)s",
                   {'id': user_data['numeric']})
    connection.commit()
    cursor.close()


@app.route('/vendor_page', methods=['post'])
def show():
    return render_template('vendor_page.html', shared=request.form)


@app.route('/vendor_juice_world', methods=['post'])
def vendor_details():
    return render_template('vendor_juice_world.html', shared=request.form)


@app.route('/report_generation', methods=['POST'])
def check_info_vendor():
    return validate_info_vendor(connection, request.form)


def validate_info_vendor(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select vendor_id,password from vendor_details where vendor_id=%(id)s AND password=%(password)s",
                   {'id': user_data['id'], 'password': user_data['psw']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('vendor_juice_world.html')
    else:
        return render_template('report_generation_page.html')


if __name__ == '__main__':
    app.run()

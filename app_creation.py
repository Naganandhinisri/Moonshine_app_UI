import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=thoughtworks_cafeteria user=techops")


@app.route('/')
def homes():
    return render_template('login_page.html')


@app.route('/ordering_page', methods=['POST'])
def get_data():
    post_data(connection, request.form)
    return render_template('ordering_page.html')


def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into guest(name) values(%s);""", (user_data['name'],))
    connection.commit()
    cursor.close()


@app.route('/ordering_page', methods=['POST'])
def data():
    return validate_data(connection, request.form)


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


@app.route('/availability', methods=['POST'])
def hello():
    table = database_connect()
    items = []
    for row in table:
        items.append({"id": row[0], "name": row[1]})
    return render_template("display_list_of_cold_beverages.html", items=items)


def database_connect():
        cursor = connection.cursor()
        cursor.execute("select id, juice_name from cold_drinks_list ")
        record = cursor.fetchall()
        return record


@app.route('/selected_cold_beverages', methods=['POST'])
def cold_beverages():
    table = database_cold_beverages(connection, request.form)
    items = []
    for row in table:
        items.append(row[0])
    database_cold_beverages(connection, request.form)
    return render_template("display_selected_cold_beverages.html", items=items)


def database_cold_beverages(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    query_to_update = "update  cold_drinks_list set selected_juices = 'no'"
    query = "update cold_drinks_list set selected_juices = 'yes' where id IN %s"
    display_selected_juices = "select juice_name from cold_drinks_list where selected_juices='yes'"
    cursor.execute(query_to_update)
    cursor.execute(query, (array,))
    connection.commit()
    cursor.execute(display_selected_juices)
    record = cursor.fetchall()
    return record


@app.route('/selected_juices', methods=['POST'])
def count_quantity():
    return database_connection_quantity(connection, request.form)


def database_connection_quantity(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    query_to_update = "update  cold_drinks_list set quantity = '0'"
    sql = "update cold_drinks_list set quantity = '1' where selected_juices='yes'"
    cursor.execute(query_to_update)
    cursor.execute(sql, (array,))
    connection.commit()
    cursor.close()


@app.route('/available_hot_beverages', methods=['POST'])
def display_hot_drinks():
    table = database_connect_hot_beverages()
    items = []
    for row in table:
        items.append({"id": row[0], "name": row[1]})
    return render_template("display_list_of_hot_beverages.html", items=items)


def database_connect_hot_beverages():
        cursor = connection.cursor()
        cursor.execute("select id, hot_drinks_name from hot_drinks_list ")
        record = cursor.fetchall()
        return record


@app.route('/selected_hot_beverages', methods=['POST'])
def hot_beverages():
    table = database_hot_beverages(connection, request.form)
    items = []
    for row in table:
        items.append(row[0])
    database_cold_beverages(connection, request.form)
    return render_template("display_selected_hot_beverages.html", items=items)


def database_hot_beverages(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    query_to_update = "update  hot_drinks_list set selected_hot_drinks = 'no'"
    query = "update hot_drinks_list set selected_hot_drinks = 'yes' where id IN %s"
    display_selected_hot_drinks = "select hot_drinks_name from hot_drinks_list where selected_hot_drinks='yes'"
    cursor.execute(query_to_update)
    cursor.execute(query, (array,))
    connection.commit()
    cursor.execute(display_selected_hot_drinks)
    record = cursor.fetchall()
    return record


@app.route('/selected_hot_drinks', methods=['POST'])
def count_quantities():
    return database_connection_quantities(connection, request.form)


def database_connection_quantities(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    query_to_update = "update  hot_drinks_list set quantity = '0'"
    sql = "update hot_drinks_list set quantity = '1' where selected_hot_drinks='yes'"
    cursor.execute(query_to_update)
    cursor.execute(sql, (array,))
    connection.commit()
    cursor.close()


@app.route('/vendor_page', methods=['post'])
def show_vendor_page():
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


@app.route('/vendor_cafe', methods=['post'])
def vendor_details_cafe():
    return render_template('vendor_cafe.html', shared=request.form)


@app.route('/generate_report', methods=['POST'])
def check_info_vendor_cafe():
    return validate_info_vendor_cafe(connection, request.form)


def validate_info_vendor_cafe(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select vendor_id,password from vendor_cafe_details where vendor_id=%(id)s AND password=%(password)s",
                   {'id': user_data['id'], 'password': user_data['psw']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('vendor_cafe.html')
    else:
        return render_template('generate_report.html')


if __name__ == '__main__':
    app.run()

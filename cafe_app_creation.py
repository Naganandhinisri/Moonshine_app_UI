import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=thoughtworks_cafeteria user=techops")


@app.route('/')
def login_page():
    return render_template('login_page.html')


@app.route('/ordering_page', methods=['POST'])
def data():
    return validate_data(connection, request.form)


def validate_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from employee_details where employee_id = %(id)s",
                   {'id': user_data['id_value']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('login_page.html')
    else:
        return render_template('ordering_page.html', itemss=user_data['id_value'])


@app.route('/availability', methods=['POST'])
def hello():
    return cold_item(connection, request.form)


def cold_item(connection, user_data):
    connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    rows = database_connect()
    items = []
    for row in rows:
        items.append({"id": row[0], "name": row[1]})
    return render_template("display_list_of_cold_beverages.html", items=items, itemss=array_value)



def database_connect():
    cursor = connection.cursor()
    cursor.execute("select id, juice_name from cold_drinks_menu ")
    record = cursor.fetchall()
    return record


@app.route('/add_to_cart', methods=['POST'])
def cold_beverages():
    database_cold_beverages(connection, request.form)
    return render_template('login_page.html')


def database_cold_beverages(connection, user_data):
    employee_details = list(user_data.values())
    employee_index = employee_details[0]
    employee_details.remove(employee_details[0])
    item_key = list(user_data.keys())
    item_key.remove(item_key[0])
    for id in list(item_key):
        quantity = user_data[id]
        if int(quantity) != 0:
            cursor = connection.cursor()
            update_details = "insert into cold_beverages_report_generation(id,count,employees_id) select id,{},{} from cold_drinks_menu where id = {}".format(
                quantity, employee_index, id)
            cursor.execute(update_details)
            connection.commit()
            cursor.close()
        else:
            continue


@app.route('/available_hot_beverages', methods=['POST'])
def show_hot_drinks():
    table = hot_drinks_menu()
    items = []
    for row in table:
        items.append({"id": row[0], "name": row[1]})
    return render_template("display_list_of_hot_beverages.html", items=items)


def hot_drinks_menu():
    cursor = connection.cursor()
    cursor.execute("select id, hot_drinks_name from hot_drinks_menu ")
    record = cursor.fetchall()
    return record


@app.route('/quantity_hot_drinks', methods=['POST'])
def hot_beverages():
    table = database_hot_beverages(connection, request.form)
    return render_template('login_page.html', items=table)


def database_hot_beverages(connection, update_data):
    item = update_data.to_dict()
    a = []
    b = []
    i = 0
    j = 1
    index = 0
    if i != len(item):
            a.append(list(item.keys())[i])
            b.append(list(item.values())[j])
            cursor = connection.cursor()
            update_details = "insert into hot_beverages_report_generation(id,count) select id,{} from hot_drinks_menu where id='{}'".format(
                b[index], a[index])
            cursor.execute(update_details)
            connection.commit()
            cursor.close()
            i += 1
            j += 1
            index += 1
    return update_details


@app.route('/vendor_page', methods=['post'])
def show_vendor_page():
    return render_template('vendor_page.html', shared=request.form)


@app.route('/vendor_juice_world', methods=['post'])
def vendor_details():
    return render_template('vendor_juice_world.html', shared=request.form)


@app.route('/report_generation', methods=['POST'])
def check_info_vendor():
    return validate_vendor_juice_shop_details(connection, request.form)


def validate_vendor_juice_shop_details(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select vendor_id,password from vendor_juice_world_details where vendor_id=%(id)s AND password=%(password)s",
                   {'id': user_data['id'], 'password': user_data['psw']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('vendor_juice_world.html')
    else:
        return render_template('report_generation_cold_drinks.html')


@app.route('/vendor_cafe', methods=['post'])
def vendor_details_cafe():
    return render_template('vendor_madras_coffee_house.html', shared=request.form)


@app.route('/generate_report', methods=['POST'])
def check_info_vendor_cafe():
    return validate_vendor_coffee_shop_details(connection, request.form)


def validate_vendor_coffee_shop_details(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select vendor_id,password from vendor_coffee_house_details where vendor_id=%(id)s AND password=%(password)s",
                   {'id': user_data['id'], 'password': user_data['psw']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('vendor_madras_coffee_house.html')
    else:
        return render_template('report_generation_hot_drinks.html')


if __name__ == '__main__':
    app.run()
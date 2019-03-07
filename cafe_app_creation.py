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
    cursor.execute("select employee_id from staff_details where employee_id = %(id)s",
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


@app.route('/add_to_cart', methods=['POST'])
def cold_beverages():
    table = database_cold_beverages(connection, request.form)
    items = []
    for row in table:
        items.append(row[0])
    return render_template('display_selected_cold_beverages.html', items=items)


def database_cold_beverages(connection, user_data):
    cursor = connection.cursor()
    # array = tuple(user_data.keys())
    arrays = tuple(user_data.keys())
    # query_to_update = "insert into cold_beverages(id)   (select id from cold_drinks_list WHERE id IN %s)"
    display_selected_juices = "select juice_name from cold_drinks_list where id IN %s"
    # cursor.execute(query_to_update, (array,))
    connection.commit()
    cursor.execute(display_selected_juices, (arrays,))
    record = cursor.fetchall()
    return record


@app.route('/selected_juices', methods=['POST'])
def count_quantity():
    database_connect_quantity(connection, request.form)
    return render_template('login_page.html')



def database_connect_quantity(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.values())
    query_to_update = "update cold_beverages set quantity = %s"\
                      " where id IN (SELECT id from cold_drinks_list where id IN %s)"
    cursor.execute(query_to_update, (array,))
    connection.commit()
    cursor.close()





if __name__ == '__main__':
    app.run()
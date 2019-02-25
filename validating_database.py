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


def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute(" insert into staff_details(employee_id) values("+user_data['numeric']+") ")
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


@app.route('/list_of_cold_beverages')
def page3():
    return render_template('list_of_cold_beverages.html')


@app.route('/list_of_hot_beverages')
def page4():
    return render_template('list_of_hot_beverages.html')




if __name__ == '__main__':
     app.run()






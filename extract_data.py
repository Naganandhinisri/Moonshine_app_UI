import psycopg2
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    table = database_connect()
    return render_template("items_display.html", items=table)


def database_connect():
    try:
        print("try is running")
        connection = psycopg2.connect(user="techops", host="127.0.0.1", port="5432",
                                      database="staffs")
        cursor = connection.cursor()
        cursor.execute("select  juice_id,Available_juices from list_juices")
        record = cursor.fetchall()

        return record
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    app.run()
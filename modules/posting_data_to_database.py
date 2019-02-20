def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into data(employee_id) values(%s);""",
                   (user_data['employee_id']))
    connection.commit()
    cursor.close()
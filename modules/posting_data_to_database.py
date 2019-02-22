def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute(" insert into number(employee_id) values("+user_data['numeric']+") ")
    connection.commit()
    cursor.close()
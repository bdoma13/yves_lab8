import mysql.connector 
 
db_conn = mysql.connector.connect(host="acit3855-hosung.westus3.cloudapp.azure.com", user="user", 
password="password", database="events") 
 
db_cursor = db_conn.cursor() 
 
db_cursor.execute(''' 
                  DROP TABLE ticket_info, review_info 
                  ''') 
 
db_conn.commit() 
db_conn.close() 
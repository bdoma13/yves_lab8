import mysql.connector 
 
db_conn = mysql.connector.connect(host="acit3855-hosung.westus3.cloudapp.azure.com", user="user", 
password="password", database="events") 

db_cursor = db_conn.cursor() 
db_cursor.execute('CREATE DATABASE IF NOT EXISTS events') 
db_cursor.execute('''
          CREATE TABLE  IF NOT EXISTS ticket_info
          (id INT AUTO_INCREMENT NOT NULL, 
           ticket_num VARCHAR(250) NOT NULL,
           movie_title VARCHAR(250) NOT NULL,
           runtime INTEGER NOT NULL,
           price INTEGER NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT ticket_pk PRIMARY KEY(id))
          ''') 
 
db_cursor.execute('''
          CREATE TABLE IF NOT EXISTS review_info
          (id INT AUTO_INCREMENT NOT NULL, 
           review_id VARCHAR(250) NOT NULL,
           movie_title VARCHAR(250) NOT NULL,
           gender VARCHAR(250) NOT NULL,
           age INTEGER NOT NULL,
           rating INTEGER NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT review_pk PRIMARY KEY(id))
          ''')
 
db_conn.commit() 
db_conn.close() 


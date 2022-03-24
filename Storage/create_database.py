import sqlite3

conn = sqlite3.connect('movie.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE review_info
          (id INTEGER PRIMARY KEY ASC, 
           review_id VARCHAR(250) NOT NULL,
           movie_title VARCHAR(250) NOT NULL,
           gender VARCHAR(250) NOT NULL,
           age INTEGER NOT NULL,
           rating INTEGER NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE ticket_info
          (id INTEGER PRIMARY KEY ASC, 
           ticket_num VARCHAR(250) NOT NULL,
           movie_title VARCHAR(250) NOT NULL,
           runtime INTEGER NOT NULL,
           price INTEGER NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()

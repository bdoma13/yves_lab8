import sqlite3 
 
conn = sqlite3.connect('stats.sqlite') 
 
c = conn.cursor() 
c.execute(''' 
          CREATE TABLE stats 
          (id INTEGER PRIMARY KEY ASC,  
           num_of_review INTEGER NOT NULL, 
           avg_age FLOAT NOT NULL, 
           avg_rating FLOAT NOT NULL, 
           total_sale FLOAT NOT NULL, 
           num_of_ticket INTEGER NOT NULL, 
           last_updated VARCHAR(100) NOT NULL) 
          ''') 
 
conn.commit() 
conn.close()    
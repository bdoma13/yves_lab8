import connexion
from connexion import NoContent
import json
from datetime import datetime
import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from ticket_info import ticketInfo
from review_info import reviewInfo
from uuid import uuid1
import logging.config
import yaml
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread 

yaml_file = "./openapi.yml"

with open('./app_conf.yml', 'r') as f:
    app_config=yaml.safe_load(f.read())
    user=app_config['datastore']['user']
    password=app_config['datastore']['password']
    hostname=app_config['datastore']['hostname']
    port=app_config['datastore']['port']
    db=app_config['datastore']['db']

with open('./log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)
logger.info(f"Connected to DB. Hostname:{app_config['datastore']['hostname']}, Port:{app_config['datastore']['port']}")

# def ticket_info(body):
#     session = DB_SESSION()

#     tickinf = ticketInfo(body['ticket_num'],
#                        body['movie_title'],
#                        body['runtime'],
#                        body['price'],
#                        body['trace_id'])

#     session.add(tickinf)
#     session.commit()
#     session.close()
#     logger.debug(f"Stored event status request with a trace id of {body['trace_id']}")
#     return NoContent, 201

def search_ticket(timestamp): 
 
    session = DB_SESSION() 

    timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
   
 
    readings = session.query(ticketInfo).filter(ticketInfo.date_created >=   
                                                  timestamp_datetime) 
 
    results_list = [] 
 
    for reading in readings: 
        results_list.append(reading.to_dict()) 
 
    session.close() 
     
    logger.info("Query for ticket readings after %s returns %d results" %  
                (timestamp, len(results_list))) 
 
    return results_list, 200

# def review_info(body):
#     """ Adds a new review to the system """
#     session = DB_SESSION()

#     review = reviewInfo(body['review_id'],
#                    body['movie_title'],
#                    body['gender'],
#                    body['age'],
#                    body['rating'],
#                    body['trace_id'])

#     session.add(review)
    
#     session.commit()
#     session.close()
#     logger.debug(f"Stored event status request with a trace id of {body['trace_id']}")
    
#     return NoContent, 201

def search_review(timestamp): 
 
    session = DB_SESSION() 
 
    timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") 
   
 
    readings = session.query(reviewInfo).filter(reviewInfo.date_created >=   
                                                  timestamp_datetime) 
 
    results_list = [] 
 
    for reading in readings: 
        results_list.append(reading.to_dict()) 
 
    session.close() 
     
    logger.info("Query for review readings after %s returns %d results" %  
                (timestamp, len(results_list))) 
 
    return results_list, 200

def process_messages(): 
    """ Process event messages """ 
    hostname = "%s:%d" % (app_config["events"]["hostname"],   
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
     
    # Create a consume on a consumer group, that only reads new messages  
    # (uncommitted messages) when the service re-starts (i.e., it doesn't  
    # read all the old messages from the history in the message queue). 
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', 
                                         reset_offset_on_start=False, 
                                         auto_offset_reset=OffsetType.LATEST) 
 
    # This is blocking - it will wait for a new message 
    for msg in consumer: 
        msg_str = msg.value.decode('utf-8') 
        msg = json.loads(msg_str) 
        logger.info("Message: %s" % msg) 
 
        payload = msg["payload"] 
                 
        if msg["type"] == "ticket_info": # Change this to your event type 
                session = DB_SESSION()
                
                bp = ticketInfo(payload['ticket_num'],
                              payload['movie_title'],
                              payload['runtime'],
                              payload['price'],
                              payload['trace_id'])

                session.add(bp)

                session.commit()
                session.close()

                logger.debug(f"Received event ticket_info request with a trace id of {payload['trace_id']}")

            
        elif msg["type"] == "review_info": # Change this to your event type 
                session = DB_SESSION()

                bp = reviewInfo(payload['review_id'],
                               payload['movie_title'],
                               payload['gender'],
                               payload['age'],
                               payload['rating'],
                               payload['trace_id'])

                session.add(bp)

                session.commit()
                session.close()

                logger.debug(f"Received event review_info request with a trace id of {payload['trace_id']}")

 
        # Commit the new message as being read 
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages) 
    t1.setDaemon(True) 
    t1.start()
    app.run(port=8090)
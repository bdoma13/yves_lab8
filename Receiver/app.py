import connexion
from connexion import NoContent
import json
from datetime import datetime
import os
import requests
import yaml
import logging.config
from uuid import uuid1
from pykafka import KafkaClient

with open('./app_conf.yml', 'r') as f:
    app_config=yaml.safe_load(f.read())
    ticket_inf=app_config['event1']['url']
    review=app_config['event2']['url']

with open('./log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')
    
def ticket_info(body):
    """ Adds a new ticket information to the system """
    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}") 
    topic = client.topics[str.encode(app_config['events']['topic'])] 
    producer = topic.get_sync_producer() 
    trace_id = str(uuid1())
    body['trace_id'] = trace_id

    msg = { "type": "ticket_info",  
            "datetime" :    
            datetime.now().strftime( 
                "%Y-%m-%dT%H:%M:%S"),  
            "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))
    
    logger.info(f"ticketinfo added with {trace_id}")
    
    return NoContent , 201


def review_info(body):
    """ Adds a new review to the system """
    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}") 
    topic = client.topics[str.encode(app_config['events']['topic'])] 
    producer = topic.get_sync_producer() 
    trace_id = str(uuid1())
    body['trace_id'] = trace_id

    msg = { "type": "review_info",  
            "datetime" :    
            datetime.now().strftime( 
                "%Y-%m-%dT%H:%M:%S"),  
            "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))
    
    logger.info(f"review info added with {trace_id}")

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    app.run(port=8080, debug=True)

from logging.handlers import BufferingHandler
import connexion
import requests
import swagger_ui_bundle
import yaml
import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
from base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stats import Stats
from datetime import datetime
from uuid import uuid1


yaml_file = "./openapi.yml"

with open('app_conf.yml', 'r') as f:
    app_config=yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"]) 
Base.metadata.bind = DB_ENGINE 
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def get_stats():
    logger.info("Request has started.")

    session = DB_SESSION() 

    try:
        readings = session.query(Stats).order_by(Stats.last_updated.desc()).first()

        results = readings.to_dict()
    except:
        logger.error("Statistics do not exist.")

    session.close()

    logger.debug(f"Python Dictionary Contents: {results}.")
    logger.info(f"Request has completed.")

    return results, 200

def populate_stats(): 
    """ Periodically update stats """ 
    logger.info(f"Periodic Request Process Has Started")

    session = DB_SESSION() 
    # print(readings.last_updated)
    try:
        readings = session.query(Stats).order_by(Stats.last_updated.desc()).first()

        # results = [] 

        # for reading in readings: 
        #     results.append(reading.to_dict())
        results = readings.to_dict()["last_updated"].replace(microsecond=0)
    except:
        results = '0001-01-01 01:01:01'
    
    # print(results)
    review_res = requests.get("http://localhost:8090/movie/review",params={'timestamp': results}, headers = {"content-type": "application/json"})
    ticket_res = requests.get("http://localhost:8090/movie/ticket",params={'timestamp': results}, headers = {"content-type": "application/json"})
    review = review_res.json()
    ticket = ticket_res.json()
    if len(review) != 0 or len(ticket) != 0:
        responses = len(review) + len(ticket)

        if review_res.ok and ticket_res.ok:
            logger.info(f"Total responses received: {responses}")
        else:
            logger.error("GET request failed.")

        trace_id = str(uuid1())

        avg_age_view = sum([x['age'] for x in review])/len(review)
        avg_rating_view = sum([x['rating'] for x in review])/len(review)
        total_sale_ticket = sum([x['price'] for x in ticket])/len(ticket)

        logger.debug(f"Total number of reviews: {len(review)}. TraceID: {trace_id}")
        logger.debug(f"Average age of reviewers: {avg_age_view}. TraceID: {trace_id}")
        logger.debug(f"Average rating of reviews: {avg_rating_view}. TraceID: {trace_id}")
        logger.debug(f"Total sales: {total_sale_ticket}. TraceID: {trace_id}")
        logger.debug(f"Total number of ticket sold: {len(ticket)}. TraceID: {trace_id}")

        stats = Stats(len(review), 
                avg_age_view, 
                avg_rating_view, 
                total_sale_ticket, 
                len(ticket), 
                datetime.now())

        session.add(stats) 
        logger.debug(f"New Stat entry. TraceID: {trace_id}")
        session.commit()

    session.close()

    logger.info(f"Periodic Request Process has ended.")


def init_scheduler():
    sched = BackgroundScheduler(daemon=True) 
    sched.add_job(populate_stats,'interval',seconds=app_config['scheduler']['period_sec']) 
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(yaml_file, strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler() 
    app.run(port=8100, use_reloader=False)
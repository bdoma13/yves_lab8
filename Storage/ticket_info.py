from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class ticketInfo(Base):
    """ Ticket Info """

    __tablename__ = "ticket_info"

    id = Column(Integer, primary_key=True)
    ticket_num = Column(String(250), nullable=False)
    movie_title = Column(String(250), nullable=False)
    runtime = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)


    def __init__(self, ticket_num, movie_title, runtime, price,trace_id):
        """ ticket info """
        self.ticket_num = ticket_num
        self.movie_title = movie_title
        self.runtime = runtime
        self.price = price
        self.date_created = datetime.datetime.now().replace(microsecond=0)
        self.trace_id = trace_id
    
    def to_dict(self):
        """ Dictionary  of ticket information """
        dict = {}
        dict['id'] = self.id
        dict['ticket_num'] = self.ticket_num
        dict['movie_title'] = self.movie_title
        dict['runtime'] = self.runtime
        dict['price'] = self.price
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict

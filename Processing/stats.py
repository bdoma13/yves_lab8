from sqlalchemy import Column, Float, Integer, String, DateTime
from base import Base 
class Stats(Base): 
    """ Processing Statistics """ 
 
    __tablename__ = "stats" 
 
    id = Column(Integer, primary_key=True) 
    num_of_review = Column(Integer, nullable=False) 
    avg_age = Column(Float, nullable=False) 
    avg_rating = Column(Float, nullable=False) 
    total_sale = Column(Float, nullable=False) 
    num_of_ticket = Column(Integer, nullable=False) 
    last_updated = Column(DateTime, nullable=False) 
 
    def __init__(self, num_of_review, avg_age, avg_rating, total_sale, num_of_ticket, last_updated): 
        """ Initializes a processing statistics object """ 
        self.num_of_review = num_of_review 
        self.avg_age = avg_age 
        self.avg_rating = avg_rating 
        self.total_sale = total_sale 
        self.num_of_ticket = num_of_ticket 
        self.last_updated = last_updated 
 
    def to_dict(self): 
        """ Dictionary Representation of a statistics """ 
        dict = {} 
        dict['num_of_review'] = self.num_of_review 
        dict['avg_age'] = self.avg_age 
        dict['avg_rating'] = self.avg_rating 
        dict['total_sale'] = self.total_sale 
        dict['num_of_ticket'] = self.num_of_ticket 
        dict['last_updated'] = self.last_updated.strftime("%Y-%m-%d %H:%M:%S") 
 
        return dict
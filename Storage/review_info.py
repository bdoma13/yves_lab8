from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class reviewInfo(Base):
    """ Review Information """

    __tablename__ = "review_info"

    id = Column(Integer, primary_key=True)
    review_id = Column(String(250), nullable=False)
    movie_title = Column(String(250), nullable=False)
    gender = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)
    
    def __init__(self, review_id, movie_title, gender, age, rating, trace_id):
        self.review_id = review_id
        self.movie_title = movie_title
        self.gender = gender
        self.age = age
        self.rating = rating
        self.date_created = datetime.datetime.now().replace(microsecond=0)
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a review information """
        dict = {}
        dict['id'] = self.id
        dict['review_id'] = self.review_id
        dict['movie_title'] = self.movie_title
        dict['gender'] = self.gender
        dict['age'] = self.age
        dict['rating'] = self.rating
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from common import db_cred
import random

Base = declarative_base()

class ImageRecord(Base):
    __tablename__ = 'image_records'

    id = Column(Integer, primary_key=True)
    image_url       = Column(String)
    title           = Column(String)
    photographer    = Column(String)
    order_no        = Column(String, nullable=False, unique=True)
    filing_info     = Column(String)
    date            = Column(String)
    description     = Column(String)
    notes           = Column(String)
    summary         = Column(String)
    subjects        = Column(String)

    def __repr__(self):
        return "<User(id='%d', title='%s', order_no'%s', photographer='%s', image_url='%s', filing_info='%s', date='%s', description='%s', notes='%s', summary='%s', subjects='%s')>" % (self.id,
           self.title, self.order_no, self.photographer, self.image_url, self.filing_info, self.date, self.description, self.notes, self.summary, self.subjects)

class DB(object):
    def __init__(self):
        self.engine = create_engine(db_cred, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def _create_session(self):
        return self.Session()

    def _commit_session(self, session):
        session.commit()
        session.close()

    def _create_record(self, session, params):
        record = ImageRecord(**params)
        session.add(record)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def create_record_batch(self, records):
        session = self._create_session()

        # poll existing order_nos
        results = session.query(ImageRecord.order_no).all()
        order_nos = map(lambda t: t[0], results)

        # save only records with unique order_nos
        for record in records:
            order_no = record['order_no'].encode('utf-8')
            if order_no not in order_nos:
                self._create_record(session, record)
                order_nos.append(order_no)
                print "Adding record: {0}".format(record)
            else:
                print "Order #{0} already found. Skipping.".format(record['order_no'])

        self._commit_session(session)

    def retrieve_record(self):
        session = self._create_session()

        # get random record
        record = None
        records = session.query(ImageRecord)

        rand_index = random.randrange(0, session.query(ImageRecord).count())
        record = records[rand_index]

        session.close()

        return record

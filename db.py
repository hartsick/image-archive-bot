from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

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
    def __init__(self, db_string):
        self.engine = create_engine(db_string, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()

    def commit_session(self, session):
        session.commit()
        session.close()

    def create_record(self, session, params):
        record = ImageRecord(**params)
        session.add(record)

    def create_record_batch(self, records):
        session = self.create_session()

        # poll existing order_nos
        order_nos = session.query(ImageRecord.order_no).all()
        print(order_nos)

        # save only records with unique order_nos
        for record in records:
            if record['order_no'] not in order_nos:
                self.create_record(session, record)
                order_nos.append(record['order_no'])
            else:
                print "Order #{0} already found. Skipping.".format(record['order_no'])

        self.commit_session(session)

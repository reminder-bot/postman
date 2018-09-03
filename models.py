from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, Unicode, String, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser

config = configparser.SafeConfigParser()
config.read('config.ini')
user = config.get('MYSQL', 'USER')
try:
    passwd = config.get('MYSQL', 'PASSWD')
except:
    passwd = None
host = config.get('MYSQL', 'HOST')
database = config.get('MYSQL', 'DATABASE')

Base = declarative_base()

class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True, unique=True)
    message = Column(Unicode(2000))
    channel = Column(BigInteger)
    guild = Column(BigInteger)
    time = Column(BigInteger)
    interval = Column(Integer)

    webhook = Column(String(200))
    avatar = Column(Text)

    mysql_charset = 'utf8mb4'

    def __repr__(self):
        return '<Reminder "{}" <#{}> {}s>'.format(self.message, self.channel, self.time)



class Deletes(Base):
    __tablename__ = 'deletes'

    map_id = Column(Integer, primary_key=True)
    message = Column(BigInteger)
    channel = Column(BigInteger)
    time = Column(BigInteger)


if passwd:
    engine = create_engine('mysql+pymysql://{user}:{passwd}@{host}/{db}?charset=utf8mb4'.format(user=user, passwd=passwd, host=host, db=database))
else:
    engine = create_engine('mysql+pymysql://{user}@{host}/{db}?charset=utf8mb4'.format(user=user, host=host, db=database))
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

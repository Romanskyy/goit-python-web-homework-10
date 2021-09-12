
from datetime import datetime, date, timedelta
#from faker import Faker

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db import Base, metadata, engine

class Abonent(Base):
    __tablename__ = 'abonents'
    abonent_id = Column('abonent_id', Integer, primary_key=True)
    name = Column('name', String(50), nullable=False)
    birthday = Column('birthday', DateTime, nullable=True)
    address = Column('address', String(100), nullable=True)

    phones = relationship("AbonentPhone", back_populates="abonentp")
    emails = relationship("AbonentEmail", back_populates="abonente")
    notes = relationship("AbonentNote", back_populates="abonentn")


class AbonentPhone(Base):
    __tablename__ = 'phones'

    phone_id = Column('phone_id', Integer, primary_key = True)
    phone = Column('phone', String(100), nullable=False)

    abonent_id = Column(Integer, ForeignKey('abonents.abonent_id'), nullable=True)
    abonentp = relationship("Abonent", back_populates = "phones")


class AbonentNote(Base):
    __tablename__ = 'notes'

    note_id = Column('note_id', Integer, primary_key = True)
    
    note = Column('note', String(200), nullable=False)
    date_note = Column('date_note', DateTime, default = datetime.utcnow)

    abonent_id = Column(Integer, ForeignKey('abonents.abonent_id'), nullable=True)
    abonentn = relationship("Abonent", back_populates = "notes")


class AbonentEmail(Base):
    __tablename__ = 'emails'

    email_id = Column('email_id', Integer, primary_key = True)
    email = Column('email', String(100), nullable=True)

    abonent_id = Column(Integer, ForeignKey('abonents.abonent_id'), nullable=True)
    abonente = relationship("Abonent", back_populates = "emails")






if __name__ == '__main__':
    #x = engine.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    #print('___', x)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

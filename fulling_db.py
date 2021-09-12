from sqlalchemy import exists

from datetime import datetime
from db import session, engine
from models import Abonent, AbonentPhone, AbonentEmail, AbonentNote

#from faker import Faker

def new_records():
    
    abonent = Abonent(name = 'Benedict Cumberbatch', 
                    birthday = datetime(2002, 5, 9),
                    address = '12 Deader str London ')
    session.add(abonent)
    session.commit()
    print(abonent.name)
    print(abonent.abonent_id)
    ab_phone = AbonentPhone(abonent_id = abonent.abonent_id, 
                            phone = '0997820999')
    session.add(ab_phone)
    
    #session.commit()
    ab_email = AbonentEmail(abonent_id = abonent.abonent_id,
                            email = 'BenKem@gmail.com')
    session.add(ab_email)
    session.commit()
    
    

if __name__ == '__main__' :
    new_records()
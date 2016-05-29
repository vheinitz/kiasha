from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User
import hashlib


engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
s = DBSession()


# Admin
admin = User( 
    user_name="a",
    user_password=hashlib.md5("a").hexdigest(),
    user_real_name="Administrator",
    user_group='admin')

s.add(admin)
s.commit()

# Test User
tu = User( 
    user_name="test",
    user_password=hashlib.md5("test").hexdigest(),
    user_real_name="Test User",
    user_group='user')

s.add(tu)
s.commit()

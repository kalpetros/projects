from setup import Base, Restaurant, MenuItem, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

restaurants = session.query(Restaurant).all()
users = session.query(User).all()

for restaurant in restaurants:
	print "Id: %s, Name: %s" % (restaurant.user_id, restaurant.name)

for user in users:
	print "Id: %s, Name: %s" % (user.id, user.name)
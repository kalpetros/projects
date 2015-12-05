###########################################
###########################################
############## PROBLEM SET 1 ##############
###########################################
###########################################
import datetime
# Necessary libraries to connect to
# the database and create a session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from puppies import Base, Shelter, Puppy, Profile, Adopter
engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

########################################
########################################
############## Exercise 2 ##############
########################################
########################################

########################################
## Question 1
## Query all of the puppies and return the
## results in ascending alphabetical order
########################################

# Select all the puppies ordered by their name in ascending order
puppies = session.query(Puppy).order_by(Puppy.name.asc()).all()
# Print all the puppies
for puppy in puppies:
	print puppy.name

########################################
## Question 2
## Query all of the puppies that are less
## than 6 months old organized by the 
## youngest first
########################################

# Get current date and subtract 6 months
date = datetime.date.today() - datetime.timedelta(days = 182.5)
# Select all the puppies that are less than 6 month old
# ordered by the youngest first
puppies = session.query(Puppy.name, Puppy.dateOfBirth).filter(Puppy.dateOfBirth > date).\
		  order_by(Puppy.dateOfBirth.desc()).all()
# Print all the puppies
for puppy in puppies:
	print puppy

########################################
## Question 3
## Query all puppies by ascending weight
########################################

# Select all the puppies ordered by their weight in ascending order
puppies = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight.asc()).all()
# Print all the puppies
for puppy in puppies:
	print puppy

########################################
## Question 4
## Query all puppies grouped by the shelter
## in which they are staying
########################################

# Select all the puppies grouped by their shelter
puppies = session.query(Puppy.name, Shelter.name).\
		  join(Shelter).filter(Puppy.shelter_id==Shelter.id).\
		  group_by(Puppy.name).all()
# Print all the puppies
for puppy in puppies:
	print puppy

########################################
########################################
############## Exercise 3 ##############
########################################
########################################

# Return all the puppy profiles
profiles = session.query(Profile.id, Profile.puppy_id, Profile.picture, Profile.description, Profile.special_needs).all()
# Print all the puppies
for profile in profiles:
	print profile

# Return all the adopters
adopters = session.query(Adopter.id, Adopter.name).all()
# Print all the puppies
for adopter in adopters:
	print adopter

########################################
########################################
############## Exercise 4 ##############
########################################
########################################

# Return maximum capacity of shelters
shelters = session.query(Shelter.name, Shelter.max_capacity).all()
# Print all the shelters
for shelter in shelters:
	print "Maximum capacity of shelter (%s) is %s" % (shelter[0], shelter[1])

# Return number of puppies that are not adopted
adopters = session.query(Shelter).all()
# Print puppies and their adopter
for adopter in adopters:
	print "Current occupancy of shelter %s is %s" %(adopter.name, adopter.current_occupancy)

########################################
########################################
############## Exercise 5 ##############
########################################
########################################

########################################
########################################
############## Exercise 6 ##############
########################################
########################################

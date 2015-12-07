###########################################
###########################################
############## PROBLEM SET 1 ##############
###########################################
###########################################
import datetime
from random import randint
import random
# Necessary libraries to connect to
# the database and create a session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from sqlalchemy import func
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
puppies = session.query(func.count(Puppy.name), Shelter.name).\
		  join(Shelter).filter(Puppy.shelter_id==Shelter.id).\
		  group_by(Shelter.name).order_by(Shelter.id).all()
# Print puppies and their adopter
for puppy in puppies:
	print "Current occupancy of shelter %s is %s" %(puppy[1], puppy[0])

########################################
########################################
############## Exercise 5 ##############
########################################
########################################

puppy_images = ["http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/dog-785193_1280.jpg?direct", "http://pixabay.com/get/6540c0052781e8d21783/1433170742/dog-280332_1280.jpg?direct","http://pixabay.com/get/8f62ce526ed56cd16e57/1433170768/pug-690566_1280.jpg?direct","http://pixabay.com/get/be6ebb661e44f929e04e/1433170798/pet-423398_1280.jpg?direct","http://pixabay.com/static/uploads/photo/2010/12/13/10/20/beagle-puppy-2681_640.jpg","http://pixabay.com/get/4b1799cb4e3f03684b69/1433170894/dog-589002_1280.jpg?direct","http://pixabay.com/get/3157a0395f9959b7a000/1433170921/puppy-384647_1280.jpg?direct","http://pixabay.com/get/2a11ff73f38324166ac6/1433170950/puppy-742620_1280.jpg?direct","http://pixabay.com/get/7dcd78e779f8110ca876/1433170979/dog-710013_1280.jpg?direct","http://pixabay.com/get/31d494632fa1c64a7225/1433171005/dog-668940_1280.jpg?direct"]

# This method will make a random age for each puppy between 0-18 months(approx.) old from the day the algorithm was run.
def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0,540)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday

# This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def CreateRandomWeight():
	return random.uniform(1.0, 40.0)

# Return all shelters and their id
shelters = session.query(Shelter.id, Shelter.name).all()
for shelter in shelters:
	print shelter

# Prompt user to enter the puppy's
# name, gender and the shelter he
# wants to check it in
puppy_name = raw_input("What is the puppy's name? ")
puppy_gender = raw_input("What is the puppy's gender? ")

reset = 0
while reset == 0:
	puppy_shelter = input("Select the id of the shelter you want to check the puppy from the list above ")

	# Give user the name of the shelter he selected
	# and check if that's ok
	# If not prompt user to enter a different shelter
	i = 0
	while i == 0:
		shelters = session.query(Shelter.id, Shelter.name).all()
		print "You selected the %s shelter" % shelters[puppy_shelter-1][1]

		puppy_confirm = raw_input("Is that OK? (type Y(for Yes) or N(for No)) ")
		check = 0
		if check == 0:
			if puppy_confirm == "Y":
				print "Awesome!"
				i = 1
				check = 1
			elif puppy_confirm == "N":
				puppy_shelter = input("Select a different shelter ")
				i = 0
				check = 1
			else:
			# Prompt user to try again if user enters something
			# different other than Y or N
				puppy_confirm = raw_input("Wrong input! Please type Y(for Yes) or N(for No) ")
				check = 0

	# Count puppies in each shelter
	puppies = session.query(func.count(Puppy.name), Shelter.name).\
		join(Shelter).filter(Puppy.shelter_id==Shelter.id).\
		group_by(Shelter.name).order_by(Shelter.id).all()

    # Check max capacity for the shelter
    # that the user has selected
  	check_max_capacity = session.query(Shelter.id, Shelter.name, Shelter.max_capacity).order_by(Shelter.id).all()
  	shelter_max_capacity = check_max_capacity[puppy_shelter-1].max_capacity

	# Check if current occupancy is less than
	# the max capacity and if yes add the new
	# puppy in the shelter if not prompt user
	# to select a different shelter
	if puppies[puppy_shelter-1][0] < 20:
		# Adds the new puppy in the
		# shelter the user specified
		new_puppy = Puppy(name = puppy_name, gender = puppy_gender, dateOfBirth = CreateRandomAge(),picture=random.choice(puppy_images) ,shelter_id=puppy_shelter, weight= CreateRandomWeight())
		session.add(new_puppy)
		session.commit()
		reset = 1

		# Check current occupancy of the shelter
		# that user has selected
		puppies = session.query(func.count(Puppy.name), Shelter.name).\
	    	join(Shelter).filter(Puppy.shelter_id==Shelter.id).\
			group_by(Shelter.name).order_by(Shelter.id).all()
		print "There are %s puppies in the %s shelter after the adition of your puppy %s" %(puppies[puppy_shelter-1][0], puppies[puppy_shelter-1].name, puppy_name)
	else:
		print "The shelter you selected is full. Please select a different shelter or let the system select a shelter for you"

		select_new_shelter = raw_input("Type Y(to secect a different shelter), N(to exit the selection) or A(to auto select) ")
		check = 0
		# Exits the loop if there are no vacancies in any shelter
		commited = 0
		while check == 0:
			if select_new_shelter == "Y":
				reset = 0
				check = 1
			elif select_new_shelter == "N":
				reset = 1
				check = 1
			elif select_new_shelter == "A":
				# Check if there are vacancies in other
				# shelters and add the puppy there
				puppies = session.query(func.count(Puppy.name), Shelter.name, Shelter.id).\
	  				join(Shelter).filter(Puppy.shelter_id==Shelter.id).\
			  		group_by(Shelter.name).order_by(Shelter.id).all()

		  		# Adds the puppy in a random
		  		# shelter (if there are any vacancies)
	  			for puppy in puppies:
	  				if puppy[0] < 20:
	  					# Adds the new puppy in the
						# shelter the user specified
						new_puppy = Puppy(name = puppy_name, gender = puppy_gender, dateOfBirth = CreateRandomAge(),picture=random.choice(puppy_images),shelter_id=puppy[2], weight= CreateRandomWeight())
						session.add(new_puppy)
						session.commit()
						reset = 1
						check = 1
						commited = 1
						# Check current occupancy of the shelter
						# that the system has selected
						puppies = session.query(func.count(Puppy.name), Shelter.name, Shelter.id).\
							join(Shelter).filter(Puppy.shelter_id==Shelter.id).\
  							group_by(Shelter.name).order_by(Shelter.id).all()
						print "There are %s puppies in the %s shelter after the adition of your puppy %s" %(puppy[0]+1, puppy[1], puppy_name)
						# Breaks the for loop
						break
			else:
				select_new_shelter = raw_input("Wrong input! Please type Y(to secect a different shelter), N(to exit the selection) or A(to auto select) ")
				check = 0

			if commited == 0:
				print "There are no empty shelters this time. Please be patient as new shelters will open."
				reset = 1
				check = 1

	puppies = session.query(func.count(Puppy.name), Shelter.name, Shelter.id).\
		join(Shelter).filter(Puppy.shelter_id==Shelter.id).\
  		group_by(Shelter.name).order_by(Shelter.id).all()

	for puppy in puppies:
		print puppy

########################################
########################################
############## Exercise 6 ##############
########################################
########################################

##########################################
##########################################
################## BUGS ##################
##########################################
##########################################
## 1.
## 2.
## 3.
## 4.
## 5.
## 6.
## 7.
## 8.
## 9.
## 10.
## 11.
## 12.

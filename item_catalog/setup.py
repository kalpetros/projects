##########################################################
##########################################################
################### CONFIGURATION CODE ###################
##########################################################
##########################################################
import os
# Sys module provides a number of functions and variables
# that can be used to manipulate different parts of the
# Python run-time enviroment
import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base
# Create foreign key relationships
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
# Lets SQLAlchemy know that classes are special
# SQLAlchemy classes that correspond to tables
# in the database
# Creates a base class that the class code will inherit
Base = declarative_base()
#########################################################
#########################################################
################### CLASS DEFINITIONS ###################
#########################################################
#########################################################
# All code for out table and mapper code
# Two classes that correspond with the two
# tables in the database (restaurant, menu item)
class Restaurant(Base):
# table representation
# double underscore = lets SQLAlchemy know the
# variable that we'll use to refer to the table
	__tablename__ = 'restaurant'
	###############################################
	###############################################
	################### MAPPERS ###################
	###############################################
	###############################################
	name = Column(
		# nullable = indicates that if name is not
		# filled out we can not create a new
		# restaurant row in this database
		String(80), nullable = False)

	description = Column(
		String(120), nullable = False)

	logo = Column(
		String(80), nullable = False)

	id = Column(
		Integer, primary_key = True)

	@property
	def serialize(self):

		return {
			'name': self.name
		}

class MenuItem(Base):
# table representation
# double underscore = lets SQLAlchemy know the
# variable that we'll use to refer to the table
	__tablename__ = 'menu_item'
	###############################################
	###############################################
	################### MAPPERS ###################
	###############################################
	###############################################
	name = Column(
		# nullable = indicates that if name is not
		# filled out we can not create a new
		# menu item row in this database
		String(80), nullable = False)

	id = Column(
		Integer, primary_key = True)

	course = Column(
		String(250))

	description = Column(
		String(250))

	price = Column(
		String(8))

	restaurant_id = Column(
		# ForeignKey will create the
		# foreign key relationship between
		# the menu item class and the restaurant class
		# Looks inside the restaurant table and retrieves
		# the ID number whenever it asks for restaurant_id
		Integer, ForeignKey('restaurant.id'))

	restaurant = relationship(Restaurant)

# We added this serialize function to be able to send JSON objects in a
# serializable format
	@property
	def serialize(self):

		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'price': self.price,
			'course': self.course,
		}

#########################################################
#########################################################
############### INSERT AT THE END OF FILE ###############
#########################################################
#########################################################
# Instance of the create_engine class
# that points to the database that we'll use
engine = create_engine(
	'sqlite:///restaurants.db')
# Goes into the database and adds
# the classes we'll create as new
# tables in the database
Base.metadata.create_all(engine)

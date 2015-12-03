from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

adopt_puppy = Table('adopt_puppy', Base.metadata,
    Column('puppy_id', Integer, ForeignKey('puppies.id')),
    Column('adopter_id', Integer, ForeignKey('adopters.id'))
)

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    # Shelter's maximum capacity
    max_capacity = Column(Integer)
    # Current number of puppies that
    # haven't yet been adopted
    current_occupancy = Column(Integer)
    
class Puppy(Base):
    __tablename__ = 'puppies'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))
    profile = relationship("Profile", uselist=False, backref="puppies")
    adopter = relationship("Adopter", secondary=adopt_puppy, backref="puppies")

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    puppy_id = Column(Integer, ForeignKey('puppies.id'))
    picture = Column(String)
    description = Column(String)
    special_needs = Column(String)
    
class Adopter(Base):
    __tablename__ = 'adopters'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)

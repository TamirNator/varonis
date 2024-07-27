from sqlalchemy import Column, Integer, String, Boolean, Time, create_engine, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the Restaurant class, which maps to the 'restaurants' table in the database
class Restaurant(Base):
    __tablename__ = 'restaurants'  # Specifies the table name in the database

    # Define columns in the 'restaurants' table
    id = Column(Integer, primary_key=True)  # Integer column 'id', primary key
    name = Column(String, nullable=False)  # String column 'name', cannot be null
    address = Column(String, nullable=False)  # String column 'address', cannot be null
    style = Column(String, nullable=False)  # String column 'style', cannot be null
    vegetarian = Column(Boolean, nullable=False)  # Boolean column 'vegetarian', cannot be null
    opening_hour = Column(Time, nullable=False)  # Time column 'opening_hour', cannot be null
    closing_hour = Column(Time, nullable=False)  # Time column 'closing_hour', cannot be null
    deliveries = Column(Boolean, nullable=False)  # Boolean column 'deliveries', cannot be null

# Define the RequestLog class, which maps to the 'request_logs' table in the database
class RequestLog(Base):
    __tablename__ = 'request_logs'  # Specifies the table name in the database

    id = Column(Integer, primary_key=True)  # Integer column 'id', primary key
    timestamp = Column(DateTime, default=datetime.utcnow)  # DateTime column 'timestamp'
    request_data = Column(Text, nullable=False)  # Text column 'request_data', cannot be null
    response_data = Column(Text, nullable=False)  # Text column 'response_data', cannot be null

# Database setup
DATABASE_URL =   # Update this with your PostgreSQL connection string

# Create a new SQLAlchemy engine instance with check_same_thread=False
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create all tables defined by the ORM models that inherit from Base
Base.metadata.create_all(engine)

# Create a sessionmaker factory, bound to the engine
Session = sessionmaker(bind=engine)

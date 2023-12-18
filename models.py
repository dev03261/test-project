# models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum,DateTime
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    password = Column(String)


    def check_password(self, password):
        return self.password == password


class MeetingRoom(Base):
    __tablename__ = "meeting_rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String, unique=True, index=True)
    capacity = Column(Integer)
    floor_location = Column(String)
    availability_status = Column(String)


class Booking(Base):
    __tablename__ = "bookings"
    BookingID = Column(Integer, primary_key=True, index=True)
    Date = Column(DateTime, default=datetime.utcnow)
    Time = Column(DateTime)
    Duration = Column(Integer)
    UserID = Column(Integer, ForeignKey("users.id"))
    RoomID = Column(Integer, ForeignKey("meeting_rooms.id"))
    StartTime = Column(DateTime, default=datetime.utcnow)
    EndTime = Column(DateTime)


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

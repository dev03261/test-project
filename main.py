import statistics
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User, SessionLocal, MeetingRoom,Booking
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi import HTTPException
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#----------------------user-------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------

@app.post("/create_user/")
def create_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = db.query(User).filter(User.email == email).first()
    if not email.endswith("@devsinc.com"):
        raise HTTPException(status_code=400, detail="Invalid email format. Email must end with @devsinc.com")

    # Create the user
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}

@app.delete("/delete_user/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_to_delete)
    db.commit()

    return {"message": "User deleted successfully"}

@app.put("/update_user/{user_id}")
def update_user(user_id: int, new_username: str, new_email: str, new_password: str, db: Session = Depends(get_db)):
    user_to_update = db.query(User).filter(User.id == user_id).first()
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_to_update.username = new_username
    user_to_update.email = new_email
    user_to_update.password = new_password

    db.commit()

    return {
        "message": "User updated successfully",
        "user_id": user_to_update.id,
        "new_username": new_username,
        "new_email": new_email,
        "new_password": new_password
    }


@app.get("/get_user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }






#------------------------LOGIN---------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

@app.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if user is None or not user.check_password(password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful", "user_id": user.id}



#-----------------------------------MEETING ROOMS-----------------------------------------------
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------


@app.post("/meeting_rooms/")
def create_meeting_room(room_name:str,capacity:int,floor_location:str,availability_status:bool,db: Session = Depends(get_db)):
    new_room = MeetingRoom(room_name=room_name,capacity=capacity,floor_location=floor_location,availability_status=availability_status)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return ("meeting room created successfully")

@app.get("/meeting_rooms/{room_id}")
def read_meeting_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(MeetingRoom).filter(MeetingRoom.id == room_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Meeting room not found")
    return room

@app.delete("/meeting_rooms/{room_id}")
def delete_meeting_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(MeetingRoom).filter(MeetingRoom.id == room_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Meeting room not found")

    db.delete(room)
    db.commit()
    return room


#-----------------------------------BOOKINGS-----------------------------------------------
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------


@app.post("/bookings/")
def create_booking(user_id: int, room_id: int, duration: int, db: Session = Depends(get_db)):
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration)

    existing_booking = db.query(Booking).filter(
        Booking.RoomID == room_id,
        Booking.EndTime > start_time,
        Booking.StartTime < end_time
    ).first()

    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking for the same room and time range already exists",
        )

    new_booking = Booking(UserID=user_id, RoomID=room_id, StartTime=start_time, EndTime=end_time)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking



@app.get("/bookings/{booking_id}")
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.BookingID == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.BookingID == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return booking




#-----------------------------------LOGOUT-----------------------------------------------
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------



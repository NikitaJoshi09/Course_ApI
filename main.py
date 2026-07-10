from sqlmodel import SQLModel,Session,select
from sqlalchemy.exc import OperationalError
from database import engine,get_session
from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from models import Course

app = FastAPI()
@app.on_event("startup")
def on_statrtup():
    try:
        SQLModel.metadata.create_all(engine)
        print("database connected successfully")
    except OperationalError as e:
        print("database connection faild",e)  

@app.get("/")
def get_home():
    return{"message":"hello fastapi"}



#create
# @app.post("/course")
# def create_course(course: Course, session:Session = Depends(get_session)):
#     session.add(course)
#     session.commit()
#     session.refresh(course)
#     return course

#get all 
@app.get("/course")
def get_all_course(session:Session= Depends(get_session)):
    return session.exec(select(Course)).all()



@app.get("/course/active")
def get_active(session:Session= Depends(get_session)):
    course =  session.exec(select(Course).where(Course.is_active == True)).all()
    if not course:
        raise HTTPException(status_code=404,detail = 'course not found')
    return course

#get one
@app.get("/course{id}")
def get_one_course(id:int,session:Session = Depends(get_session)):
    course = session.get(Course,id)
    if not course:
        raise HTTPException(status_code=404,detail="course not found")
    return course



#update
@app.put("/course{id}")
def update_course(id : int , updated : Course, session:Session= Depends(get_session)):
    course  = session.get(Course,id)
    if not course:
        raise HTTPException(status_code=404,detail="course not found")
    course.name = updated.name
    course.duration_weak = updated.duration_weak
    course.fees = updated.fees
    session.add(course)
    session.commit()
    session.refresh(course)
    return{"message":"course updated","data":course}

#delete
@app.delete("/course{id}")
def delete_course(id:int,session:Session = Depends(get_session)):
    course = session.get(Course,id)
    if not course:
        raise HTTPException(status_code=404,detail="course not found")
    session.delete(course)
    session.commit() 
    return{"message:":"delete course","data":course}

#filter with query parameter
@app.get("/course/expensive")
def get_all_course(min_fees:int, session:Session= Depends(get_session)):
    course =  session.exec(select(Course).where(Course.fees>=min_fees)).all()
    if not course:
        raise HTTPException(status_code=404,detail = 'course not found')
    return course 

@app.get("/course/expensive")
def get_all_course(min_fees:int, session:Session= Depends(get_session)):
    course =  session.exec(select(Course).where(Course.fees>=min_fees)).all()
    if not course:
        raise HTTPException(status_code=404,detail = 'course not found')
    return course




    






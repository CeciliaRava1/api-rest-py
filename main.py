from http.client import HTTPException
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Course(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    level: str
    duration: int

dbCourses = []

@app.get('/courses', response_model=List[Course])
def getCourses():
    return dbCourses

@app.post('/courses', response_model=Course)
def createCourse(course:Course):
    course.id = str(uuid.uuid4())
    dbCourses.append(course)
    return course

@app.get('/courses/{course_id}', response_model=Course)
def getCourse(courseId:str):
    course = next((course for course in dbCourses if course.id == courseId), None)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course

@app.put('/courses/{courseId}', response_model=Course)
def updateCourse(courseId:str, updatedCourse:Course):
    course = next((course for course in dbCourses if course.id == courseId), None)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    updatedCourse.id = courseId
    index = dbCourses.index(course)
    dbCourses[index] = updatedCourse
    return updatedCourse

@app.delete('/courses/{courseId}', response_model=Course)
def deleteCourse(courseId:str):
    course = next((course for course in dbCourses if course.id == courseId), None)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    dbCourses.remove(course)
    return course
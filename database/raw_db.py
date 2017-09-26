from dorm import db;
import config

class course(db.model):
    name=db.field(type="char(20)",constrain="not null", key="primary")
    description=db.field(type="text")
    college=db.field(type="char(20)",constrain="not null")

class student(db.model):
    reg_no=db.field(type="char(20)",constrain="not null",key="primary")
    full_name=db.field(type="char(50)",constrain="not null")
    course=db.field(type="char(20)",constrain="not null", key="foreign", ref="course.name")
    year=db.field(type="int", constrain="not null")

def run():
   course().create()
   astudent().create()

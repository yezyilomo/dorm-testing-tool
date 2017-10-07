from dorm import db;
import config

class course(db.model):
    name=db.field(type="char(20)", key="primary")
    description=db.field(type="text")
    college=db.field(type="char(20)",constrain="not null")

class student(db.model):
    reg_no=db.field(type="char(20)",key="primary")
    full_name=db.field(type="char(50)",constrain="not null")
    year=db.field(type="int", constrain="not null")
    course=db.field(type="char(20)",constrain="not null", key="foreign", ref="course.name")

def run():
   course().create()
   student().create()

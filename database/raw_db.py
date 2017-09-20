from dorm import db;
import config

class Dancer(db.model):
    cont_num=db.field(type="int",constrain="auto_increment",key="primary")
    name=db.field(type="char(20)",constrain="not null")
    age=db.field(type="int")
    dance_type=db.field(type="char(6)", constrain="not null")
    music_type=db.field(type="char(6)", constrain="not null")

def run():
   Dancer().create()

import os
import random
import string
import collections
from flask import Flask, render_template, request
from dorm import db
from database import config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/home/yezy/flaskproject/static/pics"

def get_rec_values(rec,cl):
    val=getattr(rec,cl)
    return '{}'.format(val)

def randstr(length):
   all_letters=string.ascii_lowercase[:]
   st=""
   for i in range(0,length):
     st=st+all_letters[random.randint(0,len(all_letters)-1)]
     st=st[0].upper()+st[1:]
   return st
app.jinja_env.globals.update(get_rec_values=get_rec_values)

@app.route('/',methods = ['POST', 'GET'])
def home():
   max_data=500
   if request.method=="GET":
     rand_table=db.random_table()
     get_table=getattr(db,rand_table)
     table=get_table()
     data=table.get()
     if len(data)>max_data:
         data=data[:max_data]
     return render_template("home.html",data=data, flag='tuple', table_used=table.table__name__)

   if request.method=="POST":
     query=request.form['query']
     splitted_query=query.split('.')
     data=""
     tb_name="Unkown"
     if splitted_query[1].startswith( "execute(" ):
         data=eval(query)
         check="value"
         if data is None:
            data="Query done!.."
         else:  ########################This is for making execute() UI more friendly####
            rand_table=db.random_table()
            get_table=getattr(db,rand_table)
            table=get_table()
            table.table__name__=query
            table.table__columns__=data.columns
            table.primary__keys__=data.columns
            result=db.get_objects(data.fetch, data.columns, table)
            data=db.custom_tuple_read(result)
            check="tuple"
            #############################################################################
     else:
        tb_name=eval("db."+splitted_query[1]).table__name__
        data=eval(query)

        if isinstance(data,db.custom_tuple_read):
            check="tuple"
            if len(data)>max_data:
               data=data[:max_data]
        else:
           check="value"

     return  render_template("home.html",data=data,qr=query, flag=check, table_used=tb_name)

from flask import Flask, render_template, request
from werkzeug import secure_filename
from flaskext.mysql import MySQL
import os, random, string, importlib
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
     table=getattr(db,rand_table)
     data=table().get()

     check=""
     if isinstance(data,db.custom_tuple_write) or isinstance(data,db.custom_tuple_read):
        check='tuple'
     elif isinstance(data,str) or isinstance(data,int) or isinstance(data,float) or isinstance(data, tuple):
        check='value'
     elif data==None :
        check='None'
        data=globals()[splitted_query[0]].get()
     else:
        check=='object'
        val={}
        for cl in tb_col:
           val.update({cl:get_rec_values(data,cl)})
        data=val
     if len(data)>max_data:
         data=data[:max_data]
     return render_template("home.html",sq=data, data=check, table_used=table().table__name__)

   if request.method=="POST":
     query=request.form['query']
     splitted_query=query.split('.')
     data=""

     if splitted_query[1].startswith( "sql(" )  or  splitted_query[2].startswith( "join(" ) :
         result=eval(query)
         tb_name=result[0].table__name__
         data=result
     else:
        tb_name=getattr(globals()['db'], splitted_query[1][:len(splitted_query[1])-2])().table__name__
        data=eval(query)


     check=""
     if isinstance(data, db.custom_tuple_write) or isinstance(data,db.custom_tuple_read):
        check='tuple'
     elif isinstance(data,str) or isinstance(data,int) or isinstance(data,float) or isinstance(data, tuple):
        check='value'
     elif data==None :
        check='None'
        command="db."+splitted_query[1]+".get()"
        data=eval(command)
     else:
        check=='object'
        val={}
        for col in tb_col:
           val.update({col:get_rec_values(data,col)})
        data=val

     if len(data)>max_data:
         data=data[:max_data]
     return  render_template("home.html",sq=data,qr=query, data=check, table_used=tb_name)

from flask import Flask, render_template, request
from werkzeug import secure_filename
from flaskext.mysql import MySQL
import os, random, string
from orm import Table, orm

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/home/yezy/flaskproject/static/pics"
orm.configure_db(db_user='root',db_name='rev',db_host='localhost',db_password='ilomo')

def get_rec_values(rec,cl):
    command="val=rec."+cl
    exec(command)
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
   if request.method=="GET":
     table=Table(Table.random_table())
     data=table.get()
     tb_col=table.table__columns__
     check=""
     if isinstance(data,tuple):
        check='tuple'
     elif isinstance(data,str) or isinstance(data,int) or isinstance(data,float):
        check='value'
     elif data==None :
        check='None'
        command="data"+splitted_query[0]+".get()"
        exec(command)
     else:
        check=='object'
        val={}
        for cl in tb_col:
           val.update({cl:get_rec_values(data,cl)})
        data=val
     return render_template("home.html",sq=data,cols=tb_col,data=check, table_used=table.table__name__)

   if request.method=="POST":
     query=request.form['query']
     splitted_query=query.split('.')
     command="tb_col="+splitted_query[0]+".table__columns__"
     exec(command)
     command="tb_name="+splitted_query[0]+".table__name__"
     exec(command)
     statement="data="+query
     exec(statement)
     check=""
     if isinstance(data,tuple):
        check='tuple'
     elif isinstance(data,str) or isinstance(data,int) or isinstance(data,float):
        check='value'
     elif data==None :
        check='None'
        command="data="+splitted_query[0]+".get()"
        exec(command)
     else:
        check=='object'
        val={}
        for col in tb_col:
           val.update({col:get_rec_values(data,col)})
        data=val
     return  render_template("home.html",sq=data,qr=query,cols=tb_col, data=check, table_used=tb_name)




from flask import Flask,jsonify,Response
from sqlalchemy import create_engine,Table,MetaData,select,insert,delete
import json
conn = ''  #Url for the database
engine = create_engine(
    conn,
    isolation_level="READ UNCOMMITTED"
)
conn = engine.connect()
user_table = Table('users',MetaData(),autoload_with=engine)

username = 'Hello'
password = 'world'




app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello'

@app.route('/<path:user>/<path:passwd>')
def get_info(user,passwd):
    if user==username and passwd == password:
        query = select(user_table)
        result = conn.execute(query).fetchall()
        dat = json.dumps({"data": dict(result)})
        resp = Response(response=dat, status=200, mimetype="application/json")
        return resp
    else:
        return Response(response='Unauthorized',status=401)


if __name__=='__main__':
   app.run()
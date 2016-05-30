import os
import sys
import json
#import urllib2
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Survey, Question
import hashlib
from datetime import datetime


engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
#s = DBSession()


from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack


app = Flask(__name__, static_url_path='')

session={}

session['dbg_admin']={'user_id':0,'user_group':'admin'} 



@app.route('/', methods = ['GET'])
def root():
    return app.send_static_file('./index.html')


############### USER ##################################
@app.route('/api/user/login', methods=['POST'])
def api_user_login():
    d = request.json 
    s = DBSession()  
    
    data = '{"result":"error","reason":"Login error"}'
    grp='' 
    print d   
    try:
        q = s.query(User).filter_by( user_name=d['user'],
            user_password=hashlib.md5(d['password']).hexdigest(), ).one()
        if q:
            sid = hashlib.md5(str(datetime.today())).hexdigest()
            session[sid]={'user_id':q.user_id,'user_group':q.user_group}        
        
        data = '{"result":"OK", "session":"%s"}' % ( sid )   
             
    except Exception as e:
        print str(e)
        
    s.commit()  
    s.close()
    print data
    return data

@app.route('/api/user/logout', methods=['GET', 'POST'])
def api_user_logout( ):
    d = request.json
    data = '{"result":"error","reason":"Logout error"}'
    if d['session'] in session:
        del session[ d['session'] ]
        print session
        data = '{"result":"OK","info":"logged out"}'
            
    return data

@app.route('/api/user/add', methods=['GET', 'POST'])
def api_user_add(): 
    data = '{"result":"error","reason":"TODO"}'
    return data

@app.route('/api/user/<int:user_id>/delete', methods=['GET', 'POST'])
def api_user_delete(user_id): 
    data = '{"result":"error","reason":"TODO"}'
    return data

############### ADMIN ##################################
@app.route('/api/admin/initdb', methods=['GET', 'POST'])
def api_admin_initdb():
    conn = sqlite3.connect('databsae.db')
    ret = conn.execute("DROP TABLE IF EXISTS t_users")
    ret = conn.execute("""
        CREATE TABLE t_users 
            ( [user] TEXT, [password] TEXT, [group] TEXT, [name] TEXT, [email] TEXT)
        """)
    ret = conn.execute("""
        INSERT INTO t_users ([user],[password],[group]) 
            VALUES ('admin', 'a', 'admin')
        """)
    conn.commit()
    conn.close()
    data = '{"result":"ok","info":"DB created successfully!"}'
    return data


#################### PROJECT ###############################
@app.route('/api/project/add', methods=['GET', 'POST'])
def api_project_add(): 
    data = '{"result":"error","reason":"TODO"}'
    return data

@app.route('/api/project/<int:project_id>/delete', methods=['GET', 'POST'])
def api_project_delete(project_id): 
    data = '{"result":"error","reason":"TODO"}'
    return data

@app.route('/api/project/list', methods=['GET', 'POST'])
def api_project_list(): 
    data = '{"result":"error","reason":"TODO"}'
    return data

@app.route('/api/project/<int:project_id>/select', methods=['GET', 'POST'])
def api_project_select(project_id): 
    data = '{"result":"error","reason":"TODO"}'
    return data
    
#################### QUESTION ###############################
@app.route('/api/question/add', methods=['GET', 'POST'])
def api_question_add(): 
    data = '{"result":"error","reason":"TODO"}'
    return data

@app.route('/api/question/<int:question_id>/delete', methods=['GET', 'POST'])
def api_question_delete(question_id): 
    data = '{"result":"error","reason":"TODO"}'
    return data

@app.route('/api/question/list', methods=['GET', 'POST'])
def api_question_list(): 
    data = '{"result":"error","reason":"TODO"}'
    return data

@app.route('/api/question/<int:id>/select', methods=['GET', 'POST'])
def api_question_select(id): 
    s = DBSession()
    data = '{"result":"error","reason":"TODO"}'
    d = request.json
    print d
    if d['session'] in session:
        
        s.commit()
        s.close()
        data = '{"result":"OK","data":{"TODO for id":%d}}'%(id)
    return data

#################### SURVEY ###############################
@app.route('/api/survey/add', methods=['GET', 'POST'])
def api_survey_add():
    s = DBSession()
    data = '{"result":"error","reason":"TODO"}'
    d = request.json
    print d
    if d['session'] in session:
        sv = Survey(survey_name=d['survey_name'],survey_info=d['survey_name'],
            survey_instructions=d['survey_instructions'], survey_owner=0)
            #int(d['session']['user_id']) )
        s.add(sv)
        s.flush()
        s.refresh(sv)
        id = sv.survey_id
        s.commit()
        s.close()
        data = '{"result":"OK","data":{"survey_id":%d}}'%(id)
    return data

@app.route('/api/survey/<int:id>/delete', methods=['GET', 'POST'])
def api_survey_delete(id): 
    data = '{"result":"error","reason":"Undefined"}'
    try:                      
        d = request.json
        print "REeurst", d, "ID", id
        if d['session'] in session:
            s = DBSession()  
            q = s.query(Survey).filter_by(survey_id=id).one()
            if q:
                s.delete(q)
                s.commit()
            s.close()
            data = '{"result":"OK","info":"Deleted survey ID: %s"}'%(id)
    except Exception as e:
        print str(e)    
    
    return data

@app.route('/api/survey/list', methods=['GET', 'POST'])
def api_survey_list(): 
    print '/api/survey/list'
    data = '{"result":"error","reason":"Undefined"}'
    try:                        
        d = request.json
        print "DATA:", d
        if d['session'] in session:
            sd=session[ d['session'] ]
            print sd
            s = DBSession()
            q = s.query(Survey).filter_by(survey_owner=sd['user_id'] )
            ret_data = []
            for srv in q:
                ret_data.append( srv.toDict() )
            
            #print json.dumps(ret_data)
            s.close()
            data = '{"result":"OK","data":%s}'%(json.dumps(ret_data))
    except Exception as e:
        print str(e)    
    
    return data

@app.route('/api/survey/<int:id>/select', methods=['GET', 'POST'])
def api_survey_select(id): 
    data = '{"result":"error","reason":"Undefined"}'
    try:                      
        d = request.json
        print "REeurst", d, "ID", id
        if d['session'] in session:
            s = DBSession()  
            srv = s.query(Survey).filter_by(survey_id=id).one()
            if srv:                
                s.close()
                data = '{"result":"OK","data":%s}'%( srv.toJson() )
    except Exception as e:
        print str(e)    
    
    return data
    
@app.route('/api/survey/<int:id>/question/add', methods=['GET', 'POST'])
def api_urvey_question_add(id): 
    s = DBSession()
    data = '{"result":"error","reason":"TODO"}'
    d = request.json
    print d
    if d['session'] in session:
        
        s.commit()
        s.close()
        data = '{"result":"OK","data":{"TODO for id":%d}}'%(id)
    return data
    
@app.route('/api/survey/<int:sid>/question/<int:qid>/delete', methods=['GET', 'POST'])
def api_survey_question_delete(sid, qid): 
    s = DBSession()
    data = '{"result":"error","reason":"TODO"}'
    d = request.json
    print d
    if d['session'] in session:
        
        s.commit()
        s.close()
        data = '{"result":"OK","data":{"TODO for id":%d}}'%(sid)
    return data

@app.route('/api/survey/<int:sid>/question/<int:qid>/select', methods=['GET', 'POST'])
def api_urvey_question_select(sid, qid): 
    s = DBSession()
    data = '{"result":"error","reason":"TODO"}'
    d = request.json
    print d
    if d['session'] in session:
        
        s.commit()
        s.close()
        data = '{"result":"OK","data":{"TODO for id":%d}}'%(sid)
    return data
        
    
if __name__ == '__main__':
    app.run(debug=True);
    app.run(host='0.0.0.0', port=5000)
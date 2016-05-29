from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User
import hashlib

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
s = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
        
        
    def do_GET(self):
        try:
            if self.path.endswith("/users"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Users</h1>"
                for u in s.query(User).all():
                    output += "<p><h3>"+u.user_name+"</h3>"
                    output += '<a href="/users/{0}/edit">edit</a> <br>'.format(u.user_id)
                    output += '<a href="/users/{0}/delete">delete</a>'.format(u.user_id)
                    output += "</p>"
                    
                output += '''
                    <form method='POST' enctype='multipart/form-data' action='/users/new'>
                      <h2>New User</h2>
                      <input name="user_name" type="text" >
                      <input name="user_password" type="text" >
                      <input name="user_email" type="text" >
                      <input name="user_real_name" type="text" >
                      <input name="user_group" type="text" >
                      <input type="submit" value="Submit"> 
                    </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            
            if self.path.endswith("/edit"):
                uid = self.path.split("/")[2]
                q = s.query(User).filter_by( user_id=uid).one()
                if q:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += q.user_name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/userd/%s/edit' >" % uid
                    output += "<input name = 'user_real_name' type='text' placeholder = '%s' >" % q.user_real_name
                    output += "<input type = 'submit' value = 'OK'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
            
            if self.path.endswith("/delete"):
                uid = self.path.split("/")[2]
                q = s.query(User).filter_by( user_id=uid).one()
                if q:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1> Are you sure you want tu delete: "
                    output += q.user_name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/userd/%s/delete' >" % uid
                    output += "<input type = 'submit' value = 'YES'>"
                    output += "</form>"
                    output += " <a href = '/users'> Cancel </a>"   
                    output += "</body></html>"
                    self.wfile.write(output)
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/users/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('user_name')

                    # Create new Restaurant Object
                    u = User(user_name=messagecontent[0],user_password='', user_real_name='',user_email='',user_group='' )
                    s.add(u)
                    s.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/users')
                    self.end_headers()
            
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    urn = fields.get('user_real_name')
                    uid = self.path.split("/")[2]

                    q = s.query(User).filter_by(user_id=uid).one()
                    if q != []:
                        q.user_real_name = urn[0]
                        s.add(q)
                        s.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/users')
                        self.end_headers()
            
            if self.path.endswith("/delete"):
                uid = self.path.split("/")[2]
                q = s.query(User).filter_by(user_id=uid).one()
                if q:
                    s.delete(q)
                    s.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/users')
                    self.end_headers()
                    
        except:
            self.send_response(501)
            print "ERROR!";
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
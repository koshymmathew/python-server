import SimpleHTTPServer
import SocketServer
import logging
import cgi

import sys



if len(sys.argv) > 2:
    PORT = int(sys.argv[2])
    I = sys.argv[1]
elif len(sys.argv) > 1:
    PORT = int(sys.argv[1])
    I = ""
else:
    PORT = 8000
    I = ""


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'Host':self.headers['Host'],
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        
 
        #self.send_response( 200 )
        length = int(self.headers.getheader('content-length'))        
        data_string = self.rfile.read(length)
        print data_string
        
        try:
            f = open("data.txt","ab")
            f.write(data_string+"\n")
            print "written into file"
        except Exception,e:
            print "cant open file "
            raise

        #import pdb;pdb.set_trace();
        #for item in form.list:
            #print item
           # logging.warning(item)
           # logging.warning("\n")
        
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "@rochacbruno Python http server version 0.1 (for testing purposes only)"
print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)
httpd.serve_forever()
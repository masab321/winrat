import os
import cgi
import http.server as server

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    """Extend SimpleHTTPRequestHandler to handle POST requests"""
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        filename = form['file'].filename
        data = form['file'].file.read()

        if not os.path.isdir("data"):
            os.makedirs("data")

        with open(f"./data/{filename}", "wb") as outfile:
            outfile.write(data)
        
        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = 'Saved "%s"\n' % filename
        self.wfile.write(reply_body.encode('utf-8'))
    
if __name__ == '__main__':
    server.test(HandlerClass=HTTPRequestHandler)

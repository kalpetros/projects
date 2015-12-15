from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
# Indicates what code to execute based
# on the type of HTTP request that is
# sent to the server
class webServerHandler(BaseHTTPRequestHandler):
    # Handles all GET requests the
    # web server receives
    def do_GET(self):
        try:
            # looks for the url that ends with /hello
            if self.path.endswith("/restaurants"):
                # if the above is found sent a status
                # code of 200 indicating a successfull
                # get request
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>List of Restaurants!</h1>"
                output += ''''''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        # Throw an exception if url is not found
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
    # Create a POST request
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
        except:
            pass
# Intantiate the server
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        # Keep it running until
        # there is a keyboard
        # interuption
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        # Shut down the server
        # by issuing ctrl+c
        server.socket.close()
# Run the main method
if __name__ == '__main__':
    main()

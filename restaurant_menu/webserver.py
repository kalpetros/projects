from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# Indicates what code to execute based
# on the type of HTTP request that is
# sent to the server
class WebServerHandler(BaseHTTPRequestHandler):
    # Handles all GET requests the
    # web server receives
    def do_GET(self):
        # looks for the url that ends with /hello
        if self.path.endswith("/hello"):
            # if the above is found sent a status
            # code of 200 indicating a successfull
            # get request
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>Hello!</body></html>"
            self.wfile.write(message)
            # might come handy for debugging
            print message
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)
# Intantiate the server
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
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

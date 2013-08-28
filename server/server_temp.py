
import BaseHTTPServer
import SocketServer
import sys
import shutil
import read_temp


HOST = ''
PORT = 8000
    

template = '''
<html>
 <body>
   <p>Last temperature reading: {0:s}</p>
   <p>Temperature: {1:0.1f} F</p>
   <p>Humidity: {2:0.1f} %</p>
 </body>
</html>
'''


class TempServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        timestamp, temperature, humidity = read_temp.read_current_temperature()
        s = template.format(timestamp, temperature, humidity)
        length = len(s)
        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html;  charset=%s" %encoding)
        self.send_header("Content-Length", str(length))
        self.end_headers()
        self.wfile.write(s)

handler = TempServer
httpd = SocketServer.TCPServer((HOST, PORT), handler)

httpd.serve_forever()

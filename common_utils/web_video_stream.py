import cv2
from PIL import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time
from threading import Thread
import socket

#HTTP Classes
class CamHandler(BaseHTTPRequestHandler):
	stream = {}
	keeper = True
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			s = self.stream[self.path[1:]]
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while self.keeper:
				img = s.get_frame()
				if img is not None:
					imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
					jpg = Image.fromarray(imgRGB)
					tmpFile = StringIO.StringIO()
					jpg.save(tmpFile,'JPEG')
					self.wfile.write("--jpgboundary")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(tmpFile.len))
					self.end_headers()
					jpg.save(self.wfile,'JPEG')
					time.sleep(0.001)
			return
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://'+s.ip+':'+s.port+'/'+s.fileName+'"/>')
			self.wfile.write('</body></html>')
			return
	def do_POST(self):
		self.send_response(200)
		self.send_header('Content-type','text/xml')
		self.end_headers()
		self.wfile.write('<ping>None</to>')
		return
	def finish(self,*args,**kw):
		self.keeper = False
		try:
			BaseHTTPRequestHandler.finish(self)
		except socket.error:
			pass
	def handle(self):
		try:
			BaseHTTPRequestHandler.handle(self)
		except socket.error:
			pass
	def log_message(self, format, *args):
		return
	def update_frame(self,frame):
		self.frame = frame
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""
	stopped = False

	def pass_stream(self, stream,fileName):
		self.RequestHandlerClass.stream[fileName] = stream
	def close_keeper(self):
		self.RequestHandlerClass.keeper = False

#Wrapper Class
class mjpg_stream():
	def __init__(self, ip='127.0.0.1',fileName='stream.mjpg', port=8080, supressDebug=False):
		self.port = port
		self.ip = ip
		self.supressDebug = supressDebug
		self.fileName = fileName
		Thread(target=self._start_server).start()
	def get_frame(self):
		return self.frame
	def update_frame(self, frame):
		self.frame = frame
	def _start_server(self):
		try:
			self.server = ThreadedHTTPServer((self.ip, self.port), CamHandler)
			if not self.supressDebug:
				print "-> MJPG stream is running: http://"+self.ip+":"+str(self.port)+'/'+self.fileName
			self.server.pass_stream(self,self.fileName)
			self.server.serve_forever()
		except KeyboardInterrupt:
			self.server.socket.close()
	def disconnect(self):
		self.server.close_keeper()
		self.server.shutdown()
		self.server.socket.close()

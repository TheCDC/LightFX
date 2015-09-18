
import pyaudio # from http://people.csail.mit.edu/hubert/pyaudio/
import serial
import audioop
import sys
import math
import time
import optparse
def list_devices():
	# List all audio input devices
	p = pyaudio.PyAudio()
	i = 0
	for i in range(p.get_device_count()):
		dev = p.get_device_info_by_index(i)
		if dev['maxInputChannels'] > 0:
			return str(i) + '. ' + dev['name']

def select_device():
	# list_devices()
	device   = int(input("Select a sound input device\n>>>"))
	return device
	
def scale_audio(rms, scale, exponent):
	return (float(rms) /(2.0  ** 16.0) * scale)**exponent 

def constrain(n,a,b):
	if n < a:
		return a
	elif n > b:
		return b
	else:
		return n
	return a*(n < a) + b*(n > b) + n * ( (n < b) and (n > a) )

def main():
	chunk    = 1024 # Change if too fast/slow, never less than 1024
	scale    = 50   # Change if too dim/bright
	exponent = 4    # Change if too little/too much difference between loud and quiet sounds

	parser = optparse.OptionParser()
	parser.add_option("-d", "--debug", help="Enable debugging options.", metavar="DEBUG", default=False)
	parser.add_option("-p", "--port", help="Specify Arduino serial port.", metavar="port", default=-1)
	parser.add_option("-s", "--scale", help="Specify scale of audio.", metavar="scale", default=1)
	parser.add_option("-e", "--exponent", help="Specify exponent of audio.", metavar="exponent", default=1)
	parser.add_option("-b", "--baudrate", help="Specify serial baud rate.", metavar="baudrate", default=115200)
	parser.add_option("-c", "--chunk", help="Specify audio sample chunk size.", metavar="chunk", default=2048)
	parser.add_option("-l", "--list_devices", help="List all possible audio devices to use then quit", metavar="devices", default=False)
	parser.add_option("-a", "--audio_device", help="Specify index of audio device to use.", metavar="device", default=-1)
	parser.add_option("-g", "--graphical", help="Draw bar graph in console.", metavar="GRAPH", default=False)

	(options, args) = parser.parse_args()
	myPort = options.port
	DEBUG = bool(options.debug)
	if options.debug == "False" or options.debug == 0:
		DEBUG = False
	elif options.debug == "True" or options.debug == 1:
		DEBUG = True
	scale = float(options.scale)
	exponent = float(options.exponent)
	baudrate = options.baudrate
	chunk = int(options.chunk)
	do_list = options.list_devices
	device = int(options.audio_device)
	GRAPH = bool(options.graphical)
	# CHANGE THIS TO CORRECT INPUT DEVICE
	# Enable stereo mixing in your sound card
	# to make you sound output an input
	# Use list_devices() to list all your input devices
	if do_list:
		print(list_devices())
		quit()
	if device == -1:
		device = select_device()
	p = pyaudio.PyAudio()
	stream = p.open(format = pyaudio.paInt16,
					channels = 1,
					rate = 44100,
					input = True,
					frames_per_buffer = chunk,
					input_device_index = device)
	
	s = serial.Serial(port=myPort,baudrate=baudrate)
	print("Starting, use Ctrl+C to stop")
	try:
		while True:
			data  = stream.read(chunk)
			rms   = audioop.rms(data, 2)
			# print(rms)
			# print(level)
			level = scale_audio(rms, scale, exponent)
			outstr = (str(int(constrain(level,0,100)*1000))+" \n").encode(encoding='UTF-8')
			for i in range(s.inWaiting()):
				s.read()

			if DEBUG:
				print("{:.2f}".format(level),end="")
				if GRAPH:
					mult = 50
					barLen = int(level*mult)
					print(" " + barLen*"#" + "_"*(mult-barLen) + "|",sep="\t",end="")
				print()

			s.write(outstr)


	except KeyboardInterrupt:
		pass
	finally:
		print("\nStopping")
		stream.close()
		p.terminate()
		sys.exit(0)

if __name__ == '__main__':
	# list_devices()
	main()
main()
#!/usr/bin/env python3
from flexx import app, ui, react
import os
import subprocess
import sys
import time
import signal
import SerialDetector


def get_devices():
	return subprocess.check_output(["python3", "main.py", "-l", "1"]).decode("utf-8").replace("\n", "<br>")


class ScrollBox(ui.Label):
	CSS = """
	.flx-scrollbox {
		overflow-y:scroll;
		background: #e8e8e8;
		border: 1px solid #444;
		margin: 3px;
		height: 100;
	}
	"""


@app.serve
class LightFX_Controller(ui.Widget):

	def set_settings(self):
		while True:
			try:
				with open("settings.txt", "r") as f:
					settings_dict = eval(f.read())
					self.deviceInput.text(settings_dict["-a"])
					self.scaleInput.text(settings_dict["-s"])
					self.exponentInput.text(settings_dict["-e"])
					# self.comPortInput.text(settings_dict["-p"])
					self.debugInput.text(settings_dict["-d"])
					self.chunkInput.text(settings_dict["-c"])
					break
			except:
				with open("settings.txt", "w") as f:
					f.write(str(
							{"-s": "6", "-e": "2.5", "-p": "your_port_here", "-a": "2", "-d": "", "-c": "2048"}))

	def init(self):
		self.serials = []

		# with ui.HBox():
		# self.label = ui.Label(flex=1)
		# help(ui.LineEdit)
		with ui.Panel():
			with ui.HBox():
				with ui.VBox() as test:
					test.size((400, 300))
					self.list = ui.Label(text=get_devices(), flex=1)
					self.consoleOut = ScrollBox(flex=1)
				# with ui.Panel():
				with ui.HBox():

					# print([str(i.split(".")[0]) for i in get_devices().split("\n")])
					with ui.VBox():

						self.scaleLabel = ui.Label(text="Scale:")

						self.expLabel = ui.Label(text="Exponent:")

						self.chunkLabel = ui.Label(text="Chunk size:")

						self.portLabel = ui.Label(text="Port:")

						self.dbgLabel = ui.Label(text="Debug?:")

						self.devLabel = ui.Label(text="Device:")

						self.graphLabel = ui.Label(text="Graph:")

					with ui.VBox():

						self.scaleInput = ui.LineEdit(placeholder_text="scale", flex=0, autocomp=tuple([str(i) for i in range(11)]))

						self.exponentInput = ui.LineEdit(placeholder_text="exponent", flex=0, autocomp=tuple([str(i / 2.0) for i in range(8)]))

						self.chunkInput = ui.LineEdit(placeholder_text="chunk", flex=0, autocomp=tuple([str(int(1024 * i / 2)) for i in range(2, 16)]))

						self.comPortInput = ui.LineEdit(placeholder_text="COM port", flex=0, autocomp=tuple(self.get_serials()))

						self.debugInput = ui.LineEdit(placeholder_text="debug?", flex=0, autocomp=("True", "False"))

						self.deviceInput = ui.LineEdit(placeholder_text="device", flex=0, autocomp=tuple([str(i.split(".")[0]) for i in get_devices().split("\n")]))
						
						self.graphInput = ui.LineEdit(placeholder_text="graph", flex=0, autocomp=("True", "False"))

		with ui.Panel():
			with ui.VBox():
				# self.size = (100,0)
				self.quit = ui.Button(text="Quit", flex=0, size=(0, 100))
				self.stop = ui.Button(text="Stop", flex=0, size=(0, 100))
				self.button = ui.Button(text='Start', flex=0, size=(0, 100))

		self.set_settings()
		# 			self.__dict__.update({str(i):ui.Label(text=str(i),flex=1)})
		try:
			with open("process.dat", "r") as f:
				pid = int(f.read())
			# self.log("Old proces\s found ({}) Killing.".format(pid))
			# os.kill(pid, signal.SIGTERM)
		except (FileNotFoundError, PermissionError):
			self.log("No current process found.")
			self.process = False
		# help(ui.LineEdit)

	def get_time(self):
		return time.strftime("%H:%M:%S")

	def kill_process(self):
		# self.consoleOut.text(self.consoleOut.text() + get_time() + " : Killed process<br>")
		try:
			self.log("Killing old proc ({})".format(self.process.pid))
			self.process.kill()
		except:
			self.log("No process found")

	def log(self, s):
		out = self.get_time() + ": " + s
		print(out)
		self.consoleOut.text(self.consoleOut.text() + out + "<br>")

	def get_serials(self):
		return SerialDetector.serial_ports()

	@react.connect('button.mouse_down')
	def _handle_launch(self, down):
		self.list.text(get_devices())
		args = [
			"-s", self.scaleInput.text(),
			"-e", self.exponentInput.text(),
			"-p", self.comPortInput.text(),
			"-a", self.deviceInput.text(),
			"-d", self.debugInput.text(),
			"-g", self.graphInput.text(),
			"-c", self.chunkInput.text()]
		if down:
			self.kill_process()
			self.log("Started child process.")
			self.process = subprocess.Popen(
				["python3", "main.py", "--graphical", "True"] + args, shell=False)
			self.log("Proc. ID: " + str(self.process.pid))
			with open("process.dat", "w") as f:
				f.write(str(self.process.pid))

	@react.connect("quit.mouse_down")
	def _handle_quit(self, down):
		if down:
			try:
				os.remove("process.dat")
			except FileNotFoundError:
				pass
			self.kill_process()
			sys.exit()

	@react.connect("stop.mouse_down")
	def _handle_stop(self, down):
		if down:
			try:
				os.remove("process.dat")
			except FileNotFoundError:
				pass
			self.kill_process()

# app.serve(LightFX_Controller)
main = app.launch(LightFX_Controller)
# main()
if __name__ == "__main__":
	app.start(port=8080)

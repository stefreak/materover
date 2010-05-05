#!/usr/bin/env python2.6
import pygame
from pygame.locals import * 
from pygame import joystick

import sys
import serial
import threading
import Queue
import time

SERIAL_DEVICE = "/dev/ttyUSB0"
SERIAL_DEBUG = False
SYNCBYTE = 0xff

class SerialThread(threading.Thread):
	def __init__(self, device, queue):
		# queue for communication with main process
		self.queue = queue

		# initialize serial device
		if not SERIAL_DEBUG:
			self.serial = serial.Serial(device)
			self.serial.open()
		else:
			class Serial:
				def write(self, what):
					print repr(what)
			self.serial = Serial()

		# two state variables
		self.state = 0,0
		self.real_state = [0,0]

		# threading.Thread initialization
		threading.Thread.__init__(self)

		self.setDaemon(True)

	def run(self):
		while True:
			# read from queue
			while self.queue.qsize() > 0:
				try:
					self.state = self.queue.get_nowait()
				except Queue.Empty:
					break

			# increment/decrement real_state
			for i in range(2):
				if self.state[i-1] > self.real_state[i-1]:
					self.real_state[i-1] += (self.state[i-1] - self.real_state[i-1])/8+1
				elif self.state[i-1] < self.real_state[i-1]:
					self.real_state[i-1] -= (self.real_state[i-1] - self.state[i-1])/8+1 

			# calculate the data for the arduino
			bytes = [0,0,0,0]
			for i in range(2):
				if self.real_state[i-1] >= 0:
					bytes[2*i-1] = self.real_state[i-1]
				elif self.real_state[i-1] < 0:
					bytes[2*i-2] = abs(self.real_state[i-1])

			# send the data
			self.serial.write(SYNCBYTE)
			for b in bytes:
				self.serial.write(b)

			# sleep
			time.sleep(.1)

class RoverControl:
	def __init__(self):
		print "Initializing..."
		pygame.init() 
		window = pygame.display.set_mode((400, 400))

		self.state = 0,0
		self.queue = Queue.Queue()
		self.thread = SerialThread(SERIAL_DEVICE, self.queue)
		self.thread.start()

		if joystick.get_count() > 0:
			self.joystick = joystick.Joystick(0)
			print "Using the first joystick on your system:"
			print "joystick name: %s" % self.joystick.get_name()
			print "Initializing joystick..."
			self.joystick.init()
		else:
			self.joystick = None

		print "Ready."

		self.loop()

	def change_state(self, motor1, motor2):
		self.state = (motor1, motor2)
		self.queue.put((motor1, motor2))

	def input(self, events):
		for event in events:
			l, r = self.state
			if event.type == QUIT: 
				sys.exit(0)
			elif event.type == KEYUP:
				print "Keyup",
				if event.key == 273:
					print "up"
					self.change_state(l-200, r-200)
				elif event.key == 276:
					print "left"
					self.change_state(l+50, r-50)
				elif event.key == 275:
					print "right"
					self.change_state(l-50, r+50)
				elif event.key == 274:
					print "down"
					self.change_state(l+200, r+200)
			elif event.type == KEYDOWN:
				print "Keydown",
				#print event
				if event.key == 273:
					print "up"
					self.change_state(l+200, r+200)
				elif event.key == 276:
					print "left"
					self.change_state(l-50, r+50)
				elif event.key == 275:
					print "right"
					self.change_state(l+50, r-50)
				elif event.key == 274:
					print "down"
					self.change_state(l-200, r-200)
			elif event.type == JOYAXISMOTION:
				#for a in range(2):
				#self.joystick.get_axis(a)
				#*100/(granularity/2)+(granularity/2)
				print event
			else: 
				#print event
				pass
	
	def loop(self):
		while True: 
			self.input(pygame.event.get())

RoverControl()

import sys
import procgame
import pinproc
from threading import Thread
import random
import string
import time
import locale
import math
import copy
import ctypes
from procgame.events import EventManager
from procgame.dmd import dmd
from pinlib import p, util

try:
	import pygame
	import pygame.locals
except ImportError:
	print "Error importing pygame; ignoring."
	pygame = None

if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
   Py_ssize_t = ctypes.c_int
elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
   Py_ssize_t = ctypes.c_int64
else:
   raise TypeError("Cannot determine type of Py_ssize_t")

PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
PyObject_AsWriteBuffer.restype = ctypes.c_int
PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                  ctypes.POINTER(ctypes.c_void_p),
                                  ctypes.POINTER(Py_ssize_t)]

orange = [
	(0, 0, 0),
	(15, 8, 0),
	(33, 17, 0),
	(51, 25, 0),
	(66, 33, 0),
	(84, 42, 0),
	(102, 51, 0),
	(117, 58, 0),
	(135, 67, 0),
	(153, 76, 0),
	(168, 84, 0),
	(186, 93, 0),
	(204, 102, 0),
	(219, 109, 0),
	(237, 118, 0),
	(255, 127, 0),
]

orange2 = [
	(0, 0, 0, 0),
	(0, 8, 15, 0),
	(0, 17, 33, 0),
	(0, 25, 51, 0),
	(0, 33, 66, 0),
	(0, 42, 84, 0),
	(0, 51, 102, 0),
	(0, 58, 117, 0),
	(0, 67, 135, 0),
	(0, 76, 153, 0),
	(0, 84, 168, 0),
	(0, 93, 186, 0),
	(0, 102, 204, 0),
	(0, 109, 219, 0),
	(0, 118, 237, 0),
	(0, 127, 255, 0)
]

def array(surface):
   buffer_interface = surface.get_buffer()
   address = ctypes.c_void_p()
   size = Py_ssize_t()
   PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
   bytes = (ctypes.c_byte * size.value).from_address(address.value)
   bytes.object = buffer_interface
   return bytes


class Desktop(object):
	"""The :class:`Desktop` class helps manage interaction with the desktop, providing both a windowed
	representation of the DMD, as well as translating keyboard input into pyprocgame events."""

	exit_event_type = 99
	"""Event type sent when Ctrl-C is received."""

	key_map = {}

	screen = None
	""":class:`pygame.Surface` object representing the screen's surface."""
	screen_multiplier = 5

	def __init__(self):
		self.ctrl = 0
		self.i = 0

		if 'pygame' in globals():
			self.setup_window()
		else:
			print 'Desktop init skipping setup_window(); pygame does not appear to be loaded.'
		self.add_key_map(pygame.locals.K_LSHIFT, 3)
		self.add_key_map(pygame.locals.K_RSHIFT, 1)
		self.rects = []
		self.last_frame = dmd.Frame(128, 32)
		for x in xrange(128):
			col = []
			self.rects += [col]
			for y in xrange(32):
				left = x * self.screen_multiplier
				top = y * self.screen_multiplier
				size = self.screen_multiplier
				col += [(pygame.Rect(left, top, size - 1, size - 1), pygame.Rect(left, top, size, size))]

	def add_key_map(self, key, switch_number):
		"""Maps the given *key* to *switch_number*, where *key* is one of the key constants in :mod:`pygame.locals`."""
		self.key_map[key] = switch_number

	def clear_key_map(self):
		"""Empties the key map."""
		self.key_map = {}

	def get_keyboard_events(self):
		"""Asks :mod:`pygame` for recent keyboard events and translates them into an array
		of events similar to what would be returned by :meth:`pinproc.PinPROC.get_events`."""
		key_events = []
		for event in pygame.event.get():
			EventManager.default().post(name=self.event_name_for_pygame_event_type(event.type), object=self, info=event)
			key_event = {}
			if event.type == pygame.locals.KEYDOWN:
				if event.key == pygame.locals.K_RCTRL or event.key == pygame.locals.K_LCTRL:
					self.ctrl = 1
				if event.key == pygame.locals.K_c:
					if self.ctrl == 1:
						key_event['type'] = self.exit_event_type
						key_event['value'] = 'quit'
				elif (event.key == pygame.locals.K_ESCAPE):
					key_event['type'] = self.exit_event_type
					key_event['value'] = 'quit'
				elif event.key in self.key_map:
					sw = p.machine.switch(self.key_map[event.key])
					if sw.type == "NC":
						key_event['type'] = pinproc.EventTypeSwitchOpenDebounced
					else:
						key_event['type'] = pinproc.EventTypeSwitchClosedDebounced
					key_event['value'] = sw.id
			elif event.type == pygame.locals.KEYUP:
				if event.key == pygame.locals.K_RCTRL or event.key == pygame.locals.K_LCTRL:
					self.ctrl = 0
				elif event.key in self.key_map:
					sw = p.machine.switch(self.key_map[event.key])
					if sw.type == "NC":
						key_event['type'] = pinproc.EventTypeSwitchClosedDebounced
					else:
						key_event['type'] = pinproc.EventTypeSwitchOpenDebounced
					key_event['value'] = sw.id
			if len(key_event):
				key_events.append(key_event)
		return key_events


	event_listeners = {}

	def event_name_for_pygame_event_type(self, event_type):
		return 'pygame(%s)' % (event_type)


	def setup_window(self):
		pygame.init()
		self.screen = pygame.display.set_mode((128*self.screen_multiplier, 32*self.screen_multiplier))
		pygame.display.set_caption('Dot Matrix Display')


	def debug_render(self, frame):
		sw = util.Stopwatch()
		updates = self.render(frame)
		elapsed = sw.elapsed() * 1000
		if elapsed > 40:
			print "draw {:2f} {:d}".format(elapsed, updates)

	def render(self, frame):
		updates = []
		for x in xrange(128):
			for y in xrange(32):
				previous = self.last_frame.get_dot(x, y)
				current = frame.get_dot(x, y)
				index = current & 0xf
				if previous != current:
					fill_rect, update_rect = self.rects[x][y]
					updates += [update_rect]
					self.screen.fill(orange[index], fill_rect)
		update_count = len(updates)
		if update_count > 0 and update_count < 4096:
			pygame.display.update(updates)
		elif update_count == 4096:
			pygame.display.update()
		self.last_frame = frame
		return update_count

	draw = render

	def stop(self):
		pygame.quit()

	def __str__(self):
		return '<Desktop pygame>'

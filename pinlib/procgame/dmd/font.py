import os
import json
from procgame.dmd import Animation, Frame
from procgame import config
from procgame import util

# Anchor values are used by Font.draw_in_rect():
AnchorN = 1
AnchorW = 2
AnchorE = 4
AnchorS = 8
AnchorNE = AnchorN | AnchorE
AnchorNW = AnchorN | AnchorW
AnchorSE = AnchorS | AnchorE
AnchorSW = AnchorS | AnchorW
AnchorCenter = 0

class Font(object):
	"""Variable-width bitmap font.

	Fonts can be loaded manually, using :meth:`load`, or with the :func:`font_named` utility function
	which supports searching a font path."""

	char_widths = None
	"""Array of dot widths for each character, 0-indexed from <space>.
	This array is populated by :meth:`load`.  You may alter this array
	in order to update the font and then :meth:`save` it."""

	left = None
	margin_top = 0
	top = 0
	bottom = 0

	#tracking = 0
	#"""Number of dots to adjust the horizontal position between characters, in addition to the last character's width."""

	composite_op = 'copy'
	"""Composite operation used by :meth:`draw` when calling :meth:`~pinproc.DMDBuffer.copy_rect`."""

	def __init__(self, filename=None):
		super(Font, self).__init__()
		self.__anim = Animation()
		self.char_size = None
		self.bitmap = None
		if filename != None:
			self.load(filename)

	def load(self, filename):
		"""Loads the font from a ``.dmd`` file (see :meth:`Animation.load`).
		Fonts are stored in .dmd files with frame 0 containing the bitmap data
		and frame 1 containing the character widths.  96 characters (32..127,
		ASCII printables) are stored in a 10x10 grid, starting with space (``' '``)
		in the upper left at 0, 0.  The character widths are stored in the second frame
		within the 'raw' bitmap data in bytes 0-95.
		"""
		self.__anim.load(filename)
		if self.__anim.width != self.__anim.height:
			raise ValueError, "Width != height!"
		root, ext = os.path.splitext(filename)
		metrics_filename = root + ".metrics.json"
		self.metrics = None
		left = 0
		if os.path.exists(metrics_filename):
			with open(metrics_filename) as fp:
				self.metrics = json.load(fp)
			left = self.metrics.get("left", 0)
			self.top = self.metrics.get("top", 0)
			self.margin_top = self.metrics.get("margin_top", 0)
			self.bottom = self.metrics.get("bottom", 0)
		elif len(self.__anim.frames) == 1:
			# We allow 1 frame for handmade fonts.
			# This is so that they can be loaded as a basic bitmap, have their char widths modified, and then be saved.
			print "Font animation file %s has 1 frame; adding one" % (filename)
			self.__anim.frames += [Frame(self.__anim.width, self.__anim.height)]
		elif len(self.__anim.frames) != 2:
			raise ValueError, "Expected 2 frames: %d" % (len(self.__anim.frames))
		self.char_size = self.__anim.width / 10
		self.bitmap = self.__anim.frames[0]

		# FIXME: Create a separate bitmap for each possible color. This makes
		# rendering fast, but could be improved
		self.bitmaps = {}
		self.bitmaps[0xf] = self.bitmap
		for color in xrange(1, 0xf):
			#print color
			width = self.bitmap.width
			height = self.bitmap.height
			self.bitmaps[color] = Frame(width, height)
			bitmap = self.bitmaps[color]
			fill = Frame(width, height)
			sub_color = 0xf - color
			fill.fill_rect(0, 0, width, height, sub_color)
			Frame.copy_rect(bitmap, 0, 0, self.bitmap, 0, 0, width, height)
			Frame.copy_rect(bitmap, 0, 0, fill, 0, 0, width, height, "sub")

			"""
			for x in xrange(self.bitmap.width):
				for y in xrange(self.bitmap.height):
					dot = self.bitmap.get_dot(x, y) - (0xf - color)
					if dot > 0:
						self.bitmaps[color].set_dot(x, y, dot)
			"""

		self.char_widths = []
		self.left = []
		if not self.metrics:
			for i in xrange(95):
				self.char_widths += [self.__anim.frames[1].get_dot(i%self.__anim.width, i/self.__anim.width)]
				self.left += [0]
		else:
			overrides = self.metrics.get("left_override", {})
			for i in xrange(95):
				self.char_widths += [self.metrics["widths"][i][1]]
				ch = chr(ord(' ') + i)
				self.left += [overrides.get(ch, left)]
		return self

	def save(self, filename):
		"""Save the font to the given path."""
		out = Animation()
		out.width = self.__anim.width
		out.height = self.__anim.height
		out.frames = [self.bitmap, Frame(out.width, out.height)]
		for i in range(96):
			out.frames[1].set_dot(i%self.__anim.width, i/self.__anim.width, self.char_widths[i])
		out.save(filename)

	def char_metrics(self, ch):
		offset = ord(ch) - ord(' ')
		if offset < 0 or offset >= 96:
			offset = ord(' ')
		x = self.char_size * (offset % 10)
		y = self.char_size * (offset / 10)
		width = self.char_widths[offset]
		if width == 0 and ch.islower():
			return self.char_metrics(ch.upper())
		return (ch, x, y, self.char_widths[offset], self.left[offset])

	def chars(self):
		result = []
		for ascii_value, width in enumerate(self.char_widths, ord(" ")):
			if width > 0:
				result += [chr(ascii_value)]
		return result

	def draw(self, frame, text, x, y, color=0xf, composite_op="copy", tracking=1):
		"""Uses this font's characters to draw the given string at the given position."""
		for ch in text:
			ch, char_x, char_y, width, left = self.char_metrics(ch)
			Frame.copy_rect(dst=frame, dst_x=x, dst_y=y + self.margin_top, src=self.bitmaps[color], src_x=char_x + left, src_y=char_y + self.top, width=width, height=self.char_size - self.top - self.bottom + self.margin_top, op=composite_op)
			x += width + tracking
		return x

	def size(self, text, tracking=1):
		"""Returns a tuple of the width and height of this text as rendered with this font."""
		x = 0
		for ch in text:
			ch, char_x, char_y, width, left = self.char_metrics(ch)
			x += width + tracking
		x = max(x - tracking, 0)
		return (x, self.char_size - self.top - self.bottom + self.margin_top)

	def draw_in_rect(self, frame, text, rect=(0,0,128,32), anchor=AnchorCenter):
		"""Draw *text* on *frame* within the given *rect*, aligned in accordance with *anchor*.

		*rect* is a tuple of length 4: (origin_x, origin_y, height, width). 0,0 is in the upper left (NW) corner.

		*anchor* is one of:
		:attr:`~procgame.dmd.AnchorN`,
		:attr:`~procgame.dmd.AnchorE`,
		:attr:`~procgame.dmd.AnchorS`,
		:attr:`~procgame.dmd.AnchorW`,
		:attr:`~procgame.dmd.AnchorNE`,
		:attr:`~procgame.dmd.AnchorNW`,
		:attr:`~procgame.dmd.AnchorSE`,
		:attr:`~procgame.dmd.AnchorSW`, or
		:attr:`~procgame.dmd.AnchorCenter` (the default).
		"""
		origin_x, origin_y, width, height = rect
		text_width, text_height = self.size(text)
		x = 0
		y = 0

		# print "Size: %d x %d" % (text_height)

		if anchor & AnchorN:
			y = origin_y
		elif anchor & AnchorS:
			y = origin_y + (height - text_height)
		else:
			y = origin_y + (height/2.0 - text_height/2.0)

		if anchor & AnchorW:
			x = origin_x
		elif anchor & AnchorE:
			x = origin_x + (width - text_width)
		else:
			x = origin_x + (width/2.0 - text_width/2.0)

		self.draw(frame=frame, text=text, x=x, y=y)

font_path = []
"""Array of paths that will be searched by :meth:`~procgame.dmd.font_named` to locate fonts.

When this module is initialized the pyprocgame global configuration (:attr:`procgame.config.values`)
``font_path`` key path is used to initialize this array."""

def init_font_path():
    global font_path
    try:
        value = config.value_for_key_path('font_path')
        if issubclass(type(value), list):
            font_path.extend(map(os.path.expanduser, value))
        elif issubclass(type(value), str):
            font_path.append(os.path.expanduser(value))
        elif value == None:
            print('WARNING no font_path set in %s!' % (config.path))
        else:
            print('ERROR loading font_path from %s; type is %s but should be list or str.' % (config.path, type(value)))
            sys.exit(1)
    except ValueError, e:
        #print e
        pass

init_font_path()


__font_cache = {}
def font_named(name):
	"""Searches the :attr:`font_path` for a font file of the given name and returns an instance of :class:`Font` if it exists."""
	if name in __font_cache:
		return __font_cache[name]
	path = util.find_file_in_path(name, font_path)
	if path:
		import dmd # have to do this to get dmd.Font to work below... odd.
		font = Font(path)
		__font_cache[name] = font
		return font
	else:
		raise ValueError, 'Font named "%s" not found; font_path=%s.  Have you configured font_path in config.json?' % (name, font_path)

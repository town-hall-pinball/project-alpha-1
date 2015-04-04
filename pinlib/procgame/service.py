import os
import json

from game import Mode
from dmd import TextLayer, GroupedLayer

class ServiceModeSkeleton(Mode):
	"""Service Mode List base class."""
	def __init__(self, game, priority, font):
		super(ServiceModeSkeleton, self).__init__(game, priority)
		self.name = ""
		self.title_layer = TextLayer(1, 1, font, "left")
		self.item_layer = TextLayer(128/2, 12, font, "center")
		self.instruction_layer = TextLayer(1, 25, font, "left")
		self.layer = GroupedLayer(128, 32, [self.title_layer, self.item_layer, self.instruction_layer])
		self.no_exit_switch = game.machine_type == 'sternWhitestar'

	def mode_started(self):
		self.title_layer.set_text(str(self.name))
		self.game.sound.play('service_enter')

	def mode_stopped(self):
		self.game.sound.play('service_exit')

	def disable(self):
		pass

	def sw_serviceDown_active(self, sw):
		if self.game.switches.serviceEnter.is_active():
			self.game.modes.remove(self)
			return True

	def sw_serviceExit_active(self, sw):
		self.game.modes.remove(self)
		return True

class ServiceModeList(ServiceModeSkeleton):
	"""Service Mode List base class."""
	def __init__(self, game, priority, font):
		super(ServiceModeList, self).__init__(game, priority, font)
		self.items = []

	def mode_started(self):
		super(ServiceModeList, self).mode_started()

		self.iterator = 0
		self.change_item()

	def change_item(self):
		ctr = 0
                for item in self.items:
			if (ctr == self.iterator):
				self.item = item
			ctr += 1
		self.max = ctr - 1
		self.item_layer.set_text(self.item.name)

	def sw_serviceUp_active(self,sw):
		if self.game.switches.serviceEnter.is_inactive():
			self.item.disable()
			if (self.iterator < self.max):
				self.iterator += 1
			else:
				self.iterator = 0
			self.game.sound.play('service_next')
			self.change_item()
		return True

	def sw_serviceDown_active(self,sw):
		if self.game.switches.serviceEnter.is_inactive():
			self.item.disable()
			if (self.iterator > 0):
				self.iterator -= 1
			else:
				self.iterator = self.max
			self.game.sound.play('service_previous')
			self.change_item()
		elif self.no_exit_switch:
			self.exit()
		return True

	def sw_serviceEnter_active(self,sw):
		self.game.modes.add(self.item)
		return True

	def exit(self):
		self.item.disable()
		self.game.modes.remove(self)
		return True

class ServiceMode(ServiceModeList):
	"""Service Mode."""
	def __init__(self, game, priority, font, config_file, extra_tests=[]):
		super(ServiceMode, self).__init__(game, priority,font)
		#self.title_layer.set_text('Service Mode')
		self.items = []
		self.name = 'SERVICE MODE'

		self.menu = None
		if os.path.exists("config/service_menu.json"):
			with open("config/service_menu.json") as fp:
				self.menu = json.load(fp)

		if self.menu:
			if self.menu["Settings"] :
				self.settings = Settings(self.game, self.priority+1, font, 'SETTINGS', self.menu["Settings"])
				self.items.append(self.settings)
			if self.menu["Statistics"]:
				self.statistics = Statistics(self.game, self.priority+1, font, 'STATISTICS', self.menu["Statistics"])
				self.items.append(self.statistics)
		self.tests = Tests(self.game, self.priority+1, font, extra_tests)
		self.items += [self.tests]

class Tests(ServiceModeList):
	"""Service Mode."""
	def __init__(self, game, priority, font, extra_tests=[]):
		super(Tests, self).__init__(game, priority,font)
		#self.title_layer.set_text('Tests')
		self.name = 'TESTS'
		self.lamp_test = LampTest(self.game, self.priority+1, font)
		self.coil_test = CoilTest(self.game, self.priority+1, font)
		self.switch_test = SwitchTest(self.game, self.priority+1, font)
		self.items = [self.switch_test, self.lamp_test, self.coil_test]
		for test in extra_tests:
			self.items.append(test)

class LampTest(ServiceModeList):
	"""Lamp Test"""
	def __init__(self, game, priority, font):
		super(LampTest, self).__init__(game, priority,font)
		self.name = "Lamp Test"
		self.items = self.game.lamps

	def change_item(self):
		super(LampTest, self).change_item()
		self.item.schedule(schedule=0x00ff00ff, cycle_seconds=0, now=True)

	def sw_serviceEnter_active(self,sw):
		return True


class CoilTest(ServiceModeList):
	"""Coil Test"""
	def __init__(self, game, priority, font):
		super(CoilTest, self).__init__(game, priority, font)
		self.name = "Coil Test"
		self.title_layer.set_text('Coil Test - Enter btn: mode')
		self.instruction_layer.set_text('Pulse with start button')
		self.items = self.game.coils

	def mode_started(self):
		super(CoilTest, self).mode_started()
		self.action = 'manual'
		if self.game.lamps.has_key('startButton'): self.game.lamps.startButton.schedule(schedule=0xff00ff00, cycle_seconds=0, now=False)
		self.delay(name='auto', event_type=None, delay=2.0, handler=self.process_auto)

	def process_auto(self):
		if (self.action == 'auto'):
			self.item.pulse(20)
		self.delay(name='auto', event_type=None, delay=2.0, handler=self.process_auto)


	def sw_serviceEnter_active(self,sw):
		if (self.action == 'manual'):
			self.action = 'auto'
			if self.game.lamps.has_key('startButton'): self.game.lamps.startButton.disable()
			self.instruction_layer.set_text('Auto pulse')
		elif (self.action == 'auto'):
			self.action = 'manual'
			if self.game.lamps.has_key('startButton'): self.game.lamps.startButton.schedule(schedule=0xff00ff00, cycle_seconds=0, now=False)
			self.instruction_layer.set_text('Pulse with start button')
		return True

	def sw_startButton_active(self,sw):
		if (self.action == 'manual'):
			self.item.pulse(20)
		return True

class SwitchTest(ServiceModeSkeleton):
	"""Switch Test"""
	def __init__(self, game, priority, font):
		super(SwitchTest, self).__init__(game, priority,font)
		self.name = "Switch Test"
		for switch in self.game.switches:
			if self.game.machine_type == 'sternWhitestar':
				add_handler = 1
			elif switch != self.game.switches.serviceExit:
				add_handler = 1
			else:
				add_handler = 0
			if add_handler:
				self.add_switch_handler(name=switch.name, event_type='inactive', delay=None, handler=self.switch_handler)
				self.add_switch_handler(name=switch.name, event_type='active', delay=None, handler=self.switch_handler)

	def switch_handler(self, sw):
		if (sw.state):
			self.game.sound.play('service_switch_edge')
		self.item_layer.set_text(sw.name + ' - ' + str(sw.state))
		return True

	def sw_serviceEnter_active(self,sw):
		return True

class Statistics(ServiceModeList):
	"""Service Mode."""
	def __init__(self, game, priority, font, name, itemlist):
		super(Statistics, self).__init__(game, priority,font)
		#self.title_layer.set_text('Settings')
		self.name = name
		self.items = []
		for section, item in itemlist.items():
			self.items.append( StatsDisplay( self.game, priority + 1, font, str(section).upper(),item ))

class StatsDisplay(ServiceModeList):
	"""Coil Test"""
	def __init__(self, game, priority, font, name, itemlist):
		super(StatsDisplay, self).__init__(game, priority, font)
		self.name = name
		self.value_layer = TextLayer(128/2, 22, font, "center")
		self.items = []
		for item in itemlist:
			value = game.data[item["key"]]
			self.items.append( StatsItem(str(item["name"]).upper(), value) )
		self.layer = GroupedLayer(128, 32, [self.title_layer, self.item_layer, self.value_layer])

	def mode_started(self):
		super(StatsDisplay, self).mode_started()

	def change_item(self):
		super(StatsDisplay, self).change_item()
		try:
			self.item.score
		except:
			self.item.score = 'None'

		if self.item.score == 'None':
			self.value_layer.set_text(str(self.item.value))
		else:
			self.value_layer.set_text(self.item.value + ": " + str(self.item.score))

	def sw_serviceEnter_active(self, sw):
		return True

class StatsItem:
	"""Service Mode."""
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def disable(self):
		pass

class HighScoreItem:
	"""Service Mode."""
	def __init__(self, name, value, score):
		self.name = name
		self.value = value
		self.score = score

	def disable(self):
		pass


class SwitchTest(ServiceModeSkeleton):
	"""Switch Test"""
	def __init__(self, game, priority, font):
		super(SwitchTest, self).__init__(game, priority,font)
		self.name = "Switch Test"
		for switch in self.game.switches:
			if self.game.machine_type == 'sternWhitestar':
				add_handler = 1
			elif switch != self.game.switches.serviceExit:
				add_handler = 1
			else:
				add_handler = 0
			if add_handler:
				self.add_switch_handler(name=switch.name, event_type='inactive', delay=None, handler=self.switch_handler)
				self.add_switch_handler(name=switch.name, event_type='active', delay=None, handler=self.switch_handler)

	def switch_handler(self, sw):
		if (sw.state):
			self.game.sound.play('service_switch_edge')
		self.item_layer.set_text(sw.name + ' - ' + str(sw.state))
		return True

	def sw_serviceEnter_active(self,sw):
		return True


class Settings(ServiceModeList):
	"""Service Mode."""
	def __init__(self, game, priority, font, name, itemlist):
		super(Settings, self).__init__(game, priority,font)
		#self.title_layer.set_text('Settings')
		self.name = name
		self.items = []
		self.font = font
		for section in itemlist.iterkeys():
			self.items.append( SettingsEditor( self.game, priority + 1, font, str(section),itemlist[section] ))

class SettingsEditor(ServiceModeList):
	"""Service Mode."""
	def __init__(self, game, priority, font, name, itemlist):
		super(SettingsEditor, self).__init__(game, priority, font)
		self.title_layer = TextLayer(1, 1, font, "left")
		self.item_layer = TextLayer(128/2, 12, font, "center")
		self.instruction_layer = TextLayer(1, 25, font, "left")
		self.no_exit_switch = game.machine_type == 'sternWhitestar'
		#self.title_layer.set_text('Settings')
		self.name = name.upper()
		self.items = []
		self.value_layer = TextLayer(128/2, 19, font, "center")
		self.layer = GroupedLayer(128, 32, [self.title_layer, self.item_layer, self.value_layer, self.instruction_layer])
		for item in itemlist:
			#self.items.append( EditItem(str(item), itemlist[item]['options'], itemlist[item]['value'] ) )
			if 'increments' in item:
				num_options = (itemlist[item]['options'][1]-itemlist[item]['options'][0]) / itemlist[item]['increments']
				option_list = []
				for i in range(0,num_options):
					option_list.append(itemlist[item]['options'][0] + (i * itemlist[item]['increments']))
				self.items.append( EditItem(str(item), option_list, self.game.user_settings[self.name][item]) )
			else:
				values = item.get("values", None)
				self.items.append( EditItem(str(item["name"]), item['options'], values, item["key"], self.game.settings[item["key"]]) )
		self.state = 'nav'
		self.stop_blinking = True
		self.item = self.items[0]
		value = self.item.value
		if self.item.values:
			self.option_index = self.item.values.index(value)
		else:
			self.option_index = self.item.options.index(value)
		self.value_layer.set_text(str(self.item.options[self.option_index]))

	def mode_started(self):
		super(SettingsEditor, self).mode_started()

	def mode_stopped(self):
		self.game.sound.play('service_exit')

	def sw_serviceEnter_active(self, sw):
		if not self.no_exit_switch:
			self.process_enter()
		return True

	def process_enter(self):
		if self.state == 'nav':
			self.state = 'edit'
			self.blink = True
			self.stop_blinking = False
			self.delay(name='blink', event_type=None, delay=.3, handler=self.blinker)
		else:
			self.state = 'nav'
			self.instruction_layer.set_text("SAVED")
			self.delay(name='change_complete', event_type=None, delay=1, handler=self.change_complete)
			self.game.sound.play('service_save')

			if self.item.values:
				self.game.settings[self.item.key] = self.item.values[self.option_index]
			else:
				self.game.settings[self.item.key] = self.item.value
			#self.game.user_settings[self.name][self.item.name]=self.item.value
			self.stop_blinking = True
			self.game.save_settings()

	def sw_serviceExit_active(self, sw):
		self.process_exit()
		return True

	def process_exit(self):
		if self.state == 'nav':
			self.game.modes.remove(self)
		else:
			self.state = 'nav'
			self.item.value = self.game.settings[self.item.key]
			self.value_layer.set_text(str(self.item.value))
			self.stop_blinking = True
			self.game.sound.play('service_cancel')
			self.instruction_layer.set_text("CANCELLED")
			self.delay(name='change_complete', event_type=None, delay=1, handler=self.change_complete)

	def sw_serviceUp_active(self, sw):
		if self.game.switches.serviceEnter.is_inactive():
			self.process_up()

		else:
			self.process_enter()
		return True

	def process_up(self):
		if self.state == 'nav':
			self.item.disable()
			if (self.iterator < self.max):
				self.iterator += 1
			else:
				self.iterator = 0
			self.game.sound.play('service_next')
			self.change_item()
		else:
			if self.option_index < (len(self.item.options) - 1):
				self.option_index += 1
			else:
				self.option_index = 0
			self.item.value = self.item.options[self.option_index]
			self.value_layer.set_text(str(self.item.value))


	def sw_serviceDown_active(self, sw):
		if self.game.switches.serviceEnter.is_inactive():
			self.process_down()
		else:
			self.process_exit()
		return True

	def process_down(self):
		if self.state == 'nav':
			self.item.disable()
			if (self.iterator > 0):
				self.iterator -= 1
			else:
				self.iterator = self.max - 1
			self.game.sound.play('service_previous')
			self.change_item()
		else:
			if self.option_index > 0:
				self.option_index -= 1
			else:
				self.option_index = len(self.item.options) - 1
			self.item.value = self.item.options[self.option_index]
			self.value_layer.set_text(str(self.item.value))

	def change_item(self):
		ctr = 0
                for item in self.items:
			if ctr == self.iterator:
				self.item = item
			ctr += 1
		self.max = ctr - 1
		self.item_layer.set_text(self.item.name)
		value = self.item.value
		if self.item.values:
			self.option_index = self.item.values.index(value)
		else:
			self.option_index = self.item.options.index(value)
		self.value_layer.set_text(str(self.item.options[self.option_index]))

	def disable(self):
		pass

	def blinker(self):
		if self.item.values:
			str_value = self.item.options[self.option_index]
		else:
			str_value = str(self.item.value)

		if self.blink:
			self.value_layer.set_text(str_value)
			self.blink = False
		else:
			self.value_layer.set_text("")
			self.blink = True
		if not self.stop_blinking:
			self.delay(name='blink', event_type=None, delay=.3, handler=self.blinker)
		else:
			self.value_layer.set_text(str_value)

	def change_complete(self):
		self.instruction_layer.set_text("")

class EditItem:
	"""Service Mode."""
	def __init__(self, name, options, values, key, value):
		self.name = name.upper()
		self.options = options
		self.values = values
		self.key = key
		self.value = value

	def __str__(self):
		return "key: {}, value: {}, name: {}, options: {}".format(
			self.key, self.value, self.name, self.options)

	def disable(self):
		pass

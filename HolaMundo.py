import sublime
import sublime_plugin

import os

from pprint import pprint

from magento_2.lib.getting_settings import Settings

class SaludaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		pprint(dir(sublime.active_window()))
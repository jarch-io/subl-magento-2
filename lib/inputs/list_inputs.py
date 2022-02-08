import sublime_plugin

import os

from magento_2.lib.getting_settings import Settings

class CompanyInputHandler(sublime_plugin.ListInputHandler):
	def placeholder(self):
		return "Select a company"

	def list_items(self):
		settings = Settings()
		options = []

		for company in settings.getSetting('company'):
			options.append(company['name'])

		return options

class ScopeInputHandler(sublime_plugin.ListInputHandler):
	def placeholder(self):
		return "Select a scope"

	def list_items(self):
		return ['adminhtml', 'frontend']

class ModuleInputHandler(sublime_plugin.ListInputHandler):
	vendor = ''
	projectDirectory = ''

	def setVendor(self, vendor):
		self.vendor = vendor

	def setProjectDirectory(self, projectDirectory):
		self.projectDirectory = projectDirectory

	def placeholder(self):
		return "Select a module"

	def list_items(self):
		settings = Settings()

		delimiter = settings.getSetting('delimiter_path')
		appCodePath = settings.getSetting('app_code_path')

		modulePath = self.projectDirectory + delimiter + appCodePath + delimiter + self.vendor

		moduleList = []

		for directory in os.listdir(modulePath):
			moduleList.append(directory)

		return moduleList

class RouteInputHandler(sublime_plugin.TextInputHandler):
	def placeholder(self):
		return "Write a route"
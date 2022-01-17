import sublime
import sublime_plugin

import os

from pprint import pprint

from magento_2.lib.getting_settings import Settings

from magento_2.lib.inputs.list_inputs import CompanyInputHandler as CompanyMasterInputHandler

class SaludaCommand(sublime_plugin.TextCommand):
	def run(self, edit, company, module, scope, name):
		sublime.status_message("%s -- %s -- %s -- %s" % (company, module, scope, name))

	def input(self, args):
		company = CompanyInputHandler()
		company.setView(self.view)
		return company

class NameInputHandler(sublime_plugin.TextInputHandler):
	def placeholder(self):
		return "Write a controller name"

	def preview(self, text):
		if text == '':
			text = 'Index'

		return text

class ScopeInputHandler(sublime_plugin.ListInputHandler):

	def placeholder(self):
		return "Select a scope"

	def list_items(self):
		return ['adminhtml', 'frontend']

	def next_input(self, args):
		return NameInputHandler()

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

	def next_input(self, args):
		return ScopeInputHandler()


class CompanyInputHandler(CompanyMasterInputHandler):
	view = None

	def setView(self, view):
		self.view = view

	def next_input(self, args):
		module = ModuleInputHandler()
		module.setVendor(args.get('company'))
		module.setProjectDirectory(self.view.window().extract_variables()['project_path'])
		return module
	
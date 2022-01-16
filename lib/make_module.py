import sublime
import sublime_plugin

import os

from magento_2.lib.getting_settings import Settings

from magento_2.templates.file_php import registration as registrationTpl
from magento_2.templates.file_xml import module as moduleTpl

class CompanyInputHandler(sublime_plugin.ListInputHandler):
	def placeholder(self):
		return "Select a company"

	def list_items(self):
		settings = Settings()
		options = []

		for company in settings.getSetting('company'):
			options.append(company['name'])

		return options

	def next_input(self, args):
		return ModuleInputHandler()

class ModuleInputHandler(sublime_plugin.TextInputHandler):
	def placeholder(self):
		return "Write a module name"

class MakeModuleM2Command(sublime_plugin.TextCommand):

	moduleName = ''
	vendorName = ''
	copyrightFormat = ''

	settings = None

	def input(self, args):
		return CompanyInputHandler()

	def run(self, edit, company, module):
		self.settings = Settings()
		self.vendorName = company
		self.moduleName = module

		companies = self.settings.getSetting('company')

		for company in companies:
		 	if self.vendorName == company['name']:
		 		self.copyrightFormat = company['copyright_format'].format(vendor = self.vendorName)
		 		break

		if self.vendorName != '' and self.moduleName != '':
			self.generateModule()
		else:
			sublime.status_message("Module has not been created")

	def generateModule(self):
		moduleNew = self.vendorName + '_' + self.moduleName
		
		varsProject = self.view.window().extract_variables()
		currentDirectory = varsProject['project_path']
		delimiter = self.settings.getSetting('delimiter_path')
		appCodePath = self.settings.getSetting('app_code_path')

		moduleDir = currentDirectory + delimiter + appCodePath + delimiter + self.vendorName + delimiter + self.moduleName
		moduleDirEtc = moduleDir + delimiter + "etc"
		fileModuleXml = moduleDirEtc + delimiter + 'module.xml'
		fileModuleRegistration = moduleDir + delimiter + 'registration.php'
		
		os.makedirs(moduleDirEtc, exist_ok = True)

		if not os.path.exists(fileModuleXml):
			with open(fileModuleXml, 'w') as file:
					content = moduleTpl.format(module = moduleNew, copyright = self.copyrightFormat)

					file.writelines(content)
					file.close

		if not os.path.exists(fileModuleRegistration):
			with open(fileModuleRegistration, 'w') as file:
					content = registrationTpl.format(module = moduleNew, copyright = self.copyrightFormat)

					file.writelines(content)
					file.close

		sublime.active_window().open_file(fileModuleXml)
		sublime.active_window().open_file(fileModuleRegistration)

		sublime.status_message("Module %s_%s has been created" % (self.vendorName, self.moduleName))
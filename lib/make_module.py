import sublime
import sublime_plugin

import os

from magento_2.lib.getting_settings import Settings

from magento_2.templates.file_php import registration as registrationTpl
from magento_2.templates.file_xml import module as moduleTpl

class MakeModuleM2Command(sublime_plugin.TextCommand):

	moduleName = ''
	vendorName = ''
	copyrightFormat = ''

	settings = None

	def run(self, edit):
		self.settings = Settings()
		companies = self.settings.getSetting('company')
		
		options = []

		for company in companies:
		 	options.append(company['name'])

		self.view.window().show_quick_panel(options, on_select = self.selectCompany)

	def selectCompany(self, index):
		if index != -1:
			company = self.settings.getSetting('company')[index]
			self.vendorName = company['name']
			self.copyrightFormat = company['copyright_format'].format(vendor = self.vendorName)
			self.view.window().show_input_panel('Module Name', 'Module', self.getModuleName, None, None)

	def getModuleName(self, module):
		if module != '':
			self.moduleName = module
			self.generateModule()

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
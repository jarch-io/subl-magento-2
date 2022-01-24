import sublime
import sublime_plugin

import os

from pprint import pprint

from magento_2.lib.getting_settings import Settings

from magento_2.lib.inputs.list_inputs import CompanyInputHandler as CompanyMasterInputHandler

class GeneratorController():
	scope = ''
	route = ''
	controller = ''
	module = ''
	vendor = ''

	def setScope(self, scope):
		self.scope = scope

	def setRoute(self, route):
		self.route = route

	def setController(self, controller):
		self.controller = controller

	def setModule(self, module):
		self.module = module

	def setVendor(self, vendor):
		self.vendor = vendor

	def getController(self):
		return self.controller.split(sep = '/')

	def getControllerClass(self):
		controllerArray = self.getController()
		controllerArray.pop()
		
		return '/'.join(controllerArray)

	def getControllerPath(self):
		controllerArray = self.getController()
		controllerArray.pop()

		return '_'.join(controllerArray).lower()

	def getActionClass(self):
		return self.getController().pop()

	def getFiles(self):
		return [
			"Block/{scope}{controller}/{action}.php".format(scope = 'Adminhtml/' if self.scope == 'adminhtml' else '', controller = self.getControllerClass(), action = self.getActionClass()),
			"Controller/{scope}{controller}/{action}.php".format(scope = 'Adminhtml/' if self.scope == 'adminhtml' else '', controller = self.getControllerClass(), action = self.getActionClass()),
			"etc/{scope}/routes.xml".format(scope = self.scope.lower()),
			"view/{scope}/layout/{route}_{controller}_{action}.xml".format(scope = self.scope.lower(), route = self.route.lower(), action = self.getActionClass().lower(), controller = self.getControllerPath().lower()),
			"view/{scope}/template/{controller}/{action}.phtml".format(scope = self.scope.lower(), route = self.route.lower(), action = self.getActionClass().lower(), controller = self.getControllerClass().lower())
		]

	def formatHtml(self):
		commonCss = """
			<style>
				ul {
					padding-left: 10px;
					padding-right: 0px;
					padding-top: 0px;
					padding-bottom: 0px;

					margin: 0px;

					li {
						list-style-type: square;
					}
				}
			</style>
		"""

		htmlPath = []

		for file in self.getFiles():
			fileArray = file.split(sep = '/')
			htmlString = ""

			for idx, part in enumerate(fileArray):
				htmlString += "<li>{}".format(part + ('<ul>' if idx < len(fileArray) - 1 else '</li>'))

			htmlString += "".join(["</ul></li>" for x in range(len(fileArray) - 1)])

			htmlPath.append(htmlString)
		
		return sublime.Html("""
			<html>
				<body>
					{cssStyle}
					<div>
						<code>Access from https://yourhost.com/{route}/{controllerPath}/{action}</code>
					</div>
					<ul>
						{htmlParse}
					</ul>
				</body>
			</html>
		""".format(cssStyle = commonCss, route = self.route.lower(), controllerPath = self.getControllerPath(), action = self.getControllerClass().lower(), htmlParse = "".join(htmlPath)))

generatorController = GeneratorController()

class SaludaCommand(sublime_plugin.TextCommand):
	def run(self, edit, company, module, scope, route, name):
		pprint(generatorController.getFiles())
		sublime.status_message("%s -- %s -- %s -- %s" % (company, module, scope, name))

	def input(self, args):
		company = CompanyInputHandler()
		company.setView(self.view)
		return company

class NameInputHandler(sublime_plugin.TextInputHandler):
	def placeholder(self):
		return "Write a controller name"

	def preview(self, text):
		textArray = []

		if text != '':
			textArray = text.split(sep = '/')

		if len(textArray) == 0:
			textArray.append('Index')

		if len(textArray) == 1:
			textArray.append('Index')

		generatorController.setController('/'.join(textArray))

		return generatorController.formatHtml()

class RouteInputHandler(sublime_plugin.TextInputHandler):
	def placeholder(self):
		return "Write a route"

	def next_input(self, args):
		generatorController.setRoute(args.get('route'))
		return NameInputHandler()

class ScopeInputHandler(sublime_plugin.ListInputHandler):

	def placeholder(self):
		return "Select a scope"

	def list_items(self):
		return ['adminhtml', 'frontend']

	def next_input(self, args):
		generatorController.setScope(args.get('scope'))
		return RouteInputHandler()

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
		generatorController.setModule(args.get('module'))
		return ScopeInputHandler()


class CompanyInputHandler(CompanyMasterInputHandler):
	view = None

	def setView(self, view):
		self.view = view

	def next_input(self, args):
		module = ModuleInputHandler()
		module.setVendor(args.get('company'))
		module.setProjectDirectory(self.view.window().extract_variables()['project_path'])

		generatorController.setVendor(args.get('company'))

		return module
	
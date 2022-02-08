import sublime
import sublime_plugin

import os

from magento_2.lib.getting_settings import Settings
from magento_2.lib.inputs.list_inputs import CompanyInputHandler as CompanyMasterInputHandler, ScopeInputHandler as ScopeMasterInputHandler, ModuleInputHandler as ModuleMasterInputHandler, RouteInputHandler as RouteMasterInputHandler

from magento_2.templates.file_php import controllerController as controllerControllerTpl, controllerBlock as controllerBlockTpl, controllerTemplate as controllerTemplateTpl
from magento_2.templates.file_xml import controllerRoutes as controllerRoutesTpl, controllerLayout as controllerLayoutTpl

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
		return {
			'block' : "Block/{scope}{controller}/{action}.php".format(scope = 'Adminhtml/' if self.scope == 'adminhtml' else '', controller = self.getControllerClass(), action = self.getActionClass()),
			'controller' : "Controller/{scope}{controller}/{action}.php".format(scope = 'Adminhtml/' if self.scope == 'adminhtml' else '', controller = self.getControllerClass(), action = self.getActionClass()),
			'route' : "etc/{scope}/routes.xml".format(scope = self.scope.lower()),
			'layout' : "view/{scope}/layout/{route}_{controller}_{action}.xml".format(scope = self.scope.lower(), route = self.route.lower(), action = self.getActionClass().lower(), controller = self.getControllerPath().lower()),
			'view' : "view/{scope}/templates/{controller}/{action}.phtml".format(scope = self.scope.lower(), route = self.route.lower(), action = self.getActionClass().lower(), controller = self.getControllerClass().lower())
		}

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
		files = self.getFiles()
		for idx in files:
			file = files[idx]
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

class ScopeInputHandler(ScopeMasterInputHandler):
	def next_input(self, args):
		generatorController.setScope(args.get('scope'))
		return RouteInputHandler()

class ModuleInputHandler(ModuleMasterInputHandler):
	def next_input(self, args):
		generatorController.setModule(args.get('module'))
		return ScopeInputHandler()

class RouteInputHandler(sublime_plugin.TextInputHandler):
	def placeholder(self):
		return "Write a route"
		
	def next_input(self, args):
		generatorController.setRoute(args.get('route'))
		return NameInputHandler()

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

class MakeControllerM2Command(sublime_plugin.TextCommand):
	def run(self, edit, company, module, scope, route, name):
		settings = Settings()

		varsProject = self.view.window().extract_variables()
		currentDirectory = varsProject['project_path']
		delimiter = settings.getSetting('delimiter_path')
		appCodePath = settings.getSetting('app_code_path')

		copyrightFormat = settings.getCopyright(vendor = company)

		routeArea = {
			'frontend' : 'standard',
			'adminhtml' : 'admin'
		}

		files = generatorController.getFiles()

		for idx in files:
			file = files[idx]
			directory = file.split(sep = '/')
			filename = directory.pop()
			className = filename.split(sep = '.')[0]
			blockName = files['block'].split(sep = '/')
			blockName = "\\".join(blockName).split(sep = '.')

			pathPrefix = currentDirectory + delimiter + appCodePath + delimiter + company + delimiter + module + delimiter

			os.makedirs(pathPrefix + delimiter.join(directory), exist_ok = True)
			content = ""

			if 'controller' == idx:
				content = controllerControllerTpl.format(vendor = company, module = module, copyright = copyrightFormat, namespace = "\\".join(directory), classs = className)
			if 'block' == idx:
				content = controllerBlockTpl.format(vendor = company, module = module, copyright = copyrightFormat, namespace = "\\".join(directory), classs = className)

			if 'route' == idx:
				content = controllerRoutesTpl.format(vendor = company, module = module, area = routeArea[scope], route = route, copyright = 'COPYRIGHT HERE!')

			if 'layout' == idx:
				content = controllerLayoutTpl.format(vendor = company, module = module, route = route, copyright = 'COPYRIGHT HERE!', action = generatorController.getActionClass().lower(), block = blockName[0], layout = className.lower(), controller = generatorController.getControllerClass().lower())

			if 'view' == idx:
				content = controllerTemplateTpl.format(vendor = company, module = module, copyright = copyrightFormat, file = files['controller'], block = blockName[0])

			if not os.path.exists(file):
				with open(pathPrefix + file, 'w') as fileIO:
					fileIO.writelines(content)
					fileIO.close()

			sublime.active_window().open_file(pathPrefix + file)

	def input(self, args):
		company = CompanyInputHandler()
		company.setView(self.view)
		return company
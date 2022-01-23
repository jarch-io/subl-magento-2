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
			text = "Index"

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

		return sublime.Html("""
			<html>
				<body>
					{cssStyle}
					<div>
						<code>Access from https://yourhost.com/{route}/{controllerPath}/{action}</code>
					</div>
					<ul>
						<li>
							Block/{controllerClass}/{actionClass}.php
						</li>
						<li>
							Controller
						</li>
						<li>
							etc
							<ul>
								<li>
									{scope}
									<ul>
										<li>routes.xml</li>
									</ul>
								</li>
							</ul>
						</li>
						<li>
							view
							<ul>
								<li>
									{scope}
									<ul>
										<li>
											layout
											<ul>
												<li>
													{route}_{controllerUnder}_{action}.xml
												</li>
											</ul>
										</li>
										<li>
											templates
											<ul>
												<li>
													{controllerUnder}/{action}.phtml
												</li>
											</ul>
										</li>
									</ul>
								</li>
							</ul>
						</li>
					</ul>
				</body>
			</html>
		""".format(cssStyle = commonCss, controllerClass = 'Index', actionClass = 'Index', scope = 'frontend', route = 'module', controllerUnder = 'index', action = 'index', controllerPath = 'index'))

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

	def setvendor(self, vendor):
		self.vendor = vendor

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
	
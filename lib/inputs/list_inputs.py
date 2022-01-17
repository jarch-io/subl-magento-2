import sublime_plugin

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
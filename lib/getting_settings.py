import sublime

class Settings():
	settings = {}

	def __init__(self):
		changeSettings = False

		defaultFile = 'Magento2 ({}).sublime-settings'.format(sublime.platform())
		userFile = 'Magento2.sublime-settings'

		userSettings = sublime.load_settings(userFile)
		default = sublime.load_settings(defaultFile)

		if userSettings.get('company') is None:
			userSettings.set('company', default.get('company'))

		if userSettings.get('app_code_path') is None:
			userSettings.set('app_code_path', default.get('app_code_path'))

		if userSettings.get('delimiter_path') is None:
			userSettings.set('delimiter_path', default.get('delimiter_path'))
		
		if changeSettings == True:
			sublime.save_settings(userFile)

		self.settings = userSettings

	def getSetting(self, key = ''):
		if(key == ''):
			return self.settings
		else:
			return self.settings.get(key)

	def getCopyright(self, **args):
		copyright = ''

		for company in self.getSetting('company'):
			if company['name'] == args.get('vendor'):
				copyright = company['copyright_format']
				break

		return copyright.format(**args)

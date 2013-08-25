import sublime
import sublime_plugin
import subprocess

PLUGIN_FOLDER = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = "GoogleTranslate.sublime-settings"
NODE_PATH = None

# settings = sublime.load_settings(SETTINGS_FILE)

class GoogleTranslateCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		nothing_selected = True
		for (index, region) in enumerate(self.view.sel()):
			log(["index", index, "region", self.view.substr(region)])
			text = self.view.substr(region)
			if len(text) == 0: 
				continue
			nothing_selected = False
			#sublime.set_timeout_async(lambda: self.translate(text, index), 0)
			self.translate(text, index)
		if (nothing_selected):
			sublime.status_message("Nothing is selected")

	def translate(self, text, index):
		result = run_node_process([PLUGIN_FOLDER + "/translate.js", text])
		log(["Translate result", text, result])
		self.view.run_command('set_translation_result', {"index": index, "result": result})

class SetTranslationResultCommand(sublime_plugin.TextCommand):
	def run(self, edit, index = None, result = None):
		for (i, region) in enumerate(self.view.sel()):
			log(["set_translation_result. index: ", index, "result", result])
			if (i == index):
				self.view.replace(edit, region, result)

def run_node_process(args):
	cmd = "node " + '"' + '" "'.join(args) + '"'
	log(["Command ", cmd])
	startupinfo = subprocess.STARTUPINFO()
	startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	output = subprocess.Popen(cmd, stdout=subprocess.PIPE, startupinfo=startupinfo).communicate()[0]
	return output.decode("utf-8")

def log(args):
	return
	args = [str(v) for v in args]
	print(" ".join(args))

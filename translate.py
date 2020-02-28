import urllib
import hashlib
import json
import random
import sublime
import sublime_plugin

base_url = 'http://dict.youdao.com/w/eng/'

appid = ''  # 填写你的appid
secretKey = ''  # 填写你的密钥
def buildUrl(text):
	myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
	fromLang = 'auto'   #原文语种
	toLang = 'zh'   #译文语种
	salt = random.randint(32768, 65536)	
	sign = appid + text + str(salt) + secretKey
	sign = hashlib.md5(sign.encode()).hexdigest()
	myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(text) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
	return myurl

class TranslateCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sels = self.view.sel()
		sels_str = []
		for sel in sels:
			sel_str = self.view.substr(sel).strip()
			if sel_str:
				sels_str.append(sel_str)
			if not sels_str:
				return
		if len(sels_str) == 0:
			sublime.status_message('Nothing Selected.')
			return
		elif len(sels_str) >= 2:
			sublime.status_message('Multiple selected. Translating the first, ignoring the rest...')
		else:
			sublime.status_message('Translating...')
		url = buildUrl(sels_str[0])
		with urllib.request.urlopen(url) as f:
			data = f.read().decode('utf-8')
			
			if f.status >= 400 or f.status < 200:
				print('status code: ', f.status)
				print('response: ', data)
				sublime.status_message('Translator Error!')
				return
			result = json.loads(data)			
			if 'error_code' in result:
				print('error_code: ',result.error_code)
				print('response: ', data)				
				sublime.status_message('Translator Error!')
				return
			dst = result['trans_result'][0]['dst']
			print(dst)
			sublime.set_clipboard(dst)
			sublime.status_message("Translated.")
			# The fox is running. The cat is dead.
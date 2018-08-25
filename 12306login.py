# @Author  : ShiRui

import requests
import random


class Login(object):

	# 必要参数
	def __init__(self):

		self.header = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
		}
		self.session = requests.session()
		# 保持session。
		self.session.headers.update(self.header)
		self.login_page_url = 'https://kyfw.12306.cn/otn/login/init'
		self.login_url = 'https://kyfw.12306.cn/passport/web/login'
		self.captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image'
		self.check_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
		self.uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
		self.auth_url = 'https://kyfw.12306.cn/otn/uamauthclient'
		self.point = {
		'1': '35,43',
		'2': '108,43',
		'3': '185,43',
		'4': '254,43',
		'5': '34,117',
		'6': '108,117',
		'7': '180,117',
		'8': '258,117',
		}

	# 主逻辑，登陆。
	def login(self, username, passwd):

		# 登陆需要传入的参数
		data = {
			'username': username,
			'password': passwd,
			'appid': 'otn'
		}
		# 请求首页
		self.session.get(self.login_page_url)
		# 调用下载验证码的函数
		self.download_img()
		# 检查验证码，并返回数据。
		check_captcha = self.check_captcha()
		# 如果返回的数据不为空，程序继续向下走。
		if check_captcha:
			# 访问真正的登录页。
			resopnse = self.session.post(self.login_url, data)
			# 如果返回值的result_code==0,则说明登陆是没有问题的。
			if resopnse.json()['result_code'] == 0:
				# 获取token值（ps:12306采取的验证登陆的方法，每个用户登陆都有一个token）
				tk = self.tk_token()
				# 验证token
				auth_url = self.get_tk(tk)
				# 如果返回的数据result_code==0，则说明登陆是成功的。
				if auth_url.json()['result_code'] == 0:
					print("登陆成功！用户名为：%s" % auth_url.json()['username'])

	# 分割验证码，使得登陆更加方便。
	def get_point(self, num):
		# 切割输入的数字。
		num = num.split(',')
		temp = []
		# 遍历数子，temp加入每个图片相对应的坐标。
		for item in num:
			temp.append(self.point[item])
		# 拼接验证码坐标，并返回。
		return ','.join(temp)

	# 下载验证码
	def download_img(self):

		# 验证码需要的数据
		data = {
			'login_site': 'E',
			'module': 'login',
			'rand': 'sjrand',
			str(random.random()): '' # 这是一个随机数，12306专门加在每个url后面的，便于区分。
		}
		# 请求验证码页面
		response = self.session.post(self.captcha_url, params=data)
		# 把获取的验证码写入本地。
		with open("html.jpg", "wb") as f:
			f.write(response.content)

	# 验证验证码
	def check_captcha(self):

		data = {
			'answer': self.get_point(input('请输入正确的图片序号>>>:')), # 这就是需要用户自己输入的验证码顺序
			'login_site': 'E',
			'rand': 'sjrand'
		}
		# 请求验证的地址
		response = self.session.post(self.check_captcha_url, data)
		# 返回响应
		return response

	# 获取token。
	def tk_token(self):

		data = {
			'appid': 'otn'
		}
		# 访问token页面。
		tk_response = self.session.post(self.uamtk_url, data)
		# 返回每次登陆都不一样的token值。
		return tk_response.json()['newapptk']

	# 验证token
	def get_tk(self, tk):

		data = {
			'tk': tk,
		}
		# 请求验证token的页面
		response = self.session.post(self.auth_url, data)
		# 返回响应
		return response

if __name__ == '__main__':

	# 实例化对象
	userlogin = Login()
	# 调用方法，传入你自己的用户名和密码。
	userlogin.login("你的用户名", "你的密码")

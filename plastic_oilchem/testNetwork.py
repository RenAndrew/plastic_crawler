#coding:utf-8
 
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
 
def z_get_href_by_partial_link_text( str ):
	try:
		var = driver.find_element_by_partial_link_text(str)
		return var.get_attribute("href")
	except:
		return ''
 
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'performance':'ALL' }
driver = webdriver.Chrome( desired_capabilities=d)
 
driver.get("http://news.oilchem.net/login.shtml")
 
print "Title: " + driver.title
 
# login_key = ['登录','登陆','登入','login', 'Login', 'LOGIN']
# reg_key = ['注册','加入','新账户','register', 'Register', 'REG']
# findpass_key = ['找回密码','忘记密码']
 
# register_u = ''
# login_u = ''
# findpass_u = ''
 
# register = driver.find_element_by_partial_link_text("注册")
 
# register.click()
 
# value_box = driver.find_element_by_name('mobile')
# value_box.send_keys('13000000000')
# value_box.send_keys(Keys.TAB)
 
for entry in driver.get_log('performance'):
	# if (entry['url'].find('getcode/api') != -1):
	print entry
#print "Register: "+z_get_href_by_partial_link_text("注册")
#print "Login: "+z_get_href_by_partial_link_text("登录")
#print "FindPassword1: "+z_get_href_by_partial_link_text("找回密码")
#print "FindPassword2: "+z_get_href_by_partial_link_text("忘记密码")
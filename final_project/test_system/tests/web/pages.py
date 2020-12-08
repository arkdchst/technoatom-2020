from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException,StaleElementReferenceException
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse

from config import *
from helpers import *

class Page:

	def __init__(self, driver):
		self.driver = driver

	def open(self):
		self.driver.get(f'{MYAPP_URL_WEB}/{self.path}')
		return self.actual()

	def opened(self):
		parsed = urlparse(self.driver.current_url)
		return parsed.path == f'/{self.path}' and parsed.netloc == f'{MYAPP_HOST_WEB}:{MYAPP_PORT_WEB}'


	def actual_class(self):
		classes = Page.__subclasses__()
		for class_ in classes:
			page = class_(self.driver)
			if page.opened():
				return page.__class__

	def actual(self):
		class_ = self.actual_class()
		if class_:
			return class_(self.driver)
		else:
			return None

	def locator(self, name):
		from .locators import locators

		for type_ in type(self).__mro__:
			if type_ in locators and name in locators[type_]:
				return locators[type_][name]

	def find(self, locator):
		element = self.wait().until(EC.presence_of_element_located(locator))
		return element

	def find_or(self, *locators):
		conds = []
		for locator in locators:
			conds.append(EC.presence_of_element_located(locator))
		element = self.wait().until(self.or_(conds))
		return element

	def or_(self, conds):
		def _located(driver):
			for cond in conds:
				element = None
				try:
					element = cond(driver)
				except: pass
				if element: return element
			return False

		return _located


	def wait(self, timeout=10):
		return WebDriverWait(self.driver, timeout)

	def text_found(self, pattern):
		return pattern in self.driver.page_source

	def element_found(self, locator):
		return self.driver.find_elements(*locator)

	def click(self, locator):		
		self.click_element(self.wait().until(EC.element_to_be_clickable(locator)))

	def click_element(self, element):
		RETRY_COUNT = 5
		for i in range(RETRY_COUNT):
			try:
				element.click()
				return
			except StaleElementReferenceException as e:
				if i == RETRY_COUNT - 1:
					raise e

	def type(self, locator, keys):
		self.wait().until(EC.element_to_be_clickable(locator)).send_keys(keys)

	def click_or(self, *locators):
		conds = []
		for locator in locators:
			conds.append(EC.element_to_be_clickable(locator))
		self.click_element(self.wait().until(self.or_(conds)))



class LoginPage(Page):
	path = 'login'

	def type_all(self, username, password):
		self.type_username(username)
		self.type_password(password)

	def type_username(self, username):
		self.username = username
		self.type(self.locator('USERNAME_FIELD'), username)

	def type_password(self, password):
		self.type(self.locator('PASSWORD_FIELD'), password)

	def login(self):
		self.click(self.locator('LOGIN_BUTTON'))

		return self.actual()

	# def reg(self):
	# 	RegPage(self.driver).open()
	# 	return self.actual()

	def reg(self):
		self.click(self.locator('REG_BUTTON'))
		return self.actual()

class RegPage(Page):
	path = 'reg'

	def type_all(self, username, email, password, repeat, term_accepted=True):
		self.type_username(username)
		self.type_email(email)
		self.type_password(password)
		self.type_repeat(repeat)
		self.select_term_accepted(term_accepted)

	def type_username(self, username):
		self.username = username
		self.type(self.locator('USERNAME_FIELD'), username)

	def type_email(self, email):
		self.type(self.locator('EMAIL_FIELD'), email)

	def type_password(self, password):
		self.type(self.locator('PASSWORD_FIELD'), password)

	def type_repeat(self, password):
		self.type(self.locator('REPEAT_FIELD'), password)

	def select_term_accepted(self, accepted=True):
		check = self.find(self.locator('TERM_CHECK'))
		if check.is_selected() != accepted:
			self.click_element(check)

	def reg(self):
		self.click(self.locator('REG_BUTTON'))
		
		return self.actual()

class WelcomePage(Page):
	path = 'welcome/'

	def logout(self):
		self.driver.get(f'{MYAPP_URL_WEB}/logout')
		return self.actual()

	def logout_btn(self):
		self.click(self.locator('LOGOUT_BUTTON'))
		return self.actual()

	def click_menu(self, locators):
		chain = ActionChains(self.driver)
		for locator in locators:
			chain = chain.move_to_element(self.find(self.locator(locator)))

		chain.perform()
		self.click(self.locator(locators[-1]))
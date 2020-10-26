from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
import helpers
from time import sleep
import os


class Page:

	def __init__(self, driver):
		self.driver = driver

	def locator(self, name):
		from locators import locators

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


	def click_or(self, *locators):
		conds = []
		for locator in locators:
			conds.append(EC.element_to_be_clickable(locator))
		self.click_element(self.wait().until(self.or_(conds)))

	def wait_until_loads(self):
		self.wait().until(lambda d: not d.find_elements(By.CLASS_NAME, 'spinner'))


class MainPage(Page):

	def type_credentials(self, login, password):
		self.find(self.locator('EMAIL_FIELD')).send_keys(login)
		self.find(self.locator('PASSWORD_FIELD')).send_keys(password)

	def login(self, login, password):
		self.click(self.locator('LOGIN_MAIN_BUTTON'))
		self.type_credentials(login, password)
		self.click(self.locator('LOGIN_FORM_BUTTON'))
		if 'https://target.my.com/dashboard' == self.driver.current_url:
			return CampaignsPage(self.driver)
		else:
			return Page(self.driver)

class DashboardPage(Page):

	def audiences_page(self):
		self.click(self.locator('SEGMENTS_BUTTON'))
		return AudiencesPage(self.driver)

	def logout(self):
		self.click(self.locator('ACCOUNT_BUTTON'))
		while True:
			try:
				self.click(self.locator('LOGOUT_BUTTON'))
				break
			except ElementClickInterceptedException: pass
		return MainPage(self.driver)

class CampaignsPage(DashboardPage):

	def campaign_creation_page(self):
		self.click_or(self.locator('CREATE_BUTTON1'), self.locator('CREATE_BUTTON2'))
		return CampaignCreationPage(self.driver)

	def wait_until_loads(self):
		super(CampaignsPage, self).wait_until_loads()
		self.wait().until(lambda d: self.text_found('Daily budget, ₽') or self.text_found('How to get started?') or self.text_found('not found'))

	def create_campaign(self):
		creation_page = self.campaign_creation_page()
		creation_page.set_objective()
		creation_page.set_link()
		creation_page.set_budget()
		creation_page.set_format()
		creation_page.set_image()
		name = creation_page.set_name()
		creation_page.create_campaign_final()
		return name

	def campaign_exists(self, name):
		return self.text_found(name)

	def delete_campaign(self, name):
		self.find(self.locator('SEARCH_FIELD')).send_keys(name)
		self.click(self.locator('HINT')(name))
		self.click(self.locator('CHECK'))
		self.click(self.locator('ACTIONS_ARROW'))
		self.click(self.locator('DELETE_BUTTON'))

	def is_empty(self):
		self.text_found('How to get started?')

class CampaignCreationPage(DashboardPage):

	def set_objective(self):
		self.click(self.locator('TRAFFIC_OBJECTIVE'))

	def set_link(self):
		self.find(self.locator('LINK_FIELD')).send_keys('test.test')

	def set_budget(self):
		self.find(self.locator('BUDGET_DAY_FIELD')).send_keys('100')
		self.find(self.locator('BUDGET_TOTAL_FIELD')).send_keys('100')

	def set_format(self):
		self.click(self.locator('BANNER_FORMAT'))

	def set_image(self):
		self.find(self.locator('IMAGE_UPLOADER')).send_keys(os.path.dirname(__file__) + '/upload.png')

	def set_name(self):
		name = helpers.random_name()
		element = self.find(self.locator('NAME_FIELD'))
		element.clear()
		element.send_keys(name)
		return name

	def create_campaign_final(self):
		#try until no Internal Server Error occures
		while True:
			self.click(self.locator('FINAL_BUTTON'))
			if not self.element_found((By.CLASS_NAME, 'button_pending')): continue

			self.wait().until(lambda d: not self.element_found((By.CLASS_NAME, 'button_pending')))
			if not self.text_found('Internal Server Error'):
				return CampaignsPage(self.driver)



class AudiencesPage(DashboardPage):

	def segment_creation(self):
		self.click_or(self.locator('CREATE_BUTTON1'), self.locator('CREATE_BUTTON2'))
		return SegmentCreationPage(self.driver)

	def wait_until_loads(self):
		super(AudiencesPage, self).wait_until_loads()
		self.wait().until(lambda d: self.element_found((By.XPATH, '//span[text()="Segment name"]')) or self.element_found(self.locator('EMPTY_PAGE_BANNER')))

	def create_segment(self):
		creation_page = self.segment_creation()
		creation_page.set_apps()
		creation_page.add_segment()
		name = creation_page.set_name()
		creation_page.create_segment_final()
		return name

	def is_empty(self):
		return self.element_found(self.locator('EMPTY_PAGE_BANNER'))

	def delete_segment(self, name):
		self.find(self.locator('SEARCH_FIELD')).send_keys(name)
		self.click(self.locator('HINT')(name))
		self.click(self.locator('DELETE_BUTTON'))
		self.click(self.locator('CONFIRM_DELETE_BUTTON'))
		if not self.is_empty():
			self.click(self.locator('CLEAR_SEARCH_BUTTON'))		

	def segment_exists(self, name):
		return self.text_found(name)


class SegmentCreationPage(DashboardPage):

	def set_apps(self):
		self.click(self.locator('APPS'))
		self.click(self.locator('PLAYED_AND_PAYED_CHECK'))

	def add_segment(self):
		self.click(self.locator('ADD_SEGMENT_BUTTON'))

	def create_segment_final(self):
		self.click(self.locator('CREATE_SEGMENT_BUTTON'))
		return AudiencesPage(self.driver)

	def set_name(self):
		name = helpers.random_name()
		element = self.find(self.locator('NAME_FIELD'))
		element.clear()
		element.send_keys(name)
		return name


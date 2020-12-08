import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from contextlib import contextmanager

import config
from helpers import *
import vkapi_client

from db.fixtures import *

from .pages import *


@pytest.fixture
def driver(request):
	# for running tests on host:
	#
	# manager = ChromeDriverManager()
	# driver = webdriver.Chrome(executable_path=manager.install())
	# yield driver
	# driver.quit()

	# you may also enable video capturing
	desired_capabilities={'acceptInsecureCerts': True, 'browserName': 'chrome','version': '87.0', "screenResolution": "1920x1080x24", "enableVideo": False, "videoName": f"{'::'.join([node.name for node in request.node.listchain()])}.mp4"}
	driver = webdriver.Remote(command_executor=f'{config.SELENOID_URL}/wd/hub/', desired_capabilities=desired_capabilities)
	driver.set_window_position(0, 0)
	driver.set_window_size(1920, 1080)
	yield driver
	driver.quit()

@pytest.fixture
def login_page(driver):
	page = LoginPage(driver).open()

	if isinstance(page, WelcomePage):
		page.logout()

	yield page

@pytest.fixture
def reg_page(login_page, driver):
	yield login_page.reg()

@pytest.fixture
def welcome_page_login(login_page, driver, added_user_add):
	@contextmanager
	def gen(user=None):
		login_page.type_all(user.username, user.password)
		page = login_page.login()

		yield page

	return gen

@pytest.fixture
def welcome_page_logout(driver, added_user_del):
	@contextmanager
	def gen():
		yield
		page = WelcomePage(driver).logout()

	return gen

@pytest.fixture
def welcome_page(welcome_page_login, welcome_page_logout, login_page, driver, added_user):
	@contextmanager
	def gen(user=None):
		with welcome_page_login(user) as page:
			with welcome_page_logout():
				yield page

	return gen


@pytest.fixture
def vkid():
	@contextmanager
	def gen(username, id=None):
		if id == None:
			id = random_number(10)

		vkapi_client.set(username, id)
		try:
			yield id
		finally:
			vkapi_client.unset(username)

	return gen


@pytest.fixture(scope='function', autouse=True)
def allure_screenshot(request, driver):
	yield
	if request.node.rep_call.failed: # rep_call added in conftest.py
		allure.attach(body=driver.get_screenshot_as_png(), name='screenshot', attachment_type=allure.attachment_type.PNG)

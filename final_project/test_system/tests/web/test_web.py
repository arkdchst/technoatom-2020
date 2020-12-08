import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import timedelta, datetime
from time import sleep

import config
from helpers import bug # abbreviation for xfail, see tests/helpers.py

from web import pages
from web import locators
from db.fixtures import *
from web.fixtures import *
from api.test_api import client as api_client

class TestWelcome:
	"""Tests for myapp's welcome page"""

	data = [
		#((LINK_LOCATOR), check),
		#((MENU_LOCATOR, LINK_LOCATOR), check),
		# check returns True if the correct page opened
		(('API_LINK',),									lambda driver, page: 'API' in driver.title),
		(('FUTURE_LINK',),								lambda driver, page: '50 Years' in driver.title),
		(('SMTP_LINK',),								lambda driver, page: 'SMTP' in driver.title),
		(('HOME_LINK',),								lambda driver, page: isinstance(page.actual(), WelcomePage)),
		(('PYTHON_MENU',),								lambda driver, page: 'Python.org' in driver.title),
		(('PYTHON_MENU', 'PYTHON_HISTORY_LINK'),		lambda driver, page: 'History' in driver.title),
		(('PYTHON_MENU', 'ABOUT_FLASK_LINK'),			lambda driver, page: 'Flask' in driver.title),
		pytest.param(('LINUX_MENU', 'CENTOS_LINK'),		lambda driver, page: 'CentOS' in driver.title,
			marks=pytest.mark.xfail(reason='bug')),
		(('NETWORK_MENU', 'WIRESHARK_NEWS_LINK'),		lambda driver, page: 'News' in driver.title),
		(('NETWORK_MENU', 'WIRESHARK_DOWNLOAD_LINK'),	lambda driver, page: 'Download' in driver.page_source),
		(('NETWORK_MENU', 'TCPDUMP_EXAMPLES_LINK'),		lambda driver, page: 'Tcpdump Examples' in driver.title),
	]

	@pytest.mark.parametrize('locators, check', data)
	def test_link(self, welcome_page, added_user, driver, locators, check):
		"""Test all links.

		Test that all links point to right pages.
		"""
		with added_user() as user, welcome_page(user) as page:
			page.click_menu(locators)

			driver.switch_to.window(driver.window_handles[-1]) # switch to opened tab

			assert check(driver, page)

	def test_logout(self, connection, welcome_page, added_user):
		"""Test logout button.

		Test redirect to login page and setting active = 0.
		"""
		with added_user() as user, welcome_page(user) as page:
			page = page.logout_btn()

			assert isinstance(page, LoginPage)
			assert not connection.get_user(user.username).active

class TestLogin:
	"""Test login form."""

	def test(self, connection, driver, login_page, added_user, welcome_page_logout):
		"""Test redirect to welcome page after successful login."""
		with added_user() as user, welcome_page_logout():
			login_page.type_all(user.username, user.password)
			page = login_page.login()

			assert isinstance(page, WelcomePage)

	def test_db_fields(self, connection, driver, login_page, added_user):
		"""Test DB fields values of user record.

		Test setting active=1 and right start_active_time with 1 minute-precision.
		"""
		with added_user() as user:
			assert not user.active
			login_page.type_all(user.username, user.password)
			page = login_page.login()

			user = connection.get_user(user.username)
			assert user.active

			page.logout()

			now = datetime.now()
			assert now - timedelta(minutes=1) <= user.start_active_time <= now + timedelta(minutes=1)


	def test_bad_password(self, connection, driver, login_page, added_user):
		"""Test login form behavior when password is wrong.

		Test that after bad login user stays on login page and active remains zero.
		"""
		with added_user() as user:
			login_page.type_all(user.username, 'bad_password')
			page = login_page.login()

			assert not isinstance(page, WelcomePage)
			assert page.element_found(page.locator('INVALID_PASSWORD'))

			user = connection.get_user(user.username)
			assert not user.active

	def test_short_username(self, login_page, driver):
		"""Test that short username is invalid."""
		user = gen_user()
		login_page.type_all(random_str(5), user.password)
		login_page.login()
		assert 'Incorrect username length' in driver.page_source

	def test_empty_password(self, login_page, driver):
		"""Test that empty password is invalid."""
		user = gen_user()
		login_page.type_all(user.username, ' ')
		login_page.login()
		assert 'Необходимо указать пароль для авторизации' in driver.page_source

	@bug
	def test_both_username_password_bad(self, login_page, driver):
		"""Test if both username and password are invalid error message."""
		user = gen_user()
		login_page.type_all(random_str(5), ' ')
		login_page.login()
		assert not "{'username':" in driver.page_source # 'Oh no, both username and password are bad!' or smth like this

	def test_spaced_creds(self, login_page, driver, added_user):
		"""Test that credentials with spaces accepted in login form.

		Spaced credentials are accepted in registration form, so we should make sure that spaces aren't trimmed in login form.
		See TestRegister::test_spaced_creds.
		"""
		user = gen_user()
		user.username = f' {random_str(5)} spa c ed '
		user.password = f' {random_str(5)} sp ac ed '
		with added_user(user) as user:
			login_page.type_all(user.username, user.password)
			page = login_page.login()

			assert isinstance(page, WelcomePage)

class TestRegister:
	"""Test registration page."""

	def test(self, connection, driver, reg_page, added_user_del, welcome_page_logout):
		"""Test redirection to welcome page after registration and that new record appeared in DB."""
		with added_user_del() as user, welcome_page_logout():
			reg_page.type_all(user.username, user.email, user.password, user.password, True)
			page = reg_page.reg()

			assert isinstance(page, WelcomePage)
			assert connection.get_user(user.username)

	def test_db_fields(self, connection, driver, reg_page, added_user_del, welcome_page_logout):
		"""Test DB fields of newly created user record."""
		with added_user_del() as user, welcome_page_logout():
			reg_page.type_all(user.username, user.email, user.password, user.password, True)
			page = reg_page.reg()

			db_user = connection.get_user(user.username)
			assert db_user.username == user.username
			assert db_user.password == user.password
			assert db_user.email == user.email
			assert db_user.access == 1

	@bug
	def test_db_fields_active(self, connection, driver, reg_page, added_user_del, welcome_page_logout):
		"""Test setting active=1 and start_active_time with 1 minute-precision after registration."""
		with added_user_del() as user, welcome_page_logout():
			reg_page.type_all(user.username, user.email, user.password, user.password, True)
			page = reg_page.reg()

			db_user = connection.get_user(user.username)
			assert db_user.active == 1

			now = datetime.now()
			assert now - timedelta(minutes=1) <= user.start_active_time <= now + timedelta(minutes=1)

	@bug
	def test_spaced_creds(self, reg_page, driver, added_user_del, connection):
		"""Test that spaces in credentials aren't accepted."""
		user = gen_user()
		user.username = f' {random_str(5)} spa c ed '
		user.password = f' {random_str(5)} sp ac ed '
		with added_user_del(user) as user:
			reg_page.type_all(user.username, user.email, user.password, user.password, True)
			page = reg_page.reg()

			assert not isinstance(page, WelcomePage)
			assert not connection.get_user(user.username)

	def test_username_exists(self, reg_page, added_user, driver):
		"""Test error message if user with same username already exists."""
		with added_user() as user:
			reg_page.type_all(user.username, user.email, user.password, user.password, True)
			page = reg_page.reg()

			assert not isinstance(page, WelcomePage)
			assert 'User already exist' in driver.page_source

	def test_diff_passwords(self, connection, driver, reg_page, added_user_del):
		"""Test that if password and confirmation don't match then registration fails."""
		with added_user_del() as user:
			reg_page.type_all(user.username, user.email, user.password, user.password + 'diff', True)
			page = reg_page.reg()

			assert not isinstance(page, WelcomePage)
			assert 'Passwords must match' in driver.page_source
			assert not connection.get_user(user.username)

	def test_bad_email(self, connection, driver, reg_page, added_user_del):
		"""Test that invalid email isn't accepted."""
		user = gen_user()
		user.email = random_str()
		with added_user_del(user) as user:
			reg_page.type_all(user.username, user.email, user.password, user.password, True)
			page = reg_page.reg()

			assert not isinstance(page, WelcomePage)
			assert 'Invalid email address' in driver.page_source
			assert not connection.get_user(user.username)

	@bug
	def test_dot_email(self, driver, reg_page, added_user_del, welcome_page_logout): # test if email can end with '.'
		"""Test that login form accepts email with dot in the end."""
		user = gen_user()
		user.email = user.email + '.'
		with added_user_del(user) as user, welcome_page_logout():
			reg_page.type_all(user.username, user.email, user.password, user.password, True)
			page = reg_page.reg()

			assert isinstance(page, WelcomePage)
			assert connection.get_user(user.username)

	@bug
	def test_email_exists(self, reg_page, added_user, driver):
		"""Test error message if user with same email already exists."""
		with added_user() as user:
			new_user = gen_user()
			reg_page.type_all(new_user.username, user.email, new_user.password, new_user.password, True)
			page = reg_page.reg()

			assert not isinstance(page, WelcomePage)
			assert not 'Internal Server Error' in driver.page_source # 'User with this email already exists' or something like that

class TestVKAPI:
	"""Test VK ID widget on welcome page."""

	def test(self, driver, added_user, welcome_page, vkid):
		"""Test that right VK ID displayed."""
		with added_user() as user, vkid(user.username) as id, welcome_page(user) as page:
			assert f'VK ID: {id}' in driver.page_source

	@bug
	def test_zero_id(self, driver, added_user, welcome_page, vkid):
		"""Test that VK ID = 0 is also displayed on on welcome page."""
		with added_user() as user, vkid(user.username,id=0) as id, welcome_page(user) as page:
			assert f'VK ID: {id}' in driver.page_source

	@bug
	def test_long_id(self, driver, added_user, welcome_page, vkid):
		"""Test that long VK ID is correctly displayed on welcome page."""
		with added_user() as user, vkid(user.username,id=random_number(150)) as id, welcome_page(user) as page:
			assert not rect_intersect(page.find(page.locator('VKID')).rect, page.find(page.locator('NETWORK_MENU')).rect)

class TestBlocked:
	"""Test all related to access=0 in DB and API block_user method."""

	def test(self, connection, driver, added_user, login_page):
		"""Test that user can't login when blocked.

		Test also that active remains zero.
		"""
		user = gen_user()
		user.access = 0
		with added_user(user) as user:
			login_page.type_all(user.username, user.password)
			page = login_page.login()

			assert isinstance(page, LoginPage)
			assert 'Ваша учетная запись заблокирована' in driver.page_source
			assert not connection.get_user(user.username).active

	def test_dynamic_block(self, connection, driver, added_user, login_page):
		"""Test that after user blocking user is forcely logged out."""
		with added_user() as user:
			login_page.type_all(user.username, user.password)
			page = login_page.login()

			user.access = 0
			connection.update_user(user.username, user)

			page.open()

			assert isinstance(page.actual(), LoginPage)
			assert 'This page is available only to authorized users' in driver.page_source

	@bug
	def test_dynamic_block_db_fields(self, connection, driver, added_user, login_page, api_client):
		"""Test that after user blocking DB fields are set correctly."""
		with added_user() as user:
			login_page.type_all(user.username, user.password)

			page = login_page.login()

			api_client.block_user(user.username)

			page.open()
			assert not connection.get_user(user.username).active


def test_failed_example(connection, driver, reg_page, added_user_del):
	"""Test that always fails - just for example."""
	with added_user_del() as user:
		reg_page.type_all(user.username, user.email, user.password, user.password, False)
		reg_page.reg()

		sleep(1)
		assert False

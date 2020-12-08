from selenium.webdriver.common.by import By
from .pages import *


locators = {
	LoginPage: {
		'USERNAME_FIELD': (By.XPATH, '//input[@placeholder="Username"]'),
		'PASSWORD_FIELD': (By.XPATH, '//input[@placeholder="Password"]'),
		'LOGIN_BUTTON': (By.XPATH, '//input[@value="Login"]'),
		'INVALID_PASSWORD': (By.XPATH, '//div[text()="Invalid username or password"]'),
		'REG_BUTTON': (By.XPATH, '//a[@href="/reg"]'),
	},

	RegPage: {
		'USERNAME_FIELD': (By.XPATH, '//input[@placeholder="Username"]'),
		'EMAIL_FIELD': (By.XPATH, '//input[@placeholder="Email"]'),
		'PASSWORD_FIELD': (By.XPATH, '//input[@placeholder="Password"]'),
		'REPEAT_FIELD': (By.XPATH, '//input[@placeholder="Repeat password"]'),
		'TERM_CHECK': (By.XPATH, '//input[@id="term"]'),
		'REG_BUTTON': (By.XPATH, '//input[@value="Register"]'),
	},

	WelcomePage: {
		'LOGOUT_BUTTON': (By.XPATH, '//a[@href="/logout"]'),
		'VKID': (By.XPATH, '//li[contains(text(),"VK")]'),

		'API_LINK': (By.XPATH, '//*[contains(text(),"API")]/following-sibling::figure'),
		'FUTURE_LINK': (By.XPATH, '//*[contains(text(),"Future")]/following-sibling::figure'),
		'SMTP_LINK': (By.XPATH, '//*[contains(text(),"SMTP")]/following-sibling::figure'),
		'HOME_LINK': (By.XPATH, '//a[text()="HOME"]'),
		'PYTHON_MENU': (By.XPATH, '//a[text()="Python"]'),
		'LINUX_MENU': (By.XPATH, '//a[text()="Linux"]'),
		'NETWORK_MENU': (By.XPATH, '//a[text()="Network"]'),
		'PYTHON_HISTORY_LINK': (By.XPATH, '//a[text()="Python history"]'),
		'ABOUT_FLASK_LINK': (By.XPATH, '//a[text()="About Flask"]'),
		'CENTOS_LINK': (By.XPATH, '//a[text()="Download Centos7"]'),
		'WIRESHARK_NEWS_LINK': (By.XPATH, '//a[text()="News"]'),
		'WIRESHARK_DOWNLOAD_LINK': (By.XPATH, '//a[text()="Download"]'),
		'TCPDUMP_EXAMPLES_LINK': (By.XPATH, '//a[text()="Examples "]'),

	}

}
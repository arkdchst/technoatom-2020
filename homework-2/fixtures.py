import pytest
from selenium import webdriver
import pages
from webdriver_manager.chrome import ChromeDriverManager


email = 'cavid49442@pastortips.com' #'fidorig277@zik2zik.com'
password = 'cavid49442' #'fidorig277'


@pytest.fixture
def driver(request):
	selenoid_option = request.config.getoption('--selenoid')
	options = webdriver.ChromeOptions()
	if selenoid_option:
		driver = webdriver.Remote(command_executor='http://'+ selenoid_option +'/wd/hub', desired_capabilities={'acceptInsecureCerts': True, 'browserName': 'chrome','version': '80.0'})
	else:
		manager = ChromeDriverManager()
		driver = webdriver.Chrome(executable_path=manager.install(), desired_capabilities={'acceptInsecureCerts': True})
	yield driver
	driver.quit()

@pytest.fixture
def main_page(driver):
	driver.get('https://target.my.com/')
	yield pages.MainPage(driver)

@pytest.fixture
def campaigns_page(main_page):
	ret = main_page.login(email, password)
	ret.wait_until_loads()
	yield ret
	ret.logout()

@pytest.fixture
def audiences_page(campaigns_page):
	ret = campaigns_page.audiences_page()
	ret.wait_until_loads()
	yield ret
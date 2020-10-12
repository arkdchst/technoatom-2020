from selenium.webdriver.common.by import By
from pages import *


locators = {
	MainPage: {
		'LOGIN_MAIN_BUTTON' : (By.XPATH, '//div[contains(@class, "responseHead-module-button")]'),
		'EMAIL_FIELD' : (By.NAME, 'email'),
		'PASSWORD_FIELD' : (By.NAME, 'password'),
		'LOGIN_FORM_BUTTON' : (By.XPATH, '//div[contains(@class, "authForm-module-button")]'),
	},
	DashboardPage: {
		'SEGMENTS_BUTTON' : (By.XPATH, '//a[@href="/segments"]'),
		'ACCOUNT_BUTTON' : (By.XPATH, '//div[contains(@class, "right-module-rightButton")]'),
		'LOGOUT_BUTTON' : (By.XPATH, '//a[@href="/logout"]')
	},
	CampaignsPage: {
		'CREATE_BUTTON1' : (By.XPATH, '//a[@href="/campaign/new"]'),
		'CREATE_BUTTON2' : (By.XPATH, '//div[text()="Create campaign"]'),
		'SEARCH_FIELD' : (By.XPATH, '//input[@placeholder="Search..."]'),
		'HINT' : lambda name: (By.XPATH, '//li[@title="'+ name +'"]'),
		'CHECK' : (By.XPATH, '//input[contains(@class, "nameCell-module-checkbox")]'),
		'ACTIONS_ARROW' : (By.XPATH, '//div[contains(@class, "Actions")]//div[contains(@class, "select-module-arrow")]'),
		'DELETE_BUTTON' : (By.XPATH, '//li[@title="Delete"]'),

	},
	CampaignCreationPage: {
		'TRAFFIC_OBJECTIVE' : (By.CLASS_NAME, '_traffic'),
		'LINK_FIELD' : (By.XPATH, '//input[@placeholder="Enter the link"]'),
		'BUDGET_DAY_FIELD' : (By.XPATH, '//input[@data-test="budget-per_day"]'),
		'BUDGET_TOTAL_FIELD' : (By.XPATH, '//input[@data-test="budget-total"]'),
		'BANNER_FORMAT' : (By.XPATH, '//div[@data-id="patterns_4"]'),
		'IMAGE_UPLOADER' : (By.XPATH, '//input[@data-test="image_240x400"]'),
		'NAME_FIELD' : (By.XPATH, '//div[@class="campaign-name__name-wrap js-campaign-name-wrap"]//input'),
		'FINAL_BUTTON' : (By.XPATH, '//div[text()="Create a campaign"][@class="button__text"]/..'),
	},
	AudiencesPage: {
		'EMPTY_PAGE_BANNER' : (By.XPATH, '//div[@class="page_segments__instruction-wrap js-instruction-wrap"][@style="display: block;"]'),
		'CREATE_BUTTON1' : (By.XPATH, '//a[@href="/segments/segments_list/new/"]'),
		'CREATE_BUTTON2' : (By.XPATH, '//div[text()="Create segment"]/..'),
		'SEARCH_FIELD' : (By.XPATH, '//input[@placeholder="Search by name or id..."]'),
		'HINT' : lambda name: (By.XPATH, '//li[text()="' + name + '"]'),
		'ANY_HINT' : (By.XPATH, '//ul[contains(@class, "optionsList-module-optionsList")]/li'), # 'Nothing found...' hint including
		'DELETE_BUTTON' : (By.CLASS_NAME, 'icon-cross'),
		'CONFIRM_DELETE_BUTTON' : (By.XPATH, '//*[text()="Delete"]/..'),
		'CLEAR_SEARCH_BUTTON' : (By.XPATH, '//*[contains(@class, "suggester-module-clearIcon")]'),
	},
	SegmentCreationPage: {
		'APPS' : (By.XPATH, '//div[text()="Apps and games in social networks"]'),
		'PLAYED_AND_PAYED_CHECK' : (By.XPATH, '//input[contains(@class, "adding-segments-source__checkbox")]'),
		'ADD_SEGMENT_BUTTON' : (By.XPATH, '//div[text()="Add segment"]/..'),
		'CREATE_SEGMENT_BUTTON' : (By.XPATH, '//div[text()="Create segment"]/..'),
		'NAME_FIELD' : (By.XPATH, '//*[@class="js-segment-name"]//input'),
	}
}
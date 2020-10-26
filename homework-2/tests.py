import pytest
from time import sleep
import pages
import helpers
from fixtures import *



@pytest.mark.ui
def test_login(main_page):
	page = main_page.login(email, password)
	page.wait_until_loads()
	assert isinstance(page, pages.CampaignsPage)
	page.logout()

@pytest.mark.ui
def test_login_negative(main_page):
	page = main_page.login(email, 'bad_password')
	assert not isinstance(page, pages.CampaignsPage)

@pytest.mark.ui
def test_campaign_creation(campaigns_page):
	name = campaigns_page.create_campaign()
	campaigns_page.wait_until_loads()
	assert campaigns_page.campaign_exists(name)
	campaigns_page.delete_campaign(name)

@pytest.mark.ui
def test_delete_segment(audiences_page):
	name = audiences_page.create_segment()
	audiences_page.wait_until_loads()
	audiences_page.delete_segment(name)
	assert not audiences_page.segment_exists(name)

@pytest.mark.ui
def test_create_segment(audiences_page):
	name = audiences_page.create_segment()
	audiences_page.wait_until_loads()
	assert audiences_page.segment_exists(name)
	audiences_page.delete_segment(name)


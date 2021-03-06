"""
    Functional test 
    this file contains functional test for the logo functionality
"""
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_check_logo_in_homepage(self):
        start_time = time.time()
        time.sleep(10)
        # Marta has heard about a cool new online django-aula app. 
        # She goes to check out its homepage. 
        self.browser.get(self.live_server_url)

        # Marta checks the logo is in homepage
        # She tries to find a logo tag in homepage
        logo_tags = self.browser.find_elements_by_css_selector('div#companyLogo')
        self.assertEqual(len(logo_tags), 1)

        self.assertIn('Logo-JdA-131x1311.png', str(logo_tags[0].value_of_css_property('background-image')))

        self.fail('Finish the test!')

        """
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)
        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text  
        self.assertIn('To-Do', header_text)
        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')  
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        inputbox.send_keys('Buy peacock feathers')
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        # The page updates again, and now shows both items on her list
        # self.wait_for_row_in_list_table('1: Buy peacock feathers')
        # self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        #self.fail('Finish the test!')
        # She visits that URL - her to-do list is still there
        # Satisfied, she goes back to sleep
        """

if __name__ == '__main__':
    unittest.main(warnings='ignore')
from selenium import webdriver
from time import sleep


class SnapBot:
	def snapSite(self, url, save_path):
		driver = webdriver.Firefox()
		driver.get(url)
		sleep(10)
		driver.get_screenshot_as_file(save_path)
		driver.quit()
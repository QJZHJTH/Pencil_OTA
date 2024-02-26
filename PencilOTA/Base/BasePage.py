# -*-coding:utf-8 -*-
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self):
        self.caps = None
        self.driver = None

    def start_driver(self, ver):
        self.caps = {"platformName": "Android", "appium:platformVersion": ver, "appium:deviceName": "联想"}
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", self.caps)
        return self.driver

    def get_ele(self, loc):
        try:
            el = WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*loc))
            return el
        except Exception as e:
            return False

    def get_eles(self, loc):
        els = self.driver.find_elements(*loc)
        return els

    def click(self, el):
        el.click()


if __name__ == '__main__':
    bp = BasePage()
    bp.start_driver()
    print(bp.driver.device_time)

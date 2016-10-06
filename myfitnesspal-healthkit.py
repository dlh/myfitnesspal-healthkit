#!/usr/bin/env python
# Copyright (c) 2016 DLH. See LICENSE.txt for the MIT license.

import datetime
import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class LogInTimeoutError(Exception):
    pass

class MyFitnessPalHealthKit(object):
    def __init__(self, adblock_extension_path):
        options = webdriver.ChromeOptions()
        options.add_extension(adblock_extension_path)
        self.driver = webdriver.Chrome(chrome_options=options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.driver.close()
        except:
            pass

    def log_in(self):
        self.driver.get("http://www.myfitnesspal.com")
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/account/logout']")))
        except TimeoutException:
            raise LogInTimeoutError("You took too long to log in to your MyFitnessPal account")

    def crawl(self):
        # TODO add option to start from a specific date
        date = datetime.date.today()
        delta = datetime.timedelta(days=1)
        while True:
            self.driver.get("http://www.myfitnesspal.com/food/diary?date={0}".format(date.strftime("%Y-%m-%d")))
            self._force_update_meals()
            date -= delta

    def _force_update_meals(self):
        number_meals = self.driver.execute_script("return document.querySelectorAll('#diary-table tr.bottom').length")
        for i in range(number_meals):
            should_wait = self.driver.execute_script("""
                var meal = document.querySelectorAll('#diary-table tr.bottom')[{0}];
                var last_entry = meal.previousElementSibling.querySelector("a.js-show-edit-food");
                if (last_entry) {{
                    last_entry.click();
                    return true;
                }}
                return false;
            """.format(i))
            if should_wait:
                element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#edit_entry > input.button")))
                element.click()

def main(adblock_extension_path):
    try:
        with MyFitnessPalHealthKit(adblock_extension_path) as mfp:
            mfp.log_in()
            mfp.crawl()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <path-to-adblock-extension.crx>".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.flight_search_page import FlightSearchPage
from configs.config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

class TestFlightSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.flight_search_page = FlightSearchPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, Config.TIMEOUT)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_flight_search(self):
        self.flight_search_page.navigate_to_flights_page()
        self.flight_search_page.select_round_trip()
        self.flight_search_page.select_from_city("Bengaluru")
        self.flight_search_page.select_to_city("Dubai")
        self.flight_search_page.select_dates_duration()
        self.flight_search_page.adjust_duration(10)
        self.flight_search_page.initiate_search()

        # Add steps for validating prices and dates as in your original script
        time.sleep(10)  # Wait for the prices to load

        # Retrieve all the dates where the flight price is lower than the median price for that month
        prices = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='tripFareCal']//p[@class='calPrice']")))

        # Filter out non-numeric prices and convert to integers
        price_list = []
        for price in prices:
            price_text = price.text.replace('₹', '').replace(',', '')
            if price_text.isdigit():
                price_list.append(int(price_text))

        if not price_list:
            print("No valid prices found.")
            return

        median_price = sorted(price_list)[len(price_list) // 2]
        lower_prices_dates = [i for i, price in enumerate(prices) if price.text.replace('₹', '').replace(',', '').isdigit() and int(price.text.replace('₹', '').replace(',', '')) < median_price]

        # Step 9: From the dates obtained, select a weekend date (Saturday or Sunday), if available
        weekend_dates = []
        for date_index in lower_prices_dates:
            date_element = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='dateInnerSec']//p[@class='blackText']")))[date_index]
            date_text = date_element.text
            date_obj = datetime(2024, 12, int(date_text))
            if date_obj.weekday() >= 5:  # Saturday is 5 and Sunday is 6
                weekend_dates.append(date_index)

        # Step 10: If a weekend date is not available, choose the date with the lowest price
        selected_date_index = weekend_dates[0] if weekend_dates else lower_prices_dates[0]

        # Verify that at least one flight is available for the selected date
        selected_date_element = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='dateInnerSec']//p[@class='blackText']")))[selected_date_index]
        selected_date_element.click()

        # Confirm availability of flights
        time.sleep(5)
        flight_availability = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='fli-list one-way']//div[@class='fli-list-body-section']")))

        if flight_availability:
            print("Flights are available on the selected date.")
        else:
            print("No flights available on the selected date.")

if __name__ == "__main__":
    unittest.main()

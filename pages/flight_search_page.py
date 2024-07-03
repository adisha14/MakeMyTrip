from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from configs.config import Config
import time

class FlightSearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, Config.TIMEOUT)

    def navigate_to_flights_page(self):
        print("Navigating to flights page...")
        self.driver.get(Config.BASE_URL)

    def select_round_trip(self):
        print("Selecting round trip...")
        trip_type = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li[@data-cy='roundTrip']")))
        trip_type.click()

    def select_from_city(self, city):
        print(f"Selecting from city: {city}...")
        from_field = self.wait.until(EC.element_to_be_clickable((By.ID, "fromCity")))
        from_field.click()
        from_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='From']")))
        from_input.send_keys(city)
        city_option = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//p[text()='{city}, India']")))
        city_option.click()

    def select_to_city(self, city):
        print(f"Selecting to city: {city}...")
        to = self.wait.until(EC.element_to_be_clickable((By.ID, "toCity")))
        to.click()
        print("Choosing 'Planning a trip internationally'...")
        time.sleep(1)
        plan_international_trip = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "(//div[@class='makeFlex column intlFlightTile-autosuggest']//p)[1]")))
        print("Found")
        plan_international_trip.click()

        # Verify presence for 'list of suggestions'
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='listingSection']")))

        to_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@tabindex='0' and @class='flex-v fieldset'])[3]")))
        to_input.click()
        enter_city = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@placeholder='Enter City'])[2]")))
        enter_city.send_keys(city)
        city_option = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{city}, United Arab Emirates']")))
        city_option.click()

    def select_dates_duration(self):
        print("Selecting dates and duration...")
        dates_duration = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@tabindex='0' and @class='flex-v fieldset'])[4]")))
        dates_duration.click()
        travel_month = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='December, 2024']")))
        travel_month.click()

    def adjust_duration(self, days):
        print(f"Adjusting duration to {days} days...")
        slider = self.driver.find_element(By.XPATH, "//div[@class='rangeslider__handle']")
        actions = ActionChains(self.driver)
        actions.click_and_hold(slider).move_by_offset(37 * (days // 2), 0).release().perform()

    def initiate_search(self):
        print("Initiating search...")
        apply_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Apply']")))
        apply_button.click()
        search_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Search']")))
        search_button.click()

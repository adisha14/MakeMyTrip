from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from datetime import datetime, timedelta
import time

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# Step 1-Navigate to the "Flights" page
driver.get("https://www.makemytrip.com/flights/")
trip_type=wait.until(EC.presence_of_element_located((By.XPATH, "//li[@data-cy='roundTrip']")))
trip_type.click()
# Step 2-Select "From" as "Bangalore"
from_field = wait.until(EC.element_to_be_clickable((By.ID, "fromCity")))
from_field.click()
from_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='From']")))
from_input.send_keys("Bangalore")
bangalore = wait.until(EC.presence_of_element_located((By.XPATH, "(//p[text()='Bengaluru, India'])[1]")))
bangalore.click()
time.sleep(2)

# Step 3- Click on the "To" dropdown and choose "Planning a trip internationally"
to = wait.until(EC.element_to_be_clickable((By.ID, "toCity")))
to.click()

plan_international_trip = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='makeFlex column intlFlightTile-autosuggest']")))
plan_international_trip.click()
# Verify presence for 'list of suggestions'
wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='listingSection']")))

# Step 4- Set 'To' as 'Dubai'
to_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@tabindex='0' and @class='flex-v fieldset'])[3]")))
to_input.click()
enter_city = wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@placeholder='Enter City'])[2]")))
enter_city.send_keys("Dubai")
dubai = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Dubai, United Arab Emirates']")))
dubai.click()

# Step 5- Click on "DATES&DURATION"
datesDuration = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@tabindex='0' and @class='flex-v fieldset'])[4]")))
datesDuration.click()

# Step 6-Select "December 2024" and adjust the duration to 10 days.
travel_month = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='December, 2024']")))
travel_month.click()

slider = driver.find_element(By.XPATH, "//div[@class='rangeslider__handle']")

# Drag the slider handle to '10 days'
actions = ActionChains(driver)
actions.click_and_hold(slider).move_by_offset(37, 0).release().perform()

# Step 7- Initiate the search
apply_button=wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Apply']")))
apply_button.click()
search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Search']")))
search_button.click()

time.sleep(10)
# Step 8: Retrieve all the dates where the flight price is lower than the median price for that month
prices = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='tripFareCal']//p[@class='calPrice']")))

# Filter out non-numeric prices and convert to integers
price_list = []
for price in prices:
    price_text = price.text.replace('₹', '').replace(',', '')
    if price_text.isdigit():
        price_list.append(int(price_text))

if not price_list:
    print("No valid prices found.")
    driver.quit()
    exit()

median_price = sorted(price_list)[len(price_list) // 2]
lower_prices_dates = [i for i, price in enumerate(prices) if price.text.replace('₹', '').replace(',', '').isdigit() and int(price.text.replace('₹', '').replace(',', '')) < median_price]

# Step 9: From the dates obtained, select a weekend date (Saturday or Sunday), if available
weekend_dates = []
for date_index in lower_prices_dates:
    date_element = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='dateInnerSec']//p[@class='blackText']")))[date_index]
    date_text = date_element.text
    date_obj = datetime(2024, 12, int(date_text))
    if date_obj.weekday() >= 5:  # Saturday is 5 and Sunday is 6
        weekend_dates.append(date_index)

# Step 10: If a weekend date is not available, choose the date with the lowest price
selected_date_index = weekend_dates[0] if weekend_dates else lower_prices_dates[0]

# Verify that at least one flight is available for the selected date
selected_date_element = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='dateInnerSec']//p[@class='blackText']")))[selected_date_index]
selected_date_element.click()

# Confirm availability of flights
time.sleep(5)
flight_availability = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='fli-list one-way']//div[@class='fli-list-body-section']")))

if flight_availability:
    print("Flights are available on the selected date.")
else:
    print("No flights available on the selected date.")

# Close the driver
driver.quit()

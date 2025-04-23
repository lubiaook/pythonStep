import threading

import schedule
from flask import Flask, jsonify
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


app = Flask(__name__)

driver = None

def start_driver():
    global driver
    if driver is None:
        chrome_driver_path = './chromedriver'
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
        print("Driver started")

def stop_driver():
    global driver
    if driver:
        driver.quit()
        driver = None
        print("Driver stopped")

# Schedule tasks to start and stop the driver at specific times
schedule.every().day.at("06:00").do(start_driver)  # Start driver at 6 AM
schedule.every().day.at("18:30").do(stop_driver)  # Stop driver at 6:30 PM

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Flask route to get ship location
@app.route('/get_ship_location/<code>', methods=['GET'])
def getShipLocation(code):
    try:
        global driver
        # Ensure the driver is running
        if driver is None:
            start_driver()

        driver.get('https://www.shipxy.com/')

        # Wait for page load and find elements
        input_box = driver.find_element(By.XPATH, '//*[@id="txtKey"]')
        input_box.send_keys(code)
        search_button = driver.find_element(By.XPATH, '//*[@id="searchBtn"]')
        search_button.click()
        time.sleep(1)

        # Extract location data
        si_lat = driver.find_element(By.XPATH,'//*[@id="si__lat"]')
        si_lon = driver.find_element(By.XPATH,'//*[@id="si__lon"]')

        data = {
            'status': 1,
            'si_lat': si_lat.text,
            'si_lon': si_lon.text
        }

    except NoSuchElementException as e:
        # Handle element not found exception
        data = {'status': 0, 'error': 'Element not found'}
    except Exception as e:
        # Handle other exceptions
        data = {'status': 0, 'error': str(e)}

    return data

# Run schedule in a separate thread to handle start and stop tasks
if __name__ == "__main__":
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

    # Start the Flask app
    app.run(debug=True)

from time import sleep, strftime
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  
sleep(2)

def load_more():
    try:
        more_results = '//a[@class = "moreButton"]'
        driver.find_element(By.XPATH, more_results).click()
        print('sleeping.....')
        sleep(randint(25, 35))
    except Exception as e:
        print(f"Error during load_more: {e}")
        pass

def start_kayak(city_from, city_to, date_start, date_end):
    kayak_url = f'https://www.kayak.com/flights/{city_from}-{city_to}/{date_start}-flexible/{date_end}-flexible?sort=bestflight_a'
    driver.get(kayak_url)
    sleep(randint(8, 10))

    try:
        xp_popup_close = '//button[contains(@id,"dialog-close") and contains(@class,"Button-No-Standard-Style close ")]'
        popup_buttons = driver.find_elements(By.XPATH, xp_popup_close)
        if len(popup_buttons) > 0:
            popup_buttons[0].click()  
            print('Popup closed.')
        else:
            print('No popup found.')
    except Exception as e:
        print(f"Error closing popup: {e}")
        pass

    sleep(randint(60, 95))

    # Switch to cheapest results
    print('Switching to cheapest results...')
    cheap_results = '//a[@data-code = "price"]'
    driver.find_element(By.XPATH, cheap_results).click()
    sleep(randint(60, 90))

    # Scrape cheapest results only
    print('Starting cheapest flights scrape...')
    df_flights_cheap = page_scrape()
    df_flights_cheap['sort'] = 'cheap'
    sleep(randint(60, 80))

    # Save to CSV file
    df_flights_cheap.to_csv(f'search_backups//{strftime("%Y%m%d-%H%M")}_flights_{city_from}_{city_to}_{date_start}_{date_end}_cheap.csv', index=False)
    print('Saved data to CSV...')

def page_scrape():
    # Extract flight details from the page
    xp_sections = '//*[@class="section duration"]'
    sections = driver.find_elements(By.XPATH, xp_sections)
    sections_list = [value.text for value in sections]
    section_a_list = sections_list[::2]
    section_b_list = sections_list[1::2]
    
    if not section_a_list:
        raise SystemExit("No flight data found!")
    
    # Process each section of data
    a_duration = []
    a_section_names = []
    for n in section_a_list:
        a_section_names.append(''.join(n.split()[2:5]))
        a_duration.append(''.join(n.split()[0:2]))

    b_duration = []
    b_section_names = []
    for n in section_b_list:
        b_section_names.append(''.join(n.split()[2:5]))
        b_duration.append(''.join(n.split()[0:2]))

    # Extract other flight details (e.g., prices, stops, cities)
    xp_prices = '//a[@class="booking-link"]/span[@class="price option-text"]'
    prices = driver.find_elements(By.XPATH, xp_prices)
    prices_list = [price.text.replace('$', '') for price in prices if price.text != '']
    prices_list = list(map(int, prices_list))

    xp_stops = '//div[@class="section stops"]/div[1]'
    stops = driver.find_elements(By.XPATH, xp_stops)
    stops_list = [stop.text[0].replace('n', '0') for stop in stops]
    a_stop_list = stops_list[::2]
    b_stop_list = stops_list[1::2]

    xp_stops_cities = '//div[@class="section stops"]/div[2]'
    stops_cities = driver.find_elements(By.XPATH, xp_stops_cities)
    stops_cities_list = [stop.text for stop in stops_cities]
    a_stop_name_list = stops_cities_list[::2]
    b_stop_name_list = stops_cities_list[1::2]

    xp_schedule = '//div[@class="section times"]'
    schedules = driver.find_elements(By.XPATH, xp_schedule)
    hours_list = []
    carrier_list = []
    for schedule in schedules:
        hours_list.append(schedule.text.split('\n')[0])
        carrier_list.append(schedule.text.split('\n')[1])
    a_hours = hours_list[::2]
    a_carrier = carrier_list[::2]
    b_hours = hours_list[1::2]
    b_carrier = carrier_list[1::2]

    # Extract dates and weekdays
    xp_dates = '//div[@class="section date"]'
    dates = driver.find_elements(By.XPATH, xp_dates)
    dates_list = [value.text for value in dates]
    a_date_list = dates_list[::2]
    b_date_list = dates_list[1::2]
    a_day = [value.split()[0] for value in a_date_list]
    a_weekday = [value.split()[1] for value in a_date_list]
    b_day = [value.split()[0] for value in b_date_list]
    b_weekday = [value.split()[1] for value in b_date_list]

    # Creating the final DataFrame
    flights_df = pd.DataFrame({
        'Out Day': a_day,
        'Out Weekday': a_weekday,
        'Out Duration': a_duration,
        'Out Cities': a_section_names,
        'Return Day': b_day,
        'Return Weekday': b_weekday,
        'Return Duration': b_duration,
        'Return Cities': b_section_names,
        'Out Stops': a_stop_list,
        'Out Stop Cities': a_stop_name_list,
        'Return Stops': b_stop_list,
        'Return Stop Cities': b_stop_name_list,
        'Out Time': a_hours,
        'Out Airline': a_carrier,
        'Return Time': b_hours,
        'Return Airline': b_carrier,                           
        'Price': prices_list
    })

    flights_df['timestamp'] = strftime("%Y%m%d-%H%M")
    return flights_df

# Example usage
city_from = input('From which city? ')
city_to = input('Where to? ')
date_start = input('Search around which departure date? Please use YYYY-MM-DD format only ')
date_end = input('Return when? Please use YYYY-MM-DD format only ')

for n in range(0, 5):
    start_kayak(city_from, city_to, date_start, date_end)
    print(f'Iteration {n} was complete @ {strftime("%Y%m%d-%H%M")}')
    sleep(60 * 60 * 4)  # Sleep between iterations

driver.quit()

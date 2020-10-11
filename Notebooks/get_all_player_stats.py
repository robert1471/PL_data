# import selenium and start a headless window
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import time
import pandas as pd
from bs4 import BeautifulSoup
import lxml

# chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# get web page
# driver = webdriver.Chrome()
driver = webdriver.Chrome(executable_path="/Users/Robert/PycharmProjects/FPL_Data/Notebooks/chromedriver.exe")


def get_on_player_page(i):
    # define root website
    driver.get("https://fbref.com/en/comps/9/3232/stats/2019-2020-Premier-League-Stats")
    time.sleep(4)

    # find data and match buttons
    search_table = driver.find_element_by_id("all_stats_standard")
    match_buttons = search_table.find_elements_by_link_text("Matches")

    # define actions
    actions = ActionChains(driver)

    # scroll to element
    try:
        actions.move_to_element(match_buttons[i]).perform()
    except:
        pass
    time.sleep(2)

    # click on element
    move = actions.click(match_buttons[i])
    move.perform()
    time.sleep(2)

    # change tables
    table_buttons = driver.find_elements(By.CLASS_NAME, "filter")
    filters = table_buttons[1].find_elements(By.TAG_NAME, "a")

    # define actions
    actions = ActionChains(driver)

    # scroll to element
    try:
        actions.move_to_element(filters[5]).perform()
    except:
        pass
    time.sleep(2)

    # click on element
    move = actions.click(filters[5])
    move.perform()
    time.sleep(2)

    # works!


# get_on_player_page(2)

########################################################################################################################

def ummm_get_stats(i):
    # get root directory
    driver.get("https://fbref.com/en/comps/9/3232/stats/2019-2020-Premier-League-Stats")
    time.sleep(2)

    # find data and match buttons
    search_table = driver.find_element_by_id("all_stats_standard")
    match_buttons = search_table.find_elements_by_link_text("Matches")

    # define actions
    actions = ActionChains(driver)

    # scroll to element
    try:
        actions.move_to_element(match_buttons[i]).perform()
    except:
        pass
    time.sleep(2)

    # click on element
    move = actions.click(match_buttons[i])
    move.perform()
    time.sleep(2)

    # get matchlogs table
    new_table = driver.find_element_by_id("all_matchlogs_all")
    rows = new_table.find_elements(By.TAG_NAME, "tr")

    # empty dict to form data structure from table and then converted to pandas df
    df_prep = {}
    for i, row in enumerate(rows):
        df_prep[i] = {}

        if i == 1:
            # get data from th in table header
            titles = row.find_elements(By.TAG_NAME, "th")
            for k, title in enumerate(titles):
                df_prep[i][k] = titles[k].text

        elif i != 0:
            # get dates from th in table body
            dates = row.find_elements(By.TAG_NAME, "th")
            df_prep[i][0] = dates[0].text

            # get data
            got_em = row.find_elements(By.TAG_NAME, "td")
            if not got_em == []:
                for j, value in enumerate(got_em):
                    df_prep[i][j + 1] = got_em[j].text

    x = pd.DataFrame(df_prep).transpose()
    x.dropna(axis=0, thresh=2, inplace=True)
    x.dropna(axis=1, thresh=2, inplace=True)
    x = x.dropna(subset=[35])

    print(x)
    return x


#######################################################################################################################


def get_all_player_stats(writer, tab_num):

    # change tables
    # table_buttons 1 is constant
    table_buttons = driver.find_elements(By.CLASS_NAME, "filter")
    filters = table_buttons[1].find_elements(By.TAG_NAME, "a")

    # define actions
    actions = ActionChains(driver)

    # scroll to element
    try:
        actions.move_to_element(filters[tab_num]).perform()
    except:
        pass

    time.sleep(1)
    # click on element
    move = actions.click(filters[tab_num])
    move.perform()
    time.sleep(1)

    # get matchlogs table
    new_table = driver.find_element_by_id("all_matchlogs_all")
    html = new_table.get_attribute('innerHTML')
    df = pd.read_html(html)
    df[0].to_excel(writer, sheet_name=f"table_{tab_num}")

bad_bois = [522]

# 97,

for player in bad_bois:
    with pd.ExcelWriter(f'player_{player}.xlsx') as writer:
        # define root website
        driver.get("https://fbref.com/en/comps/9/3232/stats/2019-2020-Premier-League-Stats")
        time.sleep(1.25)

        # find data and match buttons
        search_table = driver.find_element_by_id("all_stats_standard")
        match_buttons = search_table.find_elements_by_link_text("Matches")

        # define actions
        actions = ActionChains(driver)

        # scroll to element
        try:
            actions.move_to_element(match_buttons[player]).perform()
        except:
            pass
        time.sleep(0.75)

        # click on element
        move = actions.click(match_buttons[player])
        move.perform()
        time.sleep(0.75)

        for i in range(7):
            get_all_player_stats(writer=writer, tab_num=i)


# y = ummm_get_stats(2)
# y.to_csv("tammy_test.csv", encoding="ansi")
# rks for tammy on one table

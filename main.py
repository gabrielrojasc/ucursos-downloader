import os
import sys
from os import path

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import (get_courses, get_links, get_password, get_path,
                   get_semester, get_username)


def login(browser, wait, username, password):
    browser.find_element_by_name("username").send_keys(username)
    wait.until(EC.text_to_be_present_in_element_value((By.NAME, "username"), username))
    browser.find_element_by_name("password").send_keys(password)
    wait.until(EC.text_to_be_present_in_element_value((By.NAME, "password"), password))
    browser.find_element_by_xpath('//*[@id="upform"]/form/dl/input').click()
    try:
        wait.until(EC.presence_of_element_located((By.ID, "favoritos")))
    except:
        print("Wrong username or password")
        browser.close()
        sys.exit()


def main():
    semester = get_semester()
    courses = get_courses()
    PATH = get_path()

    len_args = len(sys.argv)
    if len_args > 1:
        username = sys.argv[1]
    else:
        username = get_username()
    if len_args > 2:
        password = sys.argv[2]
    else:
        password = get_password()

    links = get_links(courses, semester[0], semester[1])

    browser = webdriver.Safari()
    wait = WebDriverWait(browser, 5)
    browser.get("https://www.u-cursos.cl")
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    login(browser, wait, username, password)

    cookies = browser.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie["name"], cookie["value"])

    for k in range(len(links)):
        browser.get(links[k])
        wait.until(EC.presence_of_element_located((By.ID, "favoritos")))
        course = courses[k][:6]
        course_name = " ".join(
            browser.find_element_by_xpath("/html/body/div[2]/div/h1/span").text.split()
        )
        course += " - " + course_name
        print(f"\n{course}")
        course_path = f"{PATH}/{course}"
        if not path.exists(course_path):
            os.makedirs(course_path)
            print(f"Directory {course_path} created")
        row = browser.find_elements_by_xpath('//*[@id="materiales"]/tbody')
        for i in range(len(row)):
            for row2 in row[i].find_elements_by_tag_name("tr"):
                row3_link = row2.find_elements_by_xpath(
                    'td/h1/a[contains(@class,"baja")]'
                )
                row3_name = row2.find_elements_by_xpath(
                    'td/h1/a[img[contains(@class, "icono")]]'
                )
                for n in range(len(row3_link)):
                    file_name = row3_name[n].get_attribute("textContent")
                    file_name = file_name.replace("\n", "")
                    file_name = file_name.replace("\t", "")
                    file_name = file_name.replace("/", ":")
                    dlink = row3_link[n].get_attribute("href")
                    folder_name = (
                        row[i - 1]
                        .find_element_by_xpath('tr[contains(@class,"separador")]')
                        .text
                    )
                    folder_name = folder_name.replace("\n", "")
                    folder_name = folder_name.replace("\t", "")
                    if folder_name:
                        folder_name += "/"
                        if not path.exists(f"{PATH}/{course}/{folder_name}"):
                            os.mkdir(f"{PATH}/{course}/{folder_name}")
                    r = s.get(dlink)
                    if path.exists(f"{PATH}/{course}/{folder_name}{file_name}"):
                        print(f"Updating: {file_name}")
                    else:
                        print(f"Downloading: {file_name}")
                    file = open(f"{PATH}/{course}/{folder_name}{file_name}", "w+b")
                    file.write(r.content)
                    file.close()

    browser.close()
    s.close()


if __name__ == "__main__":
    main()

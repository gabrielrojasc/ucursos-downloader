#!./env/bin/python3
# -*- coding: utf-8 -*-
import requests, os, time, getpass, sys
from selenium import webdriver

def getfiles():
  global semester, courses, PATH
  try:
    semester = open("semester.txt", "r+")
  except FileNotFoundError:
    semester = open("semester.txt", "w+")
  try:
    courses = open("courses.txt", "r+")
  except FileNotFoundError:
    courses = open("courses.txt", "w+")

  try:
    PATH = open("PATH.txt","r").readlines()[0][:-1]
  except FileNotFoundError:
    print('Se debe crear archivo "PATH.txt:" con el path donde se quieran \
      descargar los achivos')
    sys.exit(1)


  semester = semester.readlines()
  courses = courses.readlines()

  if semester == []:
    semester = open("semester.txt", "r+")
    semester.write(input("Año: ")+"\n")
    semester.write(input("Semestre: "))
    getcourses()

  if courses == []:
    courses = open("courses.txt", "r+")
    ncourses = int(input("Numero de ramos: "))
    for _ in range(ncourses):
      courses.write(input("Cusos({codigo} {sección}): ")+"\n")
    getcourses()

def getlogin():
  global username, password
  username = input("username: ")
  password = getpass.getpass()
      

getfiles()
getlogin()
i = 0
links = list()
while i < len(courses):
  links.append(f"https://www.u-cursos.cl/ingenieria/{semester[0].rstrip()}/\
    {semester[1]}/{courses[i][0:6]}/{courses[i][7]}/material_docente/")
  i+=1

browser=webdriver.Safari()
browser.get("https://www.u-cursos.cl")
time.sleep(1)
browser.find_element_by_name("username").send_keys(f"{username}")
browser.find_element_by_name("password").send_keys(f"{password}")
browser.find_element_by_xpath('//*[@id="upform"]/form/dl/input').click()
time.sleep(2)

cookies = browser.get_cookies()
s = requests.Session()
for cookie in cookies:
  s.cookies.set(cookie['name'], cookie['value'])

try:
  for k in range(len(links)):
    browser.get(links[k])
    time.sleep(1)
    course = courses[k][0:6]
    course_name = " ".join(browser.find_element_by_xpath('/html/body/div[2]/div/\
      h1/span').text.split())
    course += " - "+course_name
    try:
      os.mkdir(f"{PATH}/{course}")
    except:
      pass
    row = browser.find_elements_by_xpath('//*[@id="materiales"]/tbody')
    for i in range(len(row)):
      for row2 in row[i].find_elements_by_tag_name('tr'):
        for row3 in row2.find_elements_by_xpath('td[3]'):
            row4 = row3.find_elements_by_xpath('h1/a')
            file_name = " ".join(row4[0].text.split())
            for j in range(len(file_name)):
              if file_name[j] == "/":
                file_name = file_name[:j]+":"+file_name[j+1:]
            dlink = row4[2].get_attribute('href')[:-8]
            folder_name = row[i-1].find_element_by_xpath('tr[1]/td[2]').text 
            if folder_name != "":
              folder_name += "/"
              try:
                os.mkdir(f"{PATH}/{course}/{folder_name}")
              except:
                pass
            r = s.get(dlink)
            try:
              file = open(f'{PATH}/{course}/{folder_name}{file_name}', 'r+b')
            except FileNotFoundError:
              file = open(f'{PATH}/{course}/{folder_name}{file_name}', 'w+b')

            if file.read() != r.content:
              file.write(r.content)

  browser.close()

except Exception:
  print("Wrong username or password")
  browser.close()
  sys.exit()

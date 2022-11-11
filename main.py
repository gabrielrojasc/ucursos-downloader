# -*- coding: utf-8 -*-
import sys
import os
from os import path
from requests_html import HTMLSession
from utils import (
    get_courses,
    get_semester,
    get_path,
    get_links,
    get_password,
    get_username,
)


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

    session = HTMLSession()

    # login
    payload = {"username": username, "password": password}
    session.get("https://www.u-cursos.cl")
    r = session.post("https://www.u-cursos.cl/upasaporte/adi", data=payload)
    breakpoint()
    # TODO: check if login failed

    for k in range(len(links)):
        r = session.get(links[k])
        r.html.render()
        html = r.html
        course = courses[k][:6]
        breakpoint()
        course_name = " ".join(html.xpath("/html/body/div[2]/div/h1/span").text.split())
        course += " - " + course_name
        print(f"\n{course}")
        try:
            os.mkdir(f"{PATH}/{course}")
        except FileExistsError:
            # directory already exists
            pass
        row = html.xpath('//*[@id="materiales"]/tbody')
        for i in range(len(row)):
            for row2 in row[i].find("tr"):
                row3_link = row2.xpath('td/h1/a[contains(@class,"baja")]')
                row3_name = row2.xpath('td/h1/a[img[contains(@class, "icono")]]')
                for n in range(len(row3_link)):
                    file_name = row3_name[n].attrs.get("textContent")
                    file_name = file_name.replace("\n", "")
                    file_name = file_name.replace("\t", "")
                    file_name = file_name.replace("/", ":")
                    dlink = row3_link[n].get_attribute("href")
                    folder_name = (
                        row[i - 1].xpath('tr[contains(@class,"separador")]').text
                    )
                    folder_name = folder_name.replace("\n", "")
                    folder_name = folder_name.replace("\t", "")
                    if folder_name:
                        folder_name += "/"
                        if not path.exists(f"{PATH}/{course}/{folder_name}"):
                            os.mkdir(f"{PATH}/{course}/{folder_name}")
                    r = session.get(dlink)
                    if path.exists(f"{PATH}/{course}/{folder_name}{file_name}"):
                        print(f"Updating: {file_name}")
                    else:
                        print(f"Downloading: {file_name}")
                    file = open(f"{PATH}/{course}/{folder_name}{file_name}", "w+b")
                    file.write(r.content)
                    file.close()


if __name__ == "__main__":
    main()

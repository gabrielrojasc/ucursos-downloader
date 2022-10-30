import sys
import getpass
from os import path


def get_courses() -> list:
    if path.exists(path.join(sys.path[0], "courses.txt")):
        courses = open(path.join(sys.path[0], "courses.txt"), "r+")
        if courses_lines := courses.readlines():
            courses.close()
            return courses_lines
    else:
        courses = open(path.join(sys.path[0], "courses.txt"), "w+")

    try:
        n_courses = int(input("Numero de ramos: "))
    except ValueError:
        print("El numero de ramos debe ser un numero (int)")
    for _ in range(n_courses):
        course = input("Cusos({codigo}-{sección}): ")
        courses.write(course.strip() + "\n")
    courses.close()
    return get_courses()


def get_semester() -> list:
    if path.exists(path.join(sys.path[0], "semester.txt")):
        semester = open(path.join(sys.path[0], "semester.txt"), "r+")
        if semester_lines := semester.readlines():
            semester.close()
            return semester_lines
    else:
        semester = open(path.join(sys.path[0], "semester.txt"), "w+")

    year = input("Año: ")
    semester.write(year + "\n")
    sem = input("Semestre: ")
    semester.write(sem + "\n")
    semester.close()
    return get_semester()


def get_path() -> list:
    if path.exists(path.join(sys.path[0], "PATH.txt")):
        return open(path.join(sys.path[0], "PATH.txt"), "r").readlines()[0][:-1]
    else:
        print(
            'Se debe crear archivo "PATH.txt:" con el path donde se quieran '
            "descargar los achivos"
        )
        sys.exit(1)


def get_username() -> str:
    username = input("username: ")
    return username


def get_password() -> str:
    password = getpass.getpass()
    return password


def get_links(courses: list, semester_year: int, semester_number: int) -> list:
    links = list()
    semester_year = semester_year.strip()
    semester_number = semester_number.strip()
    for i in range(len(courses)):
        links.append(
            f"https://www.u-cursos.cl/ingenieria/{semester_year}/{semester_number}/"
            f"{courses[i][:6]}/{courses[i][7]}/material_docente/"
        )
    return links

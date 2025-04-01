from dataclasses import dataclass, asdict
import requests
from bs4 import BeautifulSoup
import csv
from typing import List


URL = "https://mate.academy/study"


def get_html(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_count: int = 0


def parse_courses(html: str) -> List[Course]:
    soup = BeautifulSoup(html, "html.parser")
    courses_container = soup.find(
        "div", class_="CareerPath_careerPathItem__f_p59"
    )

    courses = []
    course_elements = courses_container.find_all(
        "h2", class_="typography_platformH2__0YzKL"
    )

    for course in course_elements:
        name_tag = course.find("h3")
        if not name_tag:
            continue

        name = name_tag.text.strip()

        short_description = (
            course.find("p")
            .text.strip() if course.find("p") else "No description"
        )
        duration = (
            course.find("span", class_="duration").text.strip()
            if course.find("span", class_="duration")
            else "No duration"
        )

        modules_count = len(course.find_all("p", class_="Tag_text__WWT2B"))

        courses.append(
            Course(
                name=name,
                short_description=short_description,
                duration=duration,
                modules_count=modules_count,
            )
        )

    return courses


def get_all_courses() -> list[Course]:
    html = get_html(URL)
    courses = parse_courses(html)

    # Перевіряємо, які курси реально парсяться
    course_names = [course.name for course in courses]
    print("✅ Отримані курси:", course_names)

    return courses


def save_courses_to_csv(
        courses: List[Course], filename: str = "courses.csv"
) -> None:
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "name",
                "short_description",
                "duration",
                "modules_count",
                "topics_count",
            ],
        )
        writer.writeheader()
        for course in courses:
            writer.writerow(asdict(course))


if __name__ == "__main__":
    courses = get_all_courses()
    save_courses_to_csv(courses)
    for course in courses:
        print(course)

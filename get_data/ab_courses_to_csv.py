# Save all courses for a given semester to a CSV file
# Uses askBanner to get the courses, allowing for parsing of any semester

import requests
from bs4 import BeautifulSoup
import csv
import parse_course as pc


def get_courses(session: str):
    # Get the page. If form data (session) is sent as .
    data = f"session={session}&dept=&instr=&type=&day=&time=&unit=&format=&division_search=&crse_level_search=&submit=Submit"
    page = requests.post("https://aisapps.vassar.edu/cgi-bin/courses.cgi", data=data)

    # Get all divs
    soup = BeautifulSoup(page.content, 'html.parser')
    div_courses = soup.find_all("div")

    processed_courses = []
    for div_course in div_courses:
        raw_course = div_course.text
        try:
            course = pc.parse_course(raw_course)
        except Exception as e:
            print(f"Error parsing course: {e}")
            print(f"Raw course: {raw_course}")
            print(f"skipping this course...")
            continue

        processed_courses.append(course)

    return processed_courses


def save_courses_for_sem(semester, path):
    all_courses = get_courses(semester)
    print(f"Found {len(all_courses)} courses for {semester}")
    # Write to CSV
    keys = all_courses[0].keys()
    with open(path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(all_courses)

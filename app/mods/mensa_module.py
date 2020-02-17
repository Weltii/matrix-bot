import datetime
import re
import requests


def search_current_day_block(spliced_content):
    ret = []
    block_found = False
    first_line = 0
    last_line = 0
    current_date = datetime.datetime.now()
    current_date = str(current_date.strftime("%d.%m.%Y"))

    for x in range(len(spliced_content)):
        row = spliced_content[x]
        if block_found:
            if re.search("\\d{1,2}\\.\\d{1,2}\\.\\d{4}", row):
                last_line = x
                break
        if current_date in row:
            block_found = True
            first_line = x
    for x in range(last_line - first_line):
        ret.append(spliced_content[x + first_line])
    return ret

def get_meals(spliced_content):
    meals = ""
    for row in spliced_content:
        if re.search("<strong>.*<\\/strong>|(\\d+,\\d+ €\\ ?\\/?\\ ?)", row):
            meals += (
                re.sub(
                    "<.{0,10}>|\\(\\w*,&.*;\\w+\\)|\\(\\w{0,3}\\)", "", row
                ).strip()
                + "\n"
            )
    return meals

def get_mensa_menu(input: str) -> str:
    response = requests.get(
        "https://www.studentenwerk.sh/de/essen/standorte/luebeck/mensa-luebeck/speiseplan.html"
    )
    spliced_content = response.text.split("\n")
    meals = get_meals(search_current_day_block(spliced_content))
    if 0 >= len(meals):
        current_day = str(datetime.datetime.now().now().strftime("%d.%m.%Y"))
        meals = f"We cannot find any meal for the {current_day}"
    return meals


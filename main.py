import requests
from bs4 import BeautifulSoup
import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import html


def render_template(template_file, tpl_vars):
    template = ""
    with open(template_file, "r") as fh:
        template = fh.read()

    for k, v in tpl_vars.items():
        tk = "<!--{{{{{s}}}}}-->".format(s=k)  # 😭
        template = template.replace(tk, html.escape(str(v)))

    return template


def render_jinja_template(template_file, tpl_vars):
    tpl_dir = os.path.dirname(template_file)
    tpl_name = os.path.basename(template_file)

    file_loader = FileSystemLoader(tpl_dir)
    env = Environment(loader=file_loader)

    template = env.get_template(tpl_name)
    return template.render(**tpl_vars)


def main():
    URL = "https://coronavirus.bg/"
    # MY_EMAIL = os.environ["SENDER"]
    # MY_PASSWORD = os.environ["PASSWORD"]
    # RECIPIENT = os.environ["RECIPIENT"]

    MY_EMAIL = os.environ['SENDER']
    MY_PASSWORD = os.environ['PASSWORD']
    RECIPIENT = os.environ['RECIPIENT']

    resnponse = requests.get(URL)

    covid_bot = resnponse.text

    soup = BeautifulSoup(covid_bot, "html.parser")

    header = soup.find(name="div", class_="row statistics-header-wrapper")
    new_cases = header.find("h1").text
    # print(new_cases)

    stats = soup.find(name="div", class_="row statistics-header-wrapper")
    stats_text = stats.find("span").text
    # print(stats_text)

    dayly_tests = soup.find(name="div", class_="col-lg-3 col-md-6")
    tests_overall = format(int(dayly_tests.find(
        name="p", class_="statistics-value").text), ",")
    tests_lable = dayly_tests.find(name="p", class_="statistics-label").text
    tests_value = dayly_tests.find(name="p", class_="statistics-subvalue").text
    tests_sublable = dayly_tests.find(name="p", class_="statistics-sublabel").text
    # print(tests_value)

    covid_overall = dayly_tests.find_next_sibling(
        name="div", class_="col-lg-3 col-md-6")
    covid_overall_confirmed_value = format(int(covid_overall.find(
        name="p", class_="statistics-value confirmed").text), ",")
    covid_overall_lable = covid_overall.find(
        name="p", class_="statistics-label").text
    covid_overall_value = covid_overall.find(
        name="p", class_="statistics-subvalue").text
    covid_overall_sublable = covid_overall.find(
        name="p", class_="statistics-sublabel").text

    healed = covid_overall.find_next_sibling(
        name="div", class_="col-lg-3 col-md-6")
    healded_value_overall = format(
        int(healed.find(name="p", class_="statistics-value healed").text), ",")
    healded_lable = healed.find(name="p", class_="statistics-label").text
    healded_value = healed.find(name="p", class_="statistics-subvalue").text
    healded_sublable = healed.find(name="p", class_="statistics-sublabel").text

    hospitalized = healed.find_next_sibling(name="div", class_="col-lg-3 col-md-6")
    hospitalized_value_overall = format(
        int(hospitalized.find(name="p", class_="statistics-value").text), ",")
    hospitalized_lable = hospitalized.find(
        name="p", class_="statistics-label").text
    hospitalized_value = hospitalized.find(
        name="p", class_="statistics-subvalue").text
    hospitalized_sublable = hospitalized.find(
        name="p", class_="statistics-sublabel").text


    deaths = hospitalized.find_next_sibling(name="div", class_="col-lg-3 col-md-6")
    deaths_value_overall = format(
        int(deaths.find(name="p", class_="statistics-value deceased").text), ",")
    deaths_lable = deaths.find(name="p", class_="statistics-label").text
    deaths_value = deaths.find(name="p", class_="statistics-subvalue").text
    deaths_sublable = deaths.find(name="p", class_="statistics-sublabel").text
    # print(deaths_lable, deaths_value, deaths_sublable)

    vaccine = deaths.find_next_sibling(name="div", class_="col-lg-3 col-md-6")
    vaccine_value_overall = format(
        int(vaccine.find(name="p", class_="statistics-value").text), ",")
    vaccine_lable = vaccine.find(name="p", class_="statistics-label").text
    vaccine_value = vaccine.find(name="p", class_="statistics-subvalue").text
    vaccine_sublable = vaccine.find(name="p", class_="statistics-sublabel").text

    vaccinated = vaccine.find_next_sibling(name="div", class_="col-lg-3 col-md-6")
    vaccinated_value_overall = vaccinated.find(
        name="p", class_="statistics-value").text
    vaccinated_lable = vaccinated.find(name="p", class_="statistics-label").text
    vaccinated_value = vaccinated.find(name="p", class_="statistics-subvalue").text
    vaccinated_sublable = vaccinated.find(
        name="p", class_="statistics-sublabel").text

    newly_hospitalized = vaccinated.find_next_sibling(
        name="div", class_="col-lg-3 col-md-6")
    newly_hospitalized_day_value = newly_hospitalized.find(
        name="p", class_="statistics-value skyblue").text
    newly_hospitalized_lable = newly_hospitalized.find(
        name="p", class_="statistics-label").text
    newly_hospitalized_subvalue = newly_hospitalized.find(
        name="p", class_="statistics-subvalue").text
    newly_hospitalized_sublable = newly_hospitalized.find(
        name="p", class_="statistics-sublabel").text
    # print(newly_hospitalized_day_value, newly_hospitalized_lable, newly_hospitalized_subvalue, newly_hospitalized_sublable)

    new_cases_persentage = round((int(tests_value.replace(" ", "")) - (int(tests_value.replace(
        " ", "")) - int(new_cases.replace(" ", "")))) / int(tests_value.replace(" ", "")) * 100, 2)


    msg = MIMEMultipart()
    msg['Subject'] = "Ковид дневна статистика"

    untrusted = "<script>alert('wooo')</script>"

    tpl_vars = {
        "STATUS": stats_text,
        "NEW_CASES": new_cases,
        "NEW_CASES_PERC": new_cases_persentage,
        "TESTS_OVERALL": tests_overall,
        "TESTS_LABLE": tests_lable,
        "TESTS_VALUE": tests_value,
        "TESTS_SUBLABLE": tests_sublable,
        "COVID_OVERALL_CONFIRMED_VALUE": covid_overall_confirmed_value,
        "COVID_OVERALL_LABLE": covid_overall_lable,
        "COVID_OVERALL_VALUE": covid_overall_value,
        "COVID_OVERALL_SUBLABLE": covid_overall_sublable,
        "HEALDED_VALUE_OVERALL": healded_value_overall,
        "HEALDED_LABLE": healded_lable,
        "HEALDED_VALUE": healded_value,
        "HEALDED_SUBLABLE": healded_sublable,
        "HOSPITALIZED_VALUE_OVERALL": hospitalized_value_overall,
        "HOSPITALIZED_LABLE": hospitalized_lable,
        "HOSPITALIZED_VALUE": hospitalized_value,
        "HOSPITALIZED_SUBLABLE": hospitalized_sublable,
        "DEATHS_VALUE_OVERALL": deaths_value_overall,
        "DEATHS_LABLE": deaths_lable,
        "DEATHS_VALUE": deaths_value,
        "DEATHS_SUBLABLE": deaths_sublable,
        "VACCINE_VALUE_OVERALL": vaccine_value_overall,
        "VACCINE_LABLE": vaccine_lable,
        "VACCINE_VALUE": vaccine_value,
        "VACCINE_SUBLABLE": vaccine_sublable,
        "VACCINATED_VALUE_OVERALL": vaccinated_value_overall,
        "VACCINATED_LABLE": vaccinated_lable,
        "VACCINATED_VALUE": vaccinated_value,
        "VACCINATED_SUBLABLE": vaccinated_sublable,
        "NEWLY_HOSPITALIZED_DAY_VALUE": newly_hospitalized_day_value,
        "NEWLY_HOSPITALIZED_LABLE": newly_hospitalized_lable,
        "NEWLY_HOSPITALIZED_SUBVALUE": newly_hospitalized_subvalue,
        "NEWLY_HOSPITALIZED_SUBLABLE": newly_hospitalized_sublable,
        "OTHER": untrusted,
    }

    email_body = render_template("views/email.html", tpl_vars)
    # email_body = render_jinja_template("views/email.jinja.html", tpl_vars)

    print(email_body)
    sys.exit(0)

    msg.attach(MIMEText(email_body, 'html'))
    text = msg.as_string()

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=RECIPIENT,
                            msg=text)


if __name__ == '__main__':
    main()

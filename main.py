import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


URL = "https://coronavirus.bg/"
# MY_EMAIL = os.environ["SENDER"]
# MY_PASSWORD = os.environ["PASSWORD"]
# RECIPIENT = os.environ["RECIPIENT"]

MY_EMAIL = "spoderinio@gmail.com"
MY_PASSWORD = "sam0zapersonal!"
RECIPIENT = "spoder@gmail.com"

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

message = (
    f"Subject: Ковид дневна статистика\n\n{stats_text}\n{new_cases} Нови случаи. Които се равняват на {new_cases_persentage}% от направените за деня тестове.\n{tests_overall} {tests_lable} {tests_value} {tests_sublable}.\n"
    f"{covid_overall_confirmed_value} {covid_overall_lable}, {covid_overall_value} {covid_overall_sublable}.\n"
    f"{healded_value_overall} {healded_lable}, {healded_value} {healded_sublable}.\n"
    f"{hospitalized_value_overall} {hospitalized_lable}, {hospitalized_value} {hospitalized_sublable}.\n"
    f"{deaths_value_overall} {deaths_lable}, {deaths_value} {deaths_sublable}.\n"
    f"{vaccine_value_overall} {vaccine_lable}, {vaccine_value} {vaccine_sublable}.\n"
    f"{vaccinated_value_overall} {vaccinated_lable}, {vaccinated_value} {vaccinated_sublable}.\n"
    f"{newly_hospitalized_day_value} {newly_hospitalized_lable} {newly_hospitalized_subvalue} {newly_hospitalized_sublable}.\n"
    "*Ваксинирани са всички лица със завършен ваксинационен курс.").encode("utf-8")

# with smtplib.SMTP("smtp.gmail.com") as connection:
#     connection.starttls()
#     connection.login(user=MY_EMAIL, password=MY_PASSWORD)
#     connection.sendmail(from_addr=MY_EMAIL,
#                         to_addrs=RECIPIENT,
#                         msg=message)

msg = MIMEMultipart()
html = '''\
<!DOCTYPE html>
<html>

<body>
    <h2>''' + str(stats_text) + '''</h2>
    <ul>
        <li><em>''' + str(new_cases) + '''</em> Нови случаи. Които се равняват на <b><em>''' + str(new_cases_persentage) + '''%</em></b> от направените за деня тестове.</li>
        <li><em>''' + str(tests_overall) + '''</em> ''' + str(tests_lable) + ''' <b><em></em>''' + str(tests_value) + '''</b> ''' + str(tests_sublable) + '''.
        </li>
        <li><em>''' + str(covid_overall_confirmed_value) + '''</em> ''' + str(covid_overall_lable) + ''', <b><em>''' + str(covid_overall_value) + '''</em></b> ''' + str(covid_overall_sublable) + '''.</li>
        <li><em>''' + str(healded_value_overall) + '''</em> ''' + str(healded_lable) + ''', <b><em>''' + str(healded_value) + '''</em></b> ''' + str(healded_sublable) + '''.</li>
        <li><em>''' + str(hospitalized_value_overall) + '''</em> ''' + str(hospitalized_lable) + ''', <b><em>''' + str(hospitalized_value) + '''</em></b> ''' + str(hospitalized_sublable) + '''.</li>
        <li><em>''' + str(deaths_value_overall) + '''</em> ''' + str(deaths_lable) + ''', <b><em>''' + str(deaths_value) + '''</em></b> ''' + str(deaths_sublable) + '''.</li>
        <li><em>''' + str(vaccine_value_overall) + '''</em>''' + str(vaccine_lable) + ''', <b><em>''' + str(vaccine_value) + '''</em></b> ''' + str(vaccine_sublable) + '''.</li>
        <li><em>''' + str(vaccinated_value_overall) + '''%</em> ''' + str(vaccinated_lable) + ''', <b>''' + str(vaccinated_value) + '''%</b> ''' + str(vaccinated_sublable) + '''.</li>
        <li><em>''' + str(newly_hospitalized_day_value) + '''</em> ''' + str(newly_hospitalized_lable) + ''' <b>''' + str(newly_hospitalized_subvalue) + '''%</b> ''' + str(newly_hospitalized_sublable) + '''.</li>
        <h3>*Ваксинирани са всички лица със <b><em>завършен</em></b> ваксинационен курс.</h3>
    </ul>

</body>

</html>'''

msg.attach(MIMEText(html, 'html'))
text = msg.as_string()

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    connection.sendmail(from_addr=MY_EMAIL,
                        to_addrs=RECIPIENT,
                        msg=text)

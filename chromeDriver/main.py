import os
import time
from datetime import datetime, timedelta

import config

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Получаем путь к текущей директории
current_directory = os.path.dirname(__file__)

chrome_driver_path = os.path.join(current_directory, 'chromedriver.exe')

service = Service(executable_path=chrome_driver_path)

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

# Данные для входа
user_email = config.user_email
user_password = config.user_password

admin_email = config.admin_email
admin_password = config.admin_password

login_url = "https://localhost:7251/Account/Login"
tsCreateUrl = "https://localhost:7251/TS/CreateTS?DepartmentName=%D0%9E%D1%82%D0%B4%D0%B5%D0%BB%20%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82%20%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9%20%D0%B8%20%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%20%D0%BE%D0%B1%D1%89%D0%B5%D0%B3%D0%BE%20%D0%BD%D0%B0%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D1%8F"
tsIndexUrl = "https://localhost:7251/TS"
adminIndexUrl = "https://localhost:7251/Admin"
mainUrl = "https://localhost:7251/"

file_path_forTs = config.file_path_forTs
file_path_forAdmin = config.file_path_forAdmin

try:
    driver.get(mainUrl)

    time.sleep(2)

    login_button = driver.find_element("id", "login")
    login_button.click()

    email_input = driver.find_element("name", "Email")
    email_input.send_keys(user_email)

    password_input = driver.find_element("name", "Password")
    password_input.send_keys(user_password)

    submit_button = driver.find_element("xpath", "//input[@type='submit']")
    submit_button.click()

    if driver.current_url == login_url:
        print("❌ Авторизация под пользователем не удалась")
        raise Exception("Авторизация под пользователем не удалась")

    print("✔️ Тест авторизации под пользователем пройден успешно!")

    driver.get(tsCreateUrl)

    time.sleep(1)

    name_input = driver.find_element("name", "Name")
    name_input.send_keys("Название тестового ТЗ")

    description_input = driver.find_element("name", "Description")
    description_input.send_keys("Описание тестового ТЗ")

    deadline_input = driver.find_element("name", "Deadline")
    tomorrow = datetime.now() + timedelta(days=1)
    formatted_tomorrow = tomorrow.strftime("%d-%m-%Y-%H:%M:%S")
    deadline_input.send_keys(formatted_tomorrow)

    budget_input = driver.find_element("name", "Budget")
    budget_input.send_keys("100")

    file_input = driver.find_element("name", "Document")
    file_name = "Задание_на_ВКР.docx"
    full_path = file_path_forTs + file_name
    file_input.send_keys(full_path)

    submit_button = driver.find_element("xpath", "//button[@type='submit']")
    submit_button.click()

    time.sleep(1)

    if driver.current_url == tsCreateUrl:
        print("❌ Не удалось подать ТЗ")
        raise Exception("Не удалось подать ТЗ")
    print("✔️ Тест подачи ТЗ пройден успешно!")

    if driver.current_url == tsIndexUrl:
        print("✔️ Тест просмотра списка ТЗ пройден успешно!")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    edit_button = driver.find_elements("id", "edit")
    edit_button[-1].click()

    time.sleep(1)

    name_input = driver.find_element("name", "Name")
    name_input.clear()
    name_input.send_keys("New Название")

    description_input = driver.find_element("name", "Description")
    description_input.clear()
    description_input.send_keys("New Описание")

    deadline_input = driver.find_element("name", "Deadline")
    deadline_input.clear()
    dayAfterTomorrow = datetime.now() + timedelta(days=2)
    formatted_dayAfterTomorrow = dayAfterTomorrow.strftime("%d-%m-%Y-%H:%M:%S")
    deadline_input.send_keys(formatted_dayAfterTomorrow)

    budget_input = driver.find_element("name", "Budget")
    budget_input.clear()
    budget_input.send_keys("10055")

    file_input = driver.find_element("name", "Document")
    file_name = "titul_praktika.docx"
    full_path = file_path_forTs + file_name
    file_input.send_keys(full_path)

    submit_button = driver.find_element("xpath", "//input[@type='submit']")
    submit_button.click()

    time.sleep(1)

    if driver.current_url != tsIndexUrl:
        print("❌ Не удалось редактировать ТЗ")
        raise Exception("Не удалось редактировать ТЗ")
    print("✔️ Тест редактирования ТЗ пройден успешно!")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    delete_button = driver.find_elements("id", "delete")
    delete_button[-1].click()

    time.sleep(1)

    submit_button = driver.find_element("xpath", "//input[@type='submit']")
    submit_button.click()

    time.sleep(1)

    if driver.current_url != tsIndexUrl:
        print("❌ Не удалось удалить ТЗ")
        raise Exception("Не удалось удалить ТЗ")
    print("✔️ Тест удаления ТЗ пройден успешно!")

    logout_button = driver.find_element("id", "logout")
    logout_button.click()

    if driver.current_url != mainUrl:
        print("❌ Не удалось выйти из аккаунта")
        raise Exception("Не удалось выйти из аккаунта")
    print("✔️ Тест выхода из аккаунта пройден успешно!")

    time.sleep(1)

    login_button = driver.find_element("id", "login")
    login_button.click()

    email_input = driver.find_element("name", "Email")
    email_input.send_keys(admin_email)

    password_input = driver.find_element("name", "Password")
    password_input.send_keys(admin_password)

    submit_button = driver.find_element("xpath", "//input[@type='submit']")
    submit_button.click()

    editor_button = driver.find_element("id", "editor")

    if not editor_button.is_displayed():
        print("❌ Не удалось войти под администратором")
        raise Exception("Не удалось войти под администратором")
    print("✔️ Тест авторизации под администратором пройден успешно!")

    editor_button.click()

    if driver.current_url == adminIndexUrl:
        print("✔️ Тест просмотра списка отделов разработки пройден успешно!")

    addDepartment_button = driver.find_element("id", "addDepartment")
    addDepartment_button.click()

    name_input = driver.find_element("name", "Name")
    name_input.send_keys("Название тестового отдела")

    description_input = driver.find_element("name", "Description")
    description_input.send_keys("Описание тестового отдела")

    image_input = driver.find_element("name", "Image")
    file_name = "audi.jpg"
    full_path = file_path_forAdmin + file_name
    image_input.send_keys(full_path)

    submit_button = driver.find_element("xpath", "//input[@type='submit']")
    submit_button.click()

    time.sleep(1)

    if driver.current_url != adminIndexUrl:
        print("❌ Не удалось создать отдел разработки")
        raise Exception("Не удалось создать отдел разработки")
    print("✔️ Тест создания отдела разработки пройден успешно!")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    edit_button = driver.find_elements("id", "edit")
    edit_button[-1].click()

    time.sleep(1)

    name_input = driver.find_element("name", "Name")
    name_input.clear()
    name_input.send_keys("New Название тестового отдела")

    description_input = driver.find_element("name", "Description")
    description_input.clear()
    description_input.send_keys("New Описание тестового отдела")

    image_input = driver.find_element("name", "Image")
    file_name = "bmw.jpg"
    full_path = file_path_forAdmin + file_name
    image_input.send_keys(full_path)

    submit_button = driver.find_element("xpath", "//input[@type='submit']")
    submit_button.click()

    time.sleep(1)

    if driver.current_url != adminIndexUrl:
        print("❌ Не удалось редактировать отдел разработки")
        raise Exception("Не удалось редактировать отдел разработки")
    print("✔️ Тест редактирования отдела разработки пройден успешно!")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    delete_button = driver.find_elements("id", "delete")
    delete_button[-1].click()

    time.sleep(1)

    submit_button = driver.find_element("xpath", "//input[@type='submit']")
    submit_button.click()

    time.sleep(1)

    if driver.current_url != adminIndexUrl:
        print("❌ Не удалось удалить отдел разработки")
        raise Exception("Не удалось удалить отдел разработки")
    print("✔️ Тест удаления отдела разработки пройден успешно!")

    time.sleep(2)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

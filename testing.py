from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from Settings import chrome_bin_location
from Settings import webdriver_location
from Settings import url
# from Settings import username, password, phonenumber
# from check_phone import check_phone_number
from Tests.test_dataset import test_dataset
svc = Service(webdriver_location)
opt = Options()
opt.binary_location = chrome_bin_location

driver = webdriver.Chrome(service=svc, options=opt)
driver.get(url)


class TestYandex(TestCase):

    def test_ya_login(self):
        for item in dataset:
            expected = check_phone_number(item['phone'])
            result = auth_with_login_email(item['user'], item['pass'])
            self.assert_(result, expected)


def test_vk_search(login_email, password):
    driver.get(url)
    sleep(5)
    # if driver.current_url == url:
    #     driver.delete_cookie('my_cookie')
    #     sleep(5)
    #     driver.get(add_link)
    try:
        driver.find_element(By.CLASS_NAME, 'Button2_view_default').click()
        sleep(3)
        login_input = driver.find_element(By.NAME, 'login')
        login_input.clear()
        login_input.send_keys(login_email)
        sleep(3)
        driver.find_element(By.CLASS_NAME, 'Button2_type_submit').click()
        sleep(3)
    except:
        return None


    if driver.current_url == 'https://passport.yandex.ru/auth/welcome':

        password_input = driver.find_element(By.NAME, 'passwd')
        password_input.clear()
        password_input.send_keys(password)
        sleep(3)
        submit_buttion = driver.find_element(By.CLASS_NAME, 'Button2_type_submit').click()
        try:
            phone_submit = driver.find_element(By.CLASS_NAME, 'auth-challenge-form-hint')
        except:
            pass

        if phone_submit['strong'].text == check_phone_number(phonenumber):
            sleep(3)
            return phone_submit
        else:
            sleep(5)
            return None

auth_with_login_email(username, password)

driver.close()
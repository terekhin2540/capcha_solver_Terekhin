# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 10:01:10 2020

@author: OHyic
"""

# system libraries
import os
import random
import sys
import urllib
import time
# recaptcha libraries
import pydub
import speech_recognition as sr
# selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# custom patch libraries
from patch import download_latest_chromedriver, webdriver_folder_name


def delay(waiting_time=5):
    driver.implicitly_wait(waiting_time)


if __name__ == "__main__":
    # download latest chromedriver, please ensure that your chrome is up to date
    while True:
        try:
            # create chrome driver
            path_to_chromedriver = os.path.normpath(
                os.path.join(os.getcwd(), webdriver_folder_name, 'chromedriver.exe'))
            driver = webdriver.Chrome(path_to_chromedriver)
            delay()
            # go to website
            # driver.get("https://www.google.com/recaptcha/api2/demo") #Это оригинал
            # driver.get("https://hh.ru/account/connect/merge")
            # driver.get("https://hh.ru/employer")
            driver.get(
                "https://hh.ru/account/login?hhtmFrom=employer_main&hhtmFromLabel=employer_index_header&backurl=%2Femployer")
            break
        except Exception:
            # patch chromedriver if not available or outdated
            try:
                driver
            except NameError:
                is_patched = download_latest_chromedriver()
            else:
                is_patched = download_latest_chromedriver(driver.capabilities['version'])
            if not is_patched:
                sys.exit(
                    "[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:"
                    "https://chromedriver.chromium.org/downloads")
    # main program
    # auto locate recaptcha frames

    time.sleep(2)
    friendly_hello_moscow = driver.find_element_by_css_selector('.bloko-icon_cancel')  ##Убирает вопрос про город
    time.sleep(1)
    friendly_hello_moscow.click()
    #
    # entering = driver.find_element_by_class_name('supernova-button')
    # time.sleep(1)
    # entering.click()

    time.sleep(1)
    link_to_password = driver.find_element_by_css_selector("span.bloko-link-switch")
    link_to_password.click()

    password = driver.find_element_by_css_selector('input.bloko-input.bloko-input_password')
    password.click()
    time.sleep(1)
    password.send_keys('YOUR PASSWORD')
    time.sleep(3)


    def slowly_send_keys(field, text):
        for c in text:
            field.send_keys(c)
            time.sleep(0.1)

    def rand_time():
        time_rand = random.randrange(1,3)
        return time_rand


    # emailElem = driver.find_element_by_css_selector('div.bloko-form-item')
    # emailElem = driver.find_element_by_css_selector(".bloko-input[inputmode='email']").click()
    emailElem = driver.find_element_by_xpath("//input[@inputmode='email']")
    time.sleep(1)
    emailElem.click()
    emailElem.send_keys('YOUR EMAIL')

    emailElem.submit()
    time.sleep(3)
    # confirm = driver.find_element_by_class_name('bloko-button bloko-button_kind-primary bloko-button_stretched')
    # confirm.click()

    frames = driver.find_elements_by_tag_name("iframe")
    recaptcha_control_frame = None
    recaptcha_challenge_frame = None
    for index, frame in enumerate(frames):
        # print(index)
        print(frame.get_attribute("title"))

        if (frame.get_attribute("title") == "reCAPTCHA"):
            recaptcha_control_frame = frame
        if (frame.get_attribute("title") == "recaptcha challenge"):  # recaptcha-checkbox-border
            recaptcha_challenge_frame = frame
        if frame.get_attribute("title") == "проверка recaptcha":
            recaptcha_challenge_frame = frame
    if (not (recaptcha_control_frame and recaptcha_challenge_frame)):
        print("[ERR] Unable to find recaptcha. Abort solver.")
        exit()
    # switch to recaptcha frame
    time.sleep(rand_time())
    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(recaptcha_control_frame)

    time.sleep(rand_time())
    # click on checkbox to activate recaptcha
    driver.find_element_by_class_name("recaptcha-checkbox-border").click()

    time.sleep(rand_time())

    # switch to recaptcha audio control frame
    driver.switch_to.default_content()
    frames = driver.find_elements_by_tag_name("iframe")
    time.sleep(rand_time())
    driver.switch_to.frame(recaptcha_challenge_frame)

    time.sleep(rand_time())

    # click on audio challenge
    driver.find_element_by_id("recaptcha-audio-button").click()

    time.sleep(rand_time())

    # switch to recaptcha audio challenge frame
    driver.switch_to.default_content()
    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(recaptcha_challenge_frame)



    time.sleep(rand_time())

    # get the mp3 audio file
    src = driver.find_element_by_id("audio-source").get_attribute("src")
    print(f"[INFO] Audio src: {src}")

    path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
    path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

    # download the mp3 audio file from the source
    urllib.request.urlretrieve(src, path_to_mp3)

    # load downloaded mp3 audio file as .wav
    try:
        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")
        sample_audio = sr.AudioFile(path_to_wav)
    except Exception:
        sys.exit("[ERR] Please run program as administrator or download ffmpeg manually, "
                 "https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/")

    # translate audio to text with google voice recognition
    r = sr.Recognizer()
    with sample_audio as source:
        audio = r.record(source)
    key = r.recognize_google(audio)
    print(f"[INFO] Recaptcha Passcode: {key}")

    time.sleep(rand_time())
    # key in results and submit
    driver.find_element_by_id("audio-response").send_keys(key.lower())

    time.sleep(rand_time())
    driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
    driver.switch_to.default_content()

    time.sleep(rand_time())

    driver.find_element_by_id("recaptcha-demo-submit").click()
    time.sleep(rand_time())

    final_button = driver.find_element_by_xpath("//button[@data-qa='account-login-submit']")
    time.sleep(1)
    final_button.click()

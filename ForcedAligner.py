import os
import selenium
from selenium import webdriver
from glob import glob

root_path = 'path_to_wav_and_transcripts_folder'

wavs = glob('*wav')

for wav in wavs:
        driver = webdriver.Firefox(executable_path = 'path_to_gecko_driver')
        driver.get('http://phon.chass.ncsu.edu/cgi-bin/step7.cgi')
        wav_file = driver.find_element_by_name('file_wav')
        text_file = driver.find_element_by_name('file_txt')
        email_box = driver.find_element_by_name("address_1")
        submit_button = driver.find_element_by_name('submit')
        
        text = wav[:-3] + "lab"
        wav_file.send_keys(root_path + (wav))
        text_file.send_keys(root_path + (text))
        email_box.send_keys('email_id')
        submit_button.click()
        driver.close()
        
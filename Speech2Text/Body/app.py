import time

import pyperclip
import pyjupyter
import tkinter as tk
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import warnings
from selenium.webdriver.chrome.service import Service
import sentiment_analysis as sa
import prodiaAI
import os
from colorama import Fore,Style

# Checking if system is connected to internet or not
try:
    requests.get('http://www.google.com', timeout=3)
except requests.ConnectionError:
    root = tk.Tk()
    root.title("Internet Connection Status")
    label = tk.Label(root, text="Connect to Internet", font=("Arial", 14))
    label.pack(pady=20)
    root.mainloop()
    exit(0)
# Ignore unnecessary warnings
warnings.simplefilter("ignore")

try:
    # Define the URL
    url = "https://dictation.io/speech"

    chrome_driver_path = '../Brain/chromedriver.exe'
    chrome_options = Options()
    chrome_options.headless = False
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    service = Service(chrome_driver_path)
    chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Disable UI pop-ups for media access
    chrome_options.add_argument("--use-fake-device-for-media-stream")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get(url)


    try:
        driver.find_element(by=By.XPATH, value="/html/body/div[1]/div").click()
        driver.minimize_window()
    except:
        pass
    print(Fore.GREEN +"........Initiating the Application ........",Style.RESET_ALL)
    sleep(15)

    # Execute JavaScript to enable microphone access
    driver.execute_script('navigator.mediaDevices.getUserMedia({ audio: true })')
    sleep(1)

    clear_button_xpath = '/html/body/div[3]/section/div/div/div[2]/div/div[3]/div[2]/a[8]'
    driver.find_element(by=By.XPATH, value=clear_button_xpath).click()
    sleep(1)

    start_button_xpath = "/html/body/div[3]/section/div/div/div[2]/div/div[3]/div[1]/a"
    driver.find_element(by=By.XPATH, value=start_button_xpath).click()
    print("Microphone is turned on")

except Exception as e:
    print("Error: Unable to configure the ChromeDriver properly.")
    print("To resolve this error, make sure to set up the ChromeDriver correctly.")
    print(e)

# Continuous loop for capturing and writing text
while True:
    # Get the text from the dictation interface
    text_element_xpath = '/html/body/div[3]/section/div/div/div[2]/div/div[2]'
    text = driver.find_element(by=By.XPATH, value=text_element_xpath).text

    if len(text) == 0:
        pass
    else:
        # Click the "Clear" button to reset
        driver.find_element(by=By.XPATH, value=clear_button_xpath).click()
        text = text.strip()

        # Write the text to a file
        output_path = "SpeechRecognition.txt"
        with open(output_path, "w") as f:
            f.write(text)
            if(text == 'gand marao'):
                break

            #below elif clause is defined for my personal use so that i can directly open my ipython and jupyter notebook by telling only avoiding opening my prompt
            # and activating my virtual environment and other 1 2 steps. you can check the source code for the given function in pyjupyter.py
            elif(text == 'Ipython' or text == 'ipython' or text == 'jupyter notebook' or  text == 'I python' or text == 'Jupiter notebook'):
                if(text == 'Jupiter notebook' or text == 'Jupyter notebook'):
                    text = 'jupyter notebook'
                else:
                    text = 'ipython'
                pyjupyter.runshell(text)

            # This elif clause do following operations: Speech2Text-->using the sentimental analysis on generated text-->Giving ouput the Text with their emotions
            elif(text.lower() == "turn on sentiment analysis"):
                print(Fore.LIGHTBLUE_EX+"............Expected wait time: 3-5 seconds............"+Style.RESET_ALL)

                #putting the after condition to loop(While True) so that it continues to record text --->analyse it-->give ouput sentiment till we turn it off
                emotion = sa.sentiment_analysis(text)
                while True:
                    # Get the text from the dictation interface
                    text_element_xpath = '/html/body/div[3]/section/div/div/div[2]/div/div[2]'
                    text = driver.find_element(by=By.XPATH, value=text_element_xpath).text

                    if len(text) == 0:
                        pass
                    else:

                        driver.find_element(by=By.XPATH, value=clear_button_xpath).click()
                        text = text.strip()

                        #below if clause will move you out from sentimental analysis of the text so that you can continue with the normal Speech2Text generation
                        if (text.lower() == 'turn off sentimental analysis'):
                            print("........Turning OFF Sentimental Analysis.........")
                            break

                        emotion = sa.sentiment_analysis(text)
                        output_path = "SpeechRecognition.txt"
                        # with open(output_path, "w") as f:
                        #     f.write("Text: ",text,"\n","Emotion: ",emotion)
                        if(emotion == 'Neutral'):
                            print("Text: ", text, "\n", "Emotion:", Fore.BLUE ,emotion,Style.RESET_ALL)
                        elif(emotion== 'Positive'):
                            print("Text: ", text, "\n", "Emotion:", Fore.GREEN,emotion,Style.RESET_ALL)
                        elif(emotion == 'Negative'):
                            print("Text: ", text, "\n", "Emotion:",Fore.RED,emotion,Style.RESET_ALL)
                        # print("Text: ",text,"\n","Emotion:",emotion)
            elif(text.lower() == 'activate generative ai'or text.lower() == 'activate generativeai'):
                cwd = os.getcwd()
                print(Fore.GREEN +".............Hello Now you'll be Using A Generative AI Model................")
                time.sleep(1.0)
                print(Fore.GREEN +".............Expected Wait Time on each prompt:5-10 seconds.................."+Style.RESET_ALL)
                while True:
                    # Get the text from the dictation interface
                    text_element_xpath = '/html/body/div[3]/section/div/div/div[2]/div/div[2]'
                    text = driver.find_element(by=By.XPATH, value=text_element_xpath).text

                    if len(text) == 0:
                        pass
                    else:

                        driver.find_element(by=By.XPATH, value=clear_button_xpath).click()
                        text = text.strip()
                        #below if clause will move you out from sentimental analysis of the text so that you can continue with the normal Speech2Text generation
                        if (text.lower() == 'deactivate'):
                            print(Fore.RED + "........Turning OFF Generative AI........."+Style.RESET_ALL)

                            break
                        elif('generate' in text.lower()):
                            print("Prompt:",text[8:].strip().title())
                            image = prodiaAI.generate(cwd,text)



            pyperclip.copy(text) #copying the recorded text to clipboard everytime you speak
            print(text)
print(Fore.RED +".........Session Closed..........."+Style.RESET_ALL)
driver.close()
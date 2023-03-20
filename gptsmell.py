# #! /usr/bin/env python3

# Imports

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from gtts import gTTS
import logging
import requests
import os.path
import openai
import sys
from dotenv import load_dotenv
import os

from pyvirtualdisplay import Display
from picamera2 import Picamera2, Preview

def capture():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration()
    picam2.configure(camera_config)
    picam2.start()
    # picam2.capture_file("../images/test.jpg")
    picam2.capture_file("./sniff.jpg")
    # picam2.start_and_capture_file("test.jpg")
    picam2.stop()


display = Display(visible=0, size=(800, 600))
display.start()

driver = webdriver.Chrome()

load_dotenv()
openai.api_key = os.environ["OPEN_AI_KEY"]

folder_dir = os.getcwd() 
driver = webdriver.Chrome()

def describeThing(description):
    print("Going to describe what " + description + " smells like")
    whatToSmell = "Describe the smell of " + description + " in 200 characters"

    hashedThing = hash(description) % ((sys.maxsize + 1) * 2)
    try:
        print("Playing audio of " + str(hashedThing) + " smells like")
        os.system("mpg123 " + str(hashedThing) + ".mp3")
        if os.system(os_cmd) != 0:
            raise Exception('wrongcommand does not exist')

    except:
        
        print("file doesnt exist let's make a new one")
        try:
            response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant describing smells for people without a sense of smell"},
                        {"role": "user", "content": whatToSmell}]
            )

            finalResponse = response["choices"][0]["message"]["content"]
            print(finalResponse)


            # If using GPT 3.5
            # response = openai.Completion.create(
            #     engine='text-davinci-003',  # Determines the quality, speed, and cost.
            #     temperature=0.8,            # Level of creativity in the response
            #     prompt=whatToSmell,           # What the user typed in
            #     max_tokens=100,             # Maximum tokens in the prompt AND response
            #     n=1,                        # The number of completions to generate
            # )
            
            # finalResponse = response["choices"][0]["text"]
            # print(finalResponse)

            # To get voice output

            try:
                
                myobj = gTTS(text=finalResponse, lang='en', slow=False)
                myobj.save(str(hashedThing)+'.mp3')
                os.system("mpg123 " + str(hashedThing) + ".mp3")
            except:
                logging.exception("Something broke at Text to Speech")

        except:
            print("something went wrong with open AI")

def main():
    capture()
    for images in os.listdir(folder_dir): 
        try:
            if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg")):

                captchaurl = 'https://lens.google.com/upload?ep=ccm&s=csp&st=1653142987619'
                encoded_image = {'encoded_image': open(images, 'rb')}
                burp0cap_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
                                    "Origin": "null",
                                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                                    "Sec-Gpc": "1", "Sec-Fetch-Site": "none",
                                    "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                                    "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate",
                                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}
                rlens = requests.post(captchaurl, files=encoded_image, headers=burp0cap_headers,
                                        allow_redirects=True)

                html = rlens.content.decode()
                html = html.split('URL=')
                finalurl = html[1]

                
                driver.get(finalurl)

                try:
                    bestGuess = driver.find_element(By.XPATH, "//div[@data-item-title]")
                    t= bestGuess.find_element(By.XPATH, (".."))
                    bestGuess = t.get_attribute('aria-label')
                    print("Secondary Guess " + bestGuess)
                    bestGuess = bestGuess[0:50]
                    describeThing(bestGuess)
                except:
                    logging.exception("something broke at Secondary Checking")

        except Exception as e:
            print(e)


# while True:
#     # input("Press Enter to redo...")
#     main()

main()
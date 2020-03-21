# ----------------------------------------------------------------------
# author : keshan
# program description : whatsapp bot that auto replies to msgs
# date : 03:11PM on June 27, 2019
# ----------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading
import json
import random
import re
import requests

# Global variables
learn_count = 0
no_reply = [
    "sorry, i didn't get that. I'm still learning. ",
    "keshan didn't teach me well. ",
    "I didn't get that",
    "I only understand english",
    "I'm still a noob, please ease up on me :("
]


#  TODO : Handle multiple messages, improve replies accuracy
# ? Need to find a way to be able to get multiple user inputs
class Whatsapp:
    # init method
    def __init__(self, target):
        # the path to the chromedriver executable
        chromepath = 'C:\\webdrivers\\chromedriver'
        self.driver = webdriver.Chrome(executable_path=chromepath)
        self.driver.get("https://web.whatsapp.com/")
        self.greet = "I'm an automated bot. Please choose an option below:\n\n1. Show current global numbers\n2. Show all countries"
        time.sleep(25)
        # the recipient
        self.target = target
        elem = None

        # search for the target in the contact list
        while elem is None:
            try:
                elem = self.driver.find_element_by_xpath(
                    '//span[@title="' + self.target + '"]')
            except:
                # if the target is not found logout
                print("Target not found!")
                self.logout()
                break

        ac = ActionChains(self.driver)
        # move to the target span and click it
        ac.move_to_element(elem).click().perform()
        time.sleep(2)
        print(f"Found target...")
        # the chat div that has all the msgs
        self.layer = self.driver.find_element_by_xpath(
            '//div[@class="_1ays2"]')
        time.sleep(5)
        self.send_msg(f"Hello {self.target}")
        time.sleep(1)
        self.send_msg(self.greet)

    # method to logout of the web session
    # if needed call function
    def logout(self):
        # gets the hamburger drop down and clicks it
        ham = self.driver.find_element_by_xpath(
            '//div[@title="Menu"]')
        ham.click()
        time.sleep(4)
        # searches for the logout span and clicks it
        ham.find_element_by_xpath(
            '//div[@class="_2hHc6 T6CTG"]/ul[@class="_3z3lc"]/li[@class="_3cfBY _2yhpw _3BqnP"]/div[@title="Log out"]').click()

    # method that gets any new command/msg sent by the
    # user and stores it in a text file
    def learn(self, new_word):
        # get the global varibale
        global learn_count
        found = False
        # open the new text file to store the new words
        with open('src/new_words.txt', 'r+') as f:
            for line in f:
                # check if the word already exists in the file
                # to avoid duplication
                if str(new_word) in line:
                    found = True
                    break
            # store if not there already
            # stores with the current date and time + the target name : msg
            if not found:
                f.write(f'{self.target}-{str(time.ctime())}: {new_word}\n')
                learn_count += 1
            else:
                print("word in list")

    # method that returns the last msg
    # sent by the recipient
    # ! problem : Cant handle multiple msgs
    def get_msg(self):
        no_div = False
        # scrolls to the height of the page
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        try:
            # gets the list of msgs received
            # This gets the base message of every group of messages [the very last message]
            msgs = [msg.text for msg in self.layer.find_elements_by_xpath(
                "//div[@class='FTBzM message-in']//span[@class='_F7Vk selectable-text invisible-space copyable-text']")]
            print(f"Base messages : {msgs[-1]}")

            # This gets all the messages sent continuously
            # TODO : Find a way to make use of this and link the messages to it's base message
            multiple_msgs = [msg.text for msg in self.layer.find_elements_by_xpath(
                "//div[@class='FTBzM _4jEk2 message-in']//span[@class='_F7Vk selectable-text invisible-space copyable-text']")]
            # print(f"Multiple messages : {multiple_msgs[-2:]}")

            # returns the last index of the list result
            return msgs[-1].lower()
        except Exception as e:
            print(f"Message error : {e}")
            pass

        return None

    # searches through the json file for a reply suitable for the sent msg
    # returns and empty list if no replies are available
    # TODO : Test accuracy and how long/Fast it can handle the user input
    @staticmethod
    def reply_msg(msg):
        opts = {
            1: 'updates',
            2: 'show/all'
        }
        API = "http://localhost:3000/"
        if msg and int(msg) in opts.keys():
            # get the api
            print(API+opts[int(msg)])
            res = requests.get(API+opts[int(msg)])
            data = json.loads(res.content)
            print(data)
        return json.dumps(data)


    # this method finds the input box and send button
    # gets the msg received from the param and sends it
    # TODO : Crashes ( for a short period of seconds ) if 2 messages are sent at once.
    def send_msg(self, msg):
        # find the text box
        try:
            input_box = self.driver.find_element_by_xpath('//div[@class="_3FeAD _1PRhq"]//div[@class="_3u328 copyable-text selectable-text"]')
        except Exception as e:
            print(f"ERR [{e.__cause__}]")
            input_box = self.driver.find_element_by_xpath('//div[@class="_3FeAD _1PRhq focused"]//div[@class="_3u328 copyable-text selectable-text"]')

        # focus on it by clicking
        input_box.click()
        # send the msg value as the reply
        input_box.send_keys(msg)
        # find the send button and click it
        self.driver.find_element_by_xpath(
            '//span[@data-icon="send"]').click()
        # once the msg is sent . clear the text box
        # to avoid old msgs being sent
        input_box.clear()

    # method that gets the msgs and replied to
    # them as programmed
    # TODO : Testing required
    def chat(self):
        IsNew = False
        # run the method continuously for every 10 seconds
        threading.Timer(10, self.chat).start()
        try:
            last_msg = self.get_msg()
            # if last_msg:
            #     print(f"Last msg by {self.target}:  {last_msg}")
            # gets all the divs that contains the msgs (in and out)
            last_reply = [msg.get_attribute('data-pre-plain-text') for msg in self.layer.find_elements_by_xpath(
                "//div[@class='-N6Gq']//div[@class='copyable-text']")]
            # gets the last div of the above result and splits it to get the target name
            person = last_reply[-1].split(']')
            person = person[1].split(':')
            person = person[0].strip()

            # checks if the target name matches the result
            if person == self.target:
                # if the target matches, then set the new var as true so the program can identify the msg and reply
                # to it this is used here because to avoid repetitive messages being sent if the program had replied
                # once then it waits for the next msg to reply
                IsNew = True

            # if the last msg was sent or recieved
            # will run only if the last msg is recieved
            if IsNew:
                # checks if there is a reply available
                # if yes returns the list containing the one random reply
                reply = self.reply_msg(last_msg)
                if reply:
                    # send the msg using the send msg method
                    self.send_msg(reply)
                    time.sleep(1)
                    self.send_msg(self.greet)
                else:
                    # no_reply is the list of words that come in handy when the bot cant process
                    # or find what the recipient said, chose a random reply and send it
                    self.send_msg(random.choice(no_reply))
                    time.sleep(1)
                    self.send_msg(self.greet)
        except Exception as e:
            print(f"\nError : {e}\n")
            print(f"New messages : {learn_count}")
            pass


# create instance of class
if __name__ == '__main__':
    target = input("Enter target name: ")
    bot = Whatsapp(target)
    bot.chat()

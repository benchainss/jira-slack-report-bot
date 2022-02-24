from locale import currency
from re import A
from sched import scheduler
from time import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from apscheduler.schedulers.blocking import BlockingScheduler
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import load_dotenv
import datetime
import os
import time
import slack
load_dotenv()
firefox_options = Options()
firefox_options.add_argument("--headless")

oauth_token=os.getenv('OAUTH_TOKEN')
channel_id=os.getenv('CHANNEL_ID')
image_connect=os.getenv('IMAGE_CONNECT')
account=os.getenv('ACCOUNT')
password=os.getenv('PASSWORD')

class Chainss_jira_Dashboard:
    def __init__(self,oauth_token,channel_id,image_connect,account,password):
        self.oauth_token = oauth_token
        self.channel_id = channel_id
        self.image_connect = image_connect
        self.account = account
        self.password = password
        self.current_date = datetime.datetime.now().strftime('%Y%m%d')
    
    def Selenium(self):
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=firefox_options)
        driver.get(self.image_connect)
        driver.find_element_by_class_name("css-1us7xzt").send_keys(self.account)
        driver.find_element_by_class_name("css-19r5em7").click()
        time.sleep(5)
        driver.find_element_by_class_name("css-1us7xzt").send_keys(self.password)
        time.sleep(5)
        driver.find_element_by_class_name("css-19r5em7").click()
        time.sleep(20)
        driver.find_element_by_xpath('//*[@id="10016"]').screenshot(f"./jira_dashboard_image/{self.current_date}.png")
        time.sleep(5)
        driver.close()
        

    def Slack_Robot(self):
        client = WebClient(token = self.oauth_token)
        file_name = f"./jira_dashboard_image/{self.current_date}.png"
        try:
            result = client.files_upload(
                channels=self.channel_id,
                initial_comment=f"ChainSS - Bug Brief Report - {self.current_date}",
                file=file_name,
            )
            response = client.chat_postMessage(
            channel=self.channel_id,
            text=f"圖片連結:{self.image_connect}"
            )
            
        except SlackApiError as e:
            print("Error uploading file: {}".format(e))
def main():
    Chainss_Robot = Chainss_jira_Dashboard(oauth_token,channel_id,image_connect,account,password)
    Chainss_Robot.Selenium()
    Chainss_Robot.Slack_Robot()
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(Chainss_jira_Dashboard(oauth_token,channel_id,image_connect,account,password),"cron",hour=6,minute=59)  
    scheduler.add_job(main,"interval",seconds=50)
    scheduler.start()
    # main()
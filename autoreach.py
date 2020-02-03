import glob
import json
import time

import boto3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class AutoReach():
    def __init__(self,
                 executable_path="chromedriver",
                 url="https://choate.reachboarding.com/",
                 cred_file="cred.json",
                 headless=False,
                 creds={}):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")

        self.cred_file = cred_file
        self.creds = creds

        self.driver = webdriver.Chrome(
            executable_path=executable_path, options=chrome_options)
        self.driver.get(url)
        self.grab_creds()
        self.authenticate()

    def authenticate(self):
        key = self.driver.find_element_by_id("username")
        key.clear()
        key.send_keys(self.username)
        value = self.driver.find_element_by_id("password")
        value.clear()
        value.send_keys(self.password)
        self.driver.execute_script("login.authenticate();")

    def in_location(self, location="In House"):
        try:
            self.driver.find_element_by_xpath("//*[contains(text(), '" +
                                              location + "')]").click()
        except:
            time.sleep(2)
            self.in_location(location=str(location))

        if location != self.grab_location():
            raise ValueError("Location not set properly!")
        else:
            return True

    def grab_creds(self):
        if not self.creds:
            with open(self.cred_file, "r") as f:
                creds = json.load(f)
                self.username = creds['username']
                self.password = creds['password']
                self.phone_number = creds['phone_number']
        else:
            self.username = self.creds['username']
            self.password = self.creds['password']
            self.phone_number = self.creds['phone_number']

    def grab_location(self):
        try:
            leave = self.driver.find_element_by_id('extSISO_OnLeave')
            if "YOU ARE ON LEAVE" in leave.text:
                return "LEAVE" 

        except:
            pass

        try:
            current_selected = self.driver.find_elements_by_class_name(
                'btn-success')
            for each_elm in current_selected:
                try:
                    loc = each_elm.find_element_by_tag_name('div').text
                except:
                    pass

            try:
                if loc:
                    return str(loc).rstrip()
            except:
                raise ValueError("No location selected!")
        except:
            time.sleep(1)
            return self.grab_location()

    def alert(self, msg):
        client = boto3.client("sns")
        opted = client.check_if_phone_number_is_opted_out(
            phoneNumber=str(self.phone_number))
        if not opted['isOptedOut']:
            # Sending message
            client.publish(PhoneNumber=self.phone_number, Message=str(msg))
        else:
            print("Warning!", self.phone_number, "opted out!")


def run_automator(cred_file="cred.json"):
    automator = AutoReach(headless=True, cred_file=cred_file)
    old_location = automator.grab_location()

    if "Class Day" == old_location:
        automator.in_location()
        assert automator.grab_location() == "In House"  # sanity check
        automator.alert("Your location has been set from \"" + old_location +
                        "\" to \"" + automator.grab_location() + "\".")
    elif "LEAVE" == old_location:
        print("YOU ARE ON LEAVE")
    else:
        assert automator.grab_location() != "Class Day"  # sanity check
        automator.alert(
            "You are currently set to \"" + automator.grab_location() +
            "\".", )
    # Might include this for liability reasons
    # automator.alert("If this location is incorrect, you must log into REACH and change
                    # it!")


if __name__ == "__main__":
    cred_list = glob.glob("cred**.json")
    for each_cred in cred_list:
        if each_cred != "cred_template.json":
            run_automator(cred_file=each_cred)


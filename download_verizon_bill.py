import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import datetime
from datetime import datetime
import argparse
import getpass
# import pyautogui
import glob
import PyPDF2



def download_verizon_bill(username, password,user_first, city, downloadto, deviceamt):
    # Set Chrome options to download PDFs
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": f"{downloadto}",  # Path inside Docker container
      "download.prompt_for_download": False,
      "plugins.always_open_pdf_externally": True,
      "plugins.plugins_disabled": ["Chrome PDF Viewer"],
    })
    # chrome_options.add_argument("--headless")  # Run in headless mode for containers
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--remote-debugging-port=9222")


    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    expensable_amount = 0.0

    try:
        # Specify the directory and pattern (e.g., *.txt)
        files = glob.glob(f'{downloadto}/*.pdf')

        # Loop through and delete matching files
        for file_path in files:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        # Step 1: Open Verizon login page
        driver.get("https://www.verizon.com/signin")

        # # Handle the consent banner by clicking the "Accept" button if it exists
        # try:
        #     WebDriverWait(driver, 10).until(
        #         EC.element_to_be_clickable((By.ID, "consent_accept_button"))
        #     ).click()  # Replace with actual button ID or XPATH after inspecting
        # except Exception as e:
        #     print(f"No consent banner found or handled: {e}")

        # Step 2: Enter username
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "IDToken1"))).send_keys(username)

        # Step 3: Scroll to and click the "Continue" button
        continue_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "continueBtn")))
        driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
        continue_button.click()

        # Step 4: Wait for the password input to appear, then enter the password
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "IDToken2"))).send_keys(password)

        # Step 5: Scroll to and click the "Login" button
        continue_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "continueBtn")))
        driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
        continue_button.click()

        # Step 6: Wait for the page to load after login
        time.sleep(5)

        # Step 7: Navigate to billing page
        driver.get("https://www.verizon.com/digital/nsa/secure/ui/bill/overview/")

        # Step 8: Download the latest bill (find download button by inspecting the element)
        time.sleep(1)
        bill_details_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='viewBillLinkTextL2']")))
        bill_details_button.click()

        time.sleep(1)


        review_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Review bill PDF opens in a new tab']")))

        # # Wait for any potential overlay to disappear
        # WebDriverWait(driver, 20).until(
        #     EC.invisibility_of_element((By.CLASS_NAME, "gnav20-eyebrow-link-list-item"))
        # )

        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", review_button)

        # Click the button using JavaScript
        driver.execute_script("arguments[0].click();", review_button)


        time.sleep(2)  # Allow time for the download to complete
        print("Download started successfully.")

        # Scroll back up to the top of the page
        driver.execute_script("window.scrollTo(0, 0);")

        # Step 10: Find the dollar amount and save it in a variable
        try:
            expand_all_element =  WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'StyledAnchor-sc-9x52p1-2')]"))
            )
            expand_all_element.click()
            time.sleep(1)

            # Wait for the element containing the dollar amount for specific user to be present
            dollar_amount_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//h4[contains(@class, 'StyledTypography-VDS__sc-5k55co-0')]//div[contains(text(), '{user_first}')]/following-sibling::span"))
            )

            dollar_amount = float(dollar_amount_element.text.replace("$",""))  # Extract the text from the element
            print(f"Extracted dollar amount: {dollar_amount}")

            # TODO find device payment amount automatically
            # device_payment_amount_element = WebDriverWait(driver, 20).until(
            #     EC.presence_of_element_located((By.XPATH, "//*[@class='StyledAccordionDetail-VDS__sc-19df7fd-1 kLXwZB']/div/div/span/div[2]/div[2]/div[1]/span"))
            # )

            # device_payment_amount = device_payment_amount_element.text
            #
            device_payment_amount = deviceamt
            print(f"Device Payment dollar amount: {device_payment_amount}")

            expensable_amount = dollar_amount - device_payment_amount

            print(f"Total expensable amount is: {expensable_amount}")





        except Exception as e:
            print(f"Error extracting dollar amount: {e}")


        driver.get("https://us2.concursolutions.com/")

        rh_email = input("Please input your RH email")

        # Step 2: Enter username
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username-input"))).send_keys(f'{rh_email}')

        submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "btnSubmit")))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()

        time.sleep(1)

        sso_user = input("Please input your RH SSO Username:")


        pin_token = getpass.getpass("Please input your PIN + Token for RH SSO:")

        # Step 2: Enter username
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(f'{sso_user}')
        # Step 2: Enter username
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(pin_token)

        # Step 2: Click Submit
        sso_submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "submit")))
        driver.execute_script("arguments[0].scrollIntoView(true);", sso_submit_button)
        sso_submit_button.click()

        time.sleep(1)  # Allow time for the download to complete

        quick_task_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@data-id, 'quicktasks-expenseStartReport')]"))
        )
        quick_task_button.click()

        time.sleep(3)  # Allow time for the download to complete

        month = datetime.now().strftime("%b")

        # Step 2: Enter username
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "name"))).send_keys(f"Cell Phone - {month}")
        time.sleep(1)
        create_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Create Report')]/..")))
        create_button.click()
        time.sleep(1)

        add_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Add Expense')]/../..")))
        add_button.click()
        time.sleep(1)

        new_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'New Expense')]/..")))
        new_button.click()
        time.sleep(1)

        category_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Mobile/Cell')]/..")))
        category_button.click()
        time.sleep(1)

        # Enter Transaction Date
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "transactionDate-date-picker-input"))).send_keys(datetime.now().strftime("%m/%d/%Y"))
        time.sleep(1)


        # Enter vendor name
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "vendorName"))).send_keys("Verizon Wireless")
        time.sleep(1)

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Show options for City of Purchase']"))).click()
        time.sleep(1)

        # Enter city of purhcase cnqr-mEkrhJeSpl
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@spellcheck='false']"))).send_keys(f"{city}")
        time.sleep(1)

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(),'{city}')]"))).click()
        time.sleep(1)

         # Enter amount
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "transactionAmount"))).send_keys(f"{expensable_amount}")
        time.sleep(1)

        receipt_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Add Receipt')]/..")))
        receipt_button.click()
        time.sleep(1)

        upload_receipt_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Upload New Receipt')]/..")))
        upload_receipt_button.click()
        time.sleep(1)

        files = glob.glob(f'{downloadto}/*.pdf')

        for file in files:
            print(f"Found {file}")
            # Specify the input and output file paths
            input_pdf_path = f'{file}'

            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )

            # Send the file path to the input field
            file_input.send_keys(f"{input_pdf_path}")

            time.sleep(2)

            # # Optionally, submit the form or trigger any action
            save_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Save Expense')]/..")))
            save_button.click()

            submit_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Submit Report')]/../..")))
            submit_button.click()

            time.sleep(300)

    finally:
        driver.quit()

if __name__ == "__main__":

    # Get username and password from environment variables
    username = os.getenv("VERIZON_USERNAME")
    password = os.getenv("VERIZON_PASSWORD")
    password = password.replace("\\","")

    if not username or not password:
        raise ValueError("Username and password must be set in environment variables")

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="A simple python script for automation of expense reports")

    # Add an argument
    parser.add_argument('--name', type=str, help='Your first name', required=True)
    parser.add_argument('--city', type=str, help='The city your transaction should be listed in fully spelled out seperated with a comma (ex. Chapel Hill, North Carolina)', required=True)
    parser.add_argument('--downloadto', type=str, help='Location of the directory to download the PDF to',required=True)
    parser.add_argument('--deviceamt', type=float, help='Amount to subtract for your monthly device payment', required=True)

    # Parse the arguments
    args = parser.parse_args()

    print(f"Hello, {args.name}!")
    download_verizon_bill(username, password, args.name, args.city, args.downloadto, args.deviceamt)

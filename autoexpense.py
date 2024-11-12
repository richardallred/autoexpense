import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import datetime
from datetime import datetime
import argparse
import getpass
import glob


def initialize_chrome(downloadto, headless, remote_debug_port) -> webdriver:
    # Set Chrome options to download PDFs
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
      "download.default_directory": f"{downloadto}",  # Path inside Docker container
      "download.prompt_for_download": False,
      "plugins.always_open_pdf_externally": True,
      "plugins.plugins_disabled": ["Chrome PDF Viewer"],
    })
    if headless:
        chrome_options.add_argument("--headless")  # Run in headless mode for containers

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    if remote_debug_port:
        chrome_options.add_argument(f"--remote-debugging-port={remote_debug_port}")
        chrome_options.add_argument("--remote-allow-origins=*")


    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def upload_to_concur(driver,rh_email, rh_sso_username, downloadto, expensable_amount, expense_report_title, expense_vendor, city, expense_category):

    driver.get("https://us2.concursolutions.com/")

    # Enter RH email to Concur to trigger RH SSO
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username-input"))).send_keys(f'{rh_email}')

    # Click "Submit"
    submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "btnSubmit")))
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    submit_button.click()

    time.sleep(1)

    # Prompt for PIN + Token
    pin_token = getpass.getpass("Please input your PIN + Token for RH SSO:")

    # Enter username
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(f'{rh_sso_user}')
    # Enter pin + token
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(pin_token)

    # Click Submit
    sso_submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "submit")))
    driver.execute_script("arguments[0].scrollIntoView(true);", sso_submit_button)
    sso_submit_button.click()

    time.sleep(1)

    # Click "Create" Button
    create_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@data-id, 'quicktasks-newDropdown')]"))
    )
    create_button.click()

    time.sleep(1)

    # Click "Start a Report" Button
    start_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Start a Report')]"))
    )
    start_button.click()




    time.sleep(3)  # Allow time for the download to complete

    # Get month in short form (ex. Oct for October)
    month = datetime.now().strftime("%b")

    # Set Report Title and Click "Create Report"
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "name"))).send_keys(f"{expense_report_title} - {month}")
    time.sleep(1.5)
    create_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Create Report')]/..")))
    create_button.click()
    time.sleep(3)


    # Click "Add Expense"
    add_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Add Expense')]/..")))
    add_button.click()
    time.sleep(1.5)

    # Click "New Expense"
    new_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'New Expense')]/..")))
    new_button.click()
    time.sleep(1)

    # Set the expense category
    category_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{expense_category}')]/..")))
    category_button.click()
    time.sleep(1.5)

    # Enter Transaction Date
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "transactionDate-date-picker-input"))).send_keys(datetime.now().strftime("%m/%d/%Y"))
    time.sleep(1.5)


    # Enter vendor name
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "vendorName"))).send_keys(f"{expense_vendor}")
    time.sleep(1.5)

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

        time.sleep(2)

        submit_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Submit Report')]/../..")))
        submit_button.click()

        time.sleep(300)


def download_verizon_bill(driver, username, password, user_first, download_to, device_amt) -> float:

    expensable_amount = 0.0

    # Specify the directory and pattern (e.g., *.txt)
    files = glob.glob(f'{download_to}/*.pdf')

    # Loop through and delete matching files
    for file_path in files:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    # Step 1: Open Verizon login page
    driver.get("https://www.verizon.com/signin")

    time.sleep(1)

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
    time.sleep(2)

    # Step 7: Navigate to billing page
    driver.get("https://www.verizon.com/digital/nsa/secure/ui/bill/overview/")

    # Step 8: Download the latest bill (find download button by inspecting the element)
    time.sleep(5)
    bill_details_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Bill details')]/..")))
    bill_details_button.click()

    time.sleep(1)


    review_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Review bill PDF')]/..")))

    # # Wait for any potential overlay to disappear
    # WebDriverWait(driver, 20).until(
    #     EC.invisibility_of_element((By.CLASS_NAME, "gnav20-eyebrow-link-list-item"))
    # )

    # Scroll the button into view
    driver.execute_script("arguments[0].scrollIntoView(true);", review_button)

    # Click the button using JavaScript
    driver.execute_script("arguments[0].click();", review_button)


    time.sleep(8)  # Allow time for the download to complete
    print("Download started successfully.")

    # Scroll back up to the top of the page
    driver.execute_script("window.scrollTo(0, 200);")

    time.sleep(1.5)

    # Step 10: Find the dollar amount and save it in a variable
    expand_all_element =  WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Expand all')]/.."))
    )
    expand_all_element.click()
    time.sleep(1.5)

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
    device_payment_amount = device_amt
    print(f"Device Payment dollar amount: {device_payment_amount}")

    expensable_amount = dollar_amount - device_payment_amount

    print(f"Total expensable amount is: {expensable_amount}")



    return expensable_amount


if __name__ == "__main__":

    # Get username and password from environment variables
    username = os.getenv("AUTOEXPENSE_VERIZON_USERNAME")
    password = os.getenv("AUTOEXPENSE_VERIZON_PASSWORD")
    name = os.getenv("AUTOEXPENSE_FIRST_NAME")
    city = os.getenv("AUTOEXPENSE_CITY")
    downloadto = os.getcwd()
    if os.getenv("AUTOEXPENSE_DEVICE_AMT"):
        deviceamt = os.getenv("AUTOEXPENSE_DEVICE_AMT")
        deviceamt = float(deviceamt)
    else:
        deviceamt = 0.0
    rh_email = os.getenv("AUTOEXPENSE_RH_EMAIL")
    rh_sso_user = os.getenv("AUTOEXPENSE_RH_SSO_USER")

    if not username or not password or not rh_email or not rh_sso_user:
        raise ValueError("Verizon Username and Password must be set in environment variables, AUTOEXPENSE_VERIZON_USERNAME, AUTOEXPENSE_VERIZON_PASSWORD, AUTOEXPENSE_RH_EMAIL and AUTOEXPENSE_RH_SSO_USER")

    password = password.replace("\\","")
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="A simple python script for automation of expense reports")

    # Add an argument
    parser.add_argument('--name', type=str, help='Your first name on your verizon bill in case you have more than one line')
    parser.add_argument('--city', type=str, help='The city your transaction should be listed in fully spelled out seperated with a comma (ex. Chapel Hill, North Carolina)')
    parser.add_argument('--downloadto', type=str, help='Location of the directory to download the PDF to')
    parser.add_argument('--deviceamt', type=float, help='Amount to subtract for your monthly device payment which is not reimbursable ex. 38.88 for $38.88')
    parser.add_argument('--headless', action='store_true' , help='Should the browser run in a headless mode?', default=False)
    parser.add_argument('--chrome-debug-port', type=str, help='Which port to run the chrome debugger on', default='8333')

    # Parse the arguments
    args = parser.parse_args()



    if args.name:
        name = args.name
    elif name == "":
        raise ValueError("First name must be set with --name or using the AUTOEXPENSE_FIRST_NAME environment variable")

    print(f"Hello, {name}!")

    if args.city:
        city = args.city
    elif city == "":
        raise ValueError("City must be set with --city or using the AUTOEXPENSE_CITY environment variable")

    if args.downloadto:
        downloadto = args.downloadto
    else:
        downloadto = os.getcwd() + "/downloads"

    if args.deviceamt:
        deviceamt = args.deviceamt

    # Initilize the web driver
    driver = initialize_chrome(downloadto,args.headless, args.chrome_debug_port)

    try:
        expensable_amount = download_verizon_bill(driver,username, password, name, downloadto, deviceamt)
        upload_to_concur(driver,rh_email,rh_sso_user,downloadto,expensable_amount,"Cell Phone", "Verizon Wireless",city, "Mobile/Cell")
    finally:
        driver.quit()

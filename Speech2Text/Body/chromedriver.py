from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Use ChromeDriverManager to automatically download and manage ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Your Selenium code here

# Quit the driver when done
driver.quit()


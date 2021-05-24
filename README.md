### Setup

In order to run the tests you must first ensure that you have python3 and account with spotify and have downloaded the Chrome driver for Selenium tests. The download for chrome driver for selenium tests can be found here: https://chromedriver.chromium.org/downloads

Next add a .env file to the repository and add the following variables:

 //.env file
 
 USERNAME=your_spotify_username  
 PASSWORD=your_spotify_password  
 CHROME_PATH=/path/to/chromedriver
 
 
 ### Run
 
 Tests should be called in the index.py file. Some sample calls have been provided. In order to run the tests navigate the directory in the command line and type the following command in a bash command-line.
 
 ```bash
 python3 index.py
 ```

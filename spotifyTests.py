from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC

import os
from dotenv import load_dotenv
import time

load_dotenv()

#tests the functionality of searching for a song and playing it
def playSongBySearchParamTest(search_param, username, password):
    try:
        browser = webdriver.Chrome(os.getenv("CHROME_PATH"))
        landingURL = "https://open.spotify.com/"
        browser.get(landingURL)

        validateURL(browser, landingURL)
        handleCookies(browser)
        login(browser, username, password)
        search(browser, search_param)
        playFirstSong(browser)
        browser.quit()
        print("playSongBySearchParamTest succesfull with param: ", search_param)
    except:
        print("playSongBySearchParamTest failed with search param: ", search_param)


#tests the functionality of browsing for content and playing the suggested content
def playBrowseContentTest(genre, username, password):
    genre = genre.lower()
    
    try:
        browser = webdriver.Chrome(os.getenv("CHROME_PATH"))
        landingURL = "https://open.spotify.com/"
        browser.get(landingURL)

        validateURL(browser, landingURL)
        handleCookies(browser)
        login(browser, username, password)
        browseGenre(browser, genre)
        playSuggestedContent(browser, genre)
        browser.quit()
        print("playBrowseContentTest successful with param:", genre)
    except:
        print("playBrowseContentTest failed with genre param:", genre)
        browser.quit()


#test the functionality of logging in
def loginTest(username, password):

    try:
        browser = webdriver.Chrome(os.getenv("CHROME_PATH"))
        landingURL = "https://open.spotify.com/"
        browser.get(landingURL)

        validateURL(browser,landingURL)
        handleCookies(browser)
        login(browser,username, password)
        loginStatus = checkLogin(browser)
        if(loginStatus):
            print("login test successful")
        else:
            print("login test failed")
        browser.quit()
    except:
        print("login test failed")
        browser.quit()

def checkLogin(browser):
    try:
        validateURL(browser, "https://open.spotify.com/")
        accountSymbol = browser.find_element(By.CLASS_NAME, "b58ee0a27e112154586faf6775b35d40-scss")
        return True
    except:
        return False
def login(browser, username, password):

    #find the login button. Could not find a unique identifier so took all elements that contained the idenitifer and iterated through to get the right one
    potLogins = browser.find_elements(By.CLASS_NAME, "_3f37264be67c8f40fa9f76449afdb4bd-scss")

    loginButton = None
    for btn in potLogins:
        if(btn.text == "LOG IN"):
            loginButton = btn
    assert loginButton != None, "Test failed because login button does not exist"

    clickElem(browser, loginButton)

    #find username form and input username
    usernameInput = browser.find_element(By.ID, "login-username")
    usernameInput.clear()
    usernameInput.send_keys(username)

    #find password form and input password
    passwordInput = browser.find_element(By.ID, "login-password")
    passwordInput.clear()
    passwordInput.send_keys(password)

    #find submit button and submit information
    submitBtn = browser.find_element(By.ID, "login-button")
    clickElem(browser,submitBtn)

def search(browser, search_param):
    #find search tab adn click it
    searchTab = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Search")))

    clickElem(browser,searchTab)
    
    #validate that we have reached teh correct URL
    validateURL(browser, "https://open.spotify.com/search")

    #find search bar and enter search criteria
    searchBar = browser.find_element(By.CLASS_NAME, "_748c0c69da51ad6d4fc04c047806cd4d-scss")
    searchBar.clear()
    searchBar.send_keys(search_param)

def playFirstSong(browser):

    #identify the first content in the page and play it
    firstSongElem = browser.find_element(By.CLASS_NAME, "e8ea6a219247d88aa936a012f6227b0d-scss")
    action = ActionChains(browser)
    action.double_click(firstSongElem).perform()
    
  
    time.sleep(12)
    
    #check to see if the content has started playing
    playBackProgressBar = browser.find_element(By.CLASS_NAME, "playback-bar__progress-time")
    try:
        assert (playBackProgressBar.text != "0:00")
    except AssertionError:
        print('no audio played during play first song test')
        browser.quit()

    #click play button again to stop 
    playButton = browser.find_element(By.CLASS_NAME, "_82ba3fb528bb730b297a91f46acd37a3-scss")
    clickElem(browser, playButton)

def browseGenre(browser, genre_name):
    #find and click search tab
    searchTab = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Search")))

    clickElem(browser,searchTab)

    #validate that we are now on the right URL
    validateURL(browser, "https://open.spotify.com/search")

    #iterate through genre elements until we find one we are looking for
    genres = browser.find_elements(By.CLASS_NAME, "c5d42a6a1f132e80cad79e45193e9e80-scss")
    targetGenre = None
    for genre in genres:
        print(genre.text.lower(), genre_name)
        if(genre.text.lower() == genre_name):
            targetGenre = genre
            break

    clickElem(browser, targetGenre)



def playSuggestedContent(browser, genre):
    #find first suggest content collection
    try:
        firstSuggestedCollection = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "_0f1a8f7fdd1d622cbfe4c283f4f5cd72-scss"))
        )
        clickElem(browser, firstSuggestedCollection)

        #play first suggested content from collection
        if(genre != "podcasts"):
            playButton = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='action-bar-row'] [aria-label='Play']"))
            )
        else:
            playButton = WebDriverWait(browser,10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "._7416cf5ca94abb6cae138a9d97fb9a0f-scss [aria-label]"))
            )

        clickElem(browser, playButton)
    except Exception as e:
        print(str(e))
        print("element was not clickable")
        browser.quit()


    time.sleep(12)
    
    #check to see if content has started playing
    playBackProgressBar = browser.find_element(By.CLASS_NAME, "playback-bar__progress-time")
    try:
        assert (playBackProgressBar.text != "0:00")
    except AssertionError:
        print('no audio played during play first song test')
        browser.quit()

    #click again to stop content playing
    clickElem(browser, playButton)

#checks to see if the current url matches intended url
def validateURL(browser, url): 
    browser.implicitly_wait(5)
    currentURL = browser.current_url
    try: 
        assert (currentURL == url), "current url does not match expect url"
    except AssertionError:
        print(currentURL, url)

        browser.close()

#clicks a target element
def clickElem(browser,elem):
    try:
        elem.click()
        
        #if our click has changed the windows update browsers active window
        if(len(browser.window_handles) > 1):
            browser.switch_to_window(browser.window_handles[-1])
    except:
        print("failed to click an element")

#takes care of the initial cookies banner that appears
def handleCookies(browser):
    try:
        closeCookiesBtn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-close-btn-container")))
        clickElem(browser, closeCookiesBtn)
    except:
        print("cookies close button not found")





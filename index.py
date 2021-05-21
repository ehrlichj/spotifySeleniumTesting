from dotenv import load_dotenv
import os
from spotifyTests import playSongBySearchParamTest, playBrowseContentTest, loginTest

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

loginTest(username, password)
#playSongBySearchParamTest("Rolling Stones", username, password)
#playSongBySearchParamTest("Yesterday", username, password)
#playBrowseContentTest("Podcasts", username, password)
#playBrowseContentTest("New Releases", username, password)
#playBrowseContentTest("Country", username, password)





Updates over priced shoes on flightclub -$1.

How to run:
1. download the latest chrome driver: https://chromedriver.chromium.org/downloads
2. get the directory
3. set it in the `login.py` file
4. set your password and email in the `login.py` file
5. run the file. (`CMD` in your directory then `python login.py`)
6. it should open a browser, let it run while it grabs your user token and cookies
7. run the main file

Settings:
- you can set delays and change how many listings you want to scrape
these are tagged under
> #updatedelay
> #listingdelay
> #listingcount
- these are in seconds to `2` = 2 Seconds and `.8` = 0.8 Seconds
> these are not hard coded play around and see id reccomend default set
 - You can change if you want to match the ask as well
 >removing the `lowest_ask-100` `-100` on line 90 which will match the lowest ask

Errors:
- flightclub login page has V3 captcha which will ocassionally prompt a captcha, close the window and re run the file. Will add handling soon

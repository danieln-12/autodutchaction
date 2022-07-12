Updates over priced shoes on flightclub -$1.

How to run

download the latest chrome driver: https://chromedriver.chromium.org/downloads
get the directory
set it in the `login.py` file
set your password and email in the `login.py` file
run the file.
it should open a browser, let it run while it grabs your user token and cookies
run the file

Settings:
you can set delays and change how many listings you want to scrape
these are tagged under
> #updatedelay
> #listingdelay
> #listingcount
 these are in seconds to `2` = 2 Seconds and `.8` = 0.8 Seconds
> these are not hard coded play around and see id reccomend default set
You can change if you want to match the ask as well but removing the `lowest_ask-100` `-100` on line 90 which will match the lowest ask

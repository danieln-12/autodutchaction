Updates over priced shoes on flightclub $1.

How to run (working on making a stable auto login)

1. Download/clone the code
2. Install the dependencies
> `python -m pip install requests`
> `python -m pip install DateTime`
3. Load `https://sell.flightclub.com/login?redirect_url=/home`
4. Inspect element, open the network tab
5. Login, find the request made titled
6. ![image](https://user-images.githubusercontent.com/91805542/178132051-42fca213-9bc1-40f8-8e4e-bfa55594b945.png)
7. Go under the response tab
8. ![image](https://user-images.githubusercontent.com/91805542/178132065-25ccdccd-e79c-4274-b970-aac6b9e4c5b0.png)
9. Find (CTRL + F) `authenticationToken`
10. ![image](https://user-images.githubusercontent.com/91805542/178132078-ea147fa7-3cbe-4ba2-9b8f-b29e06019a06.png)
11. Copy this token
12. Edit this within the code `x-user-token` and add your email under `x-user-email`
13. next go under the `login` request and find the `cookies` tab
14. ![image](https://user-images.githubusercontent.com/91805542/178132250-330fbcc1-98f9-4917-b00d-517edb761669.png)
15. from here copy each matching cookie into the cookies json at the top of the code
16. then get the `_selluuid` from the `headers` tab
17. ![image](https://user-images.githubusercontent.com/91805542/178132260-19283fa0-5ac9-4d1c-b230-916ea9979e7f.png)
18. it should resemble `set-cookie: _selluuid=` then that value copy into the JSON.
19. after these are set you should be ready to run. 
20. you can set delays and change how many listings you want to scrape
21. these are tagged under
> #updatedelay
> #listingdelay
> #listingcount
22. these are in seconds to `2` = 2 Seconds and `.8` = 0.8 Seconds
> these are not hard coded play around and see id reccomend default set

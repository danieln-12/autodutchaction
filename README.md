# autodutchaction

uses `'x-user-email'` and `'x-user-token'` to fetch active listings, compile those listing ids, update price with a post request -100 every 24HR. you can configure time to do it by different intervals but 24hrs is what I use. 

to start

1. download the program
2. update `settings.json` with your username and password
> here you an also change `updateIntervals` (hours) so 1 = 1, 2 = 2, etc.
3.  run the `updater.exe`
4.  in the menu it will prompt the options `update all (Auto)` , `update specific (Manual)`
> to sum, Auto will do every shoe listed and update it's price, Manual will then prompt another input to paste specific ids formatted as `ID, ID, ID`
5. once an option is selected a browser will open, this is simple to bypass the stupid manual captcha to fetch the x-user-token. just leave it open for a bit as every run it will need to update it
6. it will soon start mentioning what was updated, an example status as `#5271866 => Updated -100, Current: 130.00`

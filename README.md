# Tutorial
By Vu Van Long vulong3896@gmail.com
## Download chrome driver
- Check your chrome version and go to this link http://chromedriver.chromium.org/downloads to download chromedriver version that sastifi with you chrome version
- To check your chrome version open chrome and go to tab _Setting_ and then _About chrome_
- After download chrome driver unzip and paste this in current project folder
## Run crawling script
- The first time you run the script make sure you have replaced the facebook account in line 167

    ``crawler = Livestream(login="fb_account", password="fb_password")``
- The next step is prepare some facebook id to crawl data in the file _fb_ids.txt_
- And then running the script *imagetag.py* with command:
``python imagetag.py --params``
- If you are getting this error ``DevToolsActivePort file doesn't exist`` remove chrome folder in your current project
- If you are getting error with cookies, maybe your cookies is expired => remove your cookies.pkl in your current project will solve that error
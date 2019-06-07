#Tutorial
By Vu Van Long vulong3896@gmail.com
##Download chrome driver
- Check your chrome version and go to this link http://chromedriver.chromium.org/downloads to download chromedriver versin that sastify with you chrome version
- To check your chrome version open chrome and go to tab _Setting_ and then _About chrome_
- After download chromer driver paste this in current project folder
##Run crawling script
- The first time you running the script make sure you have replaced the facebook account in line 147

``crawler = Livestream(login="your facebook account", password="your password")``
- The next step is prepare some facebook id to crawl data in the file _fb_ids.txt_
- And then running the script *imagetab.py* with command:
``python imagetag.py``
- Go to file *imagetag.py* comment line 37 and uncomment line 36 to use cookie in the later running
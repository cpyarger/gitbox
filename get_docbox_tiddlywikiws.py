from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import glob
ddirectories=r"C:\Users\cpyar\Desktop\gitbox\Files"
tiddlelist = r'C:\Users\cpyar\Desktop\gitbox\tiddle_list_2020-07-27.txt'
if not os.path.exists(ddirectories):
    os.makedirs(ddirectories)

options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": ddirectories,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

driver = webdriver.Chrome(options=options)
def download_wait(directory, timeout, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.

    """
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.crdownload'):
                dl_wait = True

        seconds += 1
    return seconds


def downloadTiddle(urlend):
    filepaths = r'C:\Users\cpyar\Desktop\gitbox\password.txt'
    with open(filepaths) as fp:
        password = fp.readline()
        driver.get("http://chris:"+password+"@docbox.flint.com:8081/"+urlend)

        elem = driver.find_element_by_link_text('save to file')

        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        download_wait(ddirectories,15)

        if not os.path.exists(ddirectories+"\\"+urlend):
            os.makedirs(ddirectories+"\\"+urlend)
        txtfiles = []
        for file in glob.glob(ddirectories+"\*.html"):
            os.replace(file, ddirectories+"\\"+urlend+"\\"+urlend+".html")




with open(tiddlelist) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       print("Line {}: {}".format(cnt, line.strip()))
       line = fp.readline()
       ln = line.rstrip('\n')
       try:
           if not os.path.exists(ddirectories+"\\"+ln+"\\"+ln+".html"):
               downloadTiddle(ln)
       except:
           print(ln+" is not a tiddle ")
       cnt += 1
   driver.close()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import glob
ddirectories=r"C:\Users\cpyar\Desktop\gitbox\Files"
tiddlelist = r'C:\Users\cpyar\Desktop\gitbox\tiddle_list_2020-07-27.txt'
passwordpath = r'C:\Users\cpyar\Desktop\gitbox\password.txt'
tiddlefile=r"https://pages.gitbox.org/"
if not os.path.exists(ddirectories):
    os.makedirs(ddirectories)

options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": ddirectories,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True,
  "start-maximized":True
})


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
    with open(passwordpath) as fp:
        password = fp.readline()
        print(r"file://"+urlend)
        driver.get(r"file://"+urlend)
        # Remove Upograde wizard
        driver.execute_script("$tw.wiki.deleteTiddler('$:/UpgradeWizard');");
        # Fix Site Title
        driver.execute_script("$tw.wiki.renameTiddler('SiteTitle','$:/SiteTitle')")
        # Fix Site Subtitle
        driver.execute_script("$tw.wiki.renameTiddler('SiteSubtitle','$:/SiteSubtitle')")
        # Fix  Default Tiddles
        driver.execute_script("$tw.wiki.renameTiddler('DefaultTiddlers','$:/DefaultTiddlers')")

        # Download Tiddle
        argh=False
        while not argh:
            try:
                DLBTN = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[3]/p/div/button[3]')
                argh=True
            except:
                pass

        DLBTN.send_keys(Keys.RETURN)

        download_wait(ddirectories,5)

        for files in glob.glob(ddirectories+"\*.html"):
            os.replace(files, urlend)
        assert "No results found." not in driver.page_source


killed=False
cnt = 1
driver = webdriver.Chrome(options=options)
for subdir, dirs, files in os.walk(ddirectories):

    for file in files:
        print("Line {}: {}".format(cnt, os.path.join(subdir, file)))
        downloadTiddle(os.path.join(subdir, file))
        cnt+=1

driver.close()
#singleTest('aws')

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
tiddlefile=r"file:///C:/Users/cpyar/Desktop/gitbox/final-empty-tiddle.html"
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


driver = webdriver.Chrome(options=options)
driver.maximize_window()
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
    folder=ddirectories+"\\"+urlend
    file=folder+"\\"+urlend+".html"
    with open(passwordpath) as fp:
        password = fp.readline()
        driver.get(tiddlefile)
        # Click More Tab on Sidebar

        toolstab=driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[5]/div/p/div/div[1]/button[3]')
        toolstab.send_keys(Keys.RETURN)
        #Click Shadowed subtab on sidebar
        print(urlend)
        argh=False
        while not argh:
            try:
                fileinput = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[5]/div/p/div/div[3]/div[3]/div[9]/p/div/input')
                argh=True
            except:
                pass

        fileinput.send_keys(file)

        argh=False
        while not argh:
            try:
                inpbtn = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/section/div[1]/div[6]/p[2]/button[2]')
                argh=True
            except:
                pass

        inpbtn.send_keys(Keys.RETURN)

        argh=False
        while not argh:
            try:
                DLBTN = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[3]/p/div/button[3]')
                argh=True
            except:
                pass

        DLBTN.send_keys(Keys.RETURN)






        assert "No results found." not in driver.page_source
        download_wait(ddirectories,60)



        for files in glob.glob(ddirectories+"\*.html"):
            os.replace(files, file)



def doloop():
    with open(tiddlelist) as fp:
        killed=False
        line = fp.readline()
        cnt = 1
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            line = fp.readline()
            ln = line.rstrip('\n')
            try:
                if killed:
                    driver = webdriver.Chrome(options=options)
                    print("restarted driver")
                    killed=False
                downloadTiddle(ln)
            except:
                print(ln+" is not a tiddle ")
                #driver.close()
                #killed=True
            cnt += 1

def singleTest(folder):
    downloadTiddle(folder)
    #input()
doloop()
#driver.close()

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
    filepaths = r'C:\Users\cpyar\Desktop\gitbox\password.txt'
    with open(filepaths) as fp:
        password = fp.readline()
        driver.get("file:///C:/Users/cpyar/Desktop/gitbox/intermediate-empty-tiddle.html")
        # Click More Tab on Sidebar
        moretab=driver.find_element_by_css_selector("a[content=TabMore]");
        moretab.send_keys(Keys.RETURN)
        #Click Shadowed subtab on sidebar
        soretab=driver.find_element_by_css_selector("a[content=TabMoreShadowed]");
        soretab.send_keys(Keys.RETURN)
        #Click Import Tiddlers Link
        elem = driver.find_element_by_link_text('ImportTiddlers')
        elem.send_keys(Keys.RETURN)
        #upload file to tiddle

        fileinput = driver.find_element_by_name('txtBrowse')
        fileinput.send_keys(urlend)
        #click "OPEN" button
        OPENBTN = driver.find_element_by_link_text('open')
        OPENBTN.send_keys(Keys.RETURN)
        # do ??
        # Click import aLL CHECKBOX ==


        argh=False
        while not argh:
            try:
                cb = driver.find_element(By.XPATH,'/html/body/div[7]/div[4]/div[2]/div[1]/div[6]/form/div[1]/div/div/div/table/thead/tr/th[1]/input')
                argh=True
            except:
                pass
        #act= ActionChains(driver).move_to_element(cb).click().perform();

        #time.sleep(3)
        cb.click()
        argh=False
        while not argh:
            try:
                inpbtn = driver.find_element(By.XPATH,'/html/body/div[7]/div[4]/div[2]/div[1]/div[6]/form/div[2]/a[2]')
                argh=True
            except:
                pass
        inpbtn.send_keys(Keys.RETURN)
        # cLICK IMPORT BUTTON
        #IMPORTBTN = driver.find_element_by_link_text('import')
        #IMPORTBTN.send_keys(Keys.RETURN)
        #download new intermediate tiddle

        #Profit?



        elem = driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div[1]/a[6]')
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        download_wait(ddirectories,60)



        for file in glob.glob(ddirectories+"\*.html"):
            os.replace(file, urlend)

killed=False

cnt = 1
for subdir, dirs, files in os.walk(ddirectories):

    for file in files:
        print("Line {}: {}".format(cnt, os.path.join(subdir, file)))
        if killed:
            driver = webdriver.Chrome(options=options)
            print("restarted driver")
        try:

            downloadTiddle(os.path.join(subdir, file))

        except:
            print(os.path.join(subdir, file)+" is not a tiddle ")
            driver.close()
            killed=True
        cnt += 1
driver.close()

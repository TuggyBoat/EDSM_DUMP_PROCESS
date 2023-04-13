import datetime
import pprint
import sys
import time
import urllib.request
import os.path
from bs4 import BeautifulSoup

dump_page = "https://www.edsm.net/en/nightly-dumps"

target_dump_url = "https://www.edsm.net/dump/stations.json.gz"

file_1 = "stations.json"
file_2 = "stations.json.gz"

file_1_check = os.path.isfile(f'./' + file_1)
file_2_check = os.path.isfile(f'./' + file_2)


# Check last dump time
def soup_page(url):
    page = urllib.request.urlopen(dump_page)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup


soup = soup_page(dump_page)
card = soup.find_all("div", {"class": "card"})[8]
table = card.find("table")
td = table.find_all("td")[5].text.strip()
dt_format = '%b %d, %Y, %I:%M:%S %p'
DUMP_UPDATE_TIME = datetime.datetime.strptime(td, dt_format)


def get_dump_update(url, out_name):
    try:
        if file_1_check:
            os.rename('./'+file_1, './'+'old_'+file_1)
        if file_2_check:
            os.rename('./'+file_2, './'+'old_'+file_2)
        urllib.request.urlretrieve(url, out_name)
        with gzip.open(out_name, 'rb') as f:
            with open(file_2, 'wb') as f_out:
                shutil.copyfileobj(f, f_out)

        os.remove(f'./{file_1}')
        os.remove(f'./{file_2}')



    except:
        print("Cannot get new dump.")
        return False


if not file_1_check and not file_2_check:
    get_dump_update(target_dump_url, file_2)
elif file_1_check:
    print(f'{file_1} is present in the repo! Checking date...')
    ctime = os.path.getctime(file_1)
    local_time = time.ctime(ctime)
    # print(local_time)
    lt_format = '%a %b %d %I:%M:%S %Y'
    LOCAL_DUMP_DOWNLOAD_TIME = datetime.datetime.strptime(local_time, lt_format)
    # print(LOCAL_DUMP_DOWNLOAD_TIME>=DUMP_UPDATE_TIME)

    if LOCAL_DUMP_DOWNLOAD_TIME >= DUMP_UPDATE_TIME:
        print('Data is up-to-date!')

    else:
        print('Data is not up-to-date! Replacing...')
        get_dump_update(target_dump_url, file_2)

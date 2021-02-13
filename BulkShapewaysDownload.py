#!/usr/bin/env python3

# See the How to Use section of the README to get started!

import requests
import pandas as pd
import os, time, re, sys
import zipfile # not certain if this requires a pip install


# Paste your list of files to download here
filesToDownload = ['GWJWLVDCM','6UQJK8H2W','FK39QN893','S4VY6PPS7','DZNQ6M2YV','LLGZ9772S','QMFTERTSY','K44DN5U2B','N4L7N4JAG','5H6GM4BWE','WE4NDEQNY','6CYJC95NS','JG4TDZ5WW','U9FJJQF67','C9GMGLBG8','W4K3WS3AY','WHG4MFPJ5','QA7AFJ4Y3','VQWXYJZKP','CKEBSJHQ5','AMHR7FK2U','UHVVNCFJG','JE8958VUE','R5AV6D26T','DRHVMSCV3','C68DWSRSM','XJGFAMFS5','Z7F46JSSC','ELG7Y4GJL','LYJ2J9TW9','P7XADP867','2MEKQU4A9','ZSQHTBGWW','ZUK9ACJHK','FUR3ZT3SA','2QAEEPG47','EZNZZXWNB','E5JSUJ6WC','SKKDDHC4P','KX7ZHQYH8','CBZXELHAM','T9UVF58JZ','ELWM74GRE','NY3UHEGWL','S8JE29PED','PPFUD8N2W','CHS6PNCCR','CHLZHGSEK','QD2PMS3JK','3GGFHJ2NC','U8BN5DTSN','E8REG6W2N','RUP6Z6RWU','DU58HR6WT','62JWMY4RA','XTGCBLJ2G','SBSY3KE28','TVB4NSFWF','TLKCUJN26','SKNYFLVK8','A33ZGMBE6','3QKZQ7TSN','LHKL9PX2V','SFQ4XL3Q3','8S97DR56X','KMGU8GFVA','B7MNHW3W3','CKAURV2SG','P5CHJ4U6V','49SZJVBSP','QNSXTEVEV','LBKLUNYCT','NFFSTQA65','YR4EKUV6N','WPBDB7QA5','XTXKU3GBU','7BQY4H2W2','TEH4CUAJQ','V9RRTTVWE','2EQSQ9JX7','M4V7S7MAX','DBYE8EJ22','FTZXF9E6J','8N57W8E5K','ZMPMYNW22','UUFR8HZNV','W47FWX6SL','HYY9XLBYT','WYR52NJWB','4TGEJ4ZSH']


# Critical tool for converting from web request to Python request: https://curl.trillworks.com/

# Paste your headers here:
headers = {
    'authority': 'www.shapeways.com',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': '...',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '...',
}

outFolder = os.path.join('..', f"BulkDownload {time.strftime('%Y-%m-%d_%H%M%S')}")
os.mkdir(outFolder)

del headers['referer']

def getResponseFilename(response):
    """Gets the response's suggested filename.
    Source: https://stackoverflow.com/a/31805472/10247514
    """
    d = response.headers['content-disposition']
    fname = re.findall("filename=(.+)", d)[0]
    fname = fname.replace("'", "").replace('"', '').replace(';', '').replace(' .', '.') # added to strip out bad characters and trailing spaces
    return fname

def doSingleFile(pathThing:str, index:int):
    """
    Downloads a single file from Shapeways, saves the ZIP and the STL into a specific folder.
    @param pathThing a string like 'VQWXYJZKP' indicating which file on Shapeways
    @param index a number to prepend for tracking
    @return directionary of info used
    """

    notes = ""

    downloadPath = 'https://www.shapeways.com/product/download/' + pathThing
    response = requests.get(downloadPath, headers=headers)

    filenameOfZip = getResponseFilename(response)
    baseFilename = filenameOfZip.split('.')[0] # get the part before 

    folderPath = os.path.join(outFolder, f"{index} - {baseFilename}")
    
    # Make the folder to store the file
    os.mkdir(folderPath)

    # Write the zip file out
    zipFilePath = os.path.join(folderPath, filenameOfZip)
    with open(zipFilePath, 'wb') as fp:
        fp.write(response.content)

    # Unzip the file
    try:
        with zipfile.ZipFile(zipFilePath, 'r') as zip_in:
            zip_in.extractall(folderPath)
    except FileNotFoundError:
        print(f"ERROR: ZIP File wasn't saved for index {index}.")
        notes += f"ERROR: ZIP File wasn't saved for index {index}."

    return {
        'Index': index,
        'Base Name': baseFilename,
        'ZIP File Name': filenameOfZip,
        'SW Path Thing': pathThing,
        'URL': downloadPath, 
        'Notes': notes
    }


def downloadAll():
    startTime = time.time()

    df = pd.DataFrame()

    curIndex = 101
    curCount = 0

    for fileStr in filesToDownload:
        thisDict = doSingleFile(fileStr, curIndex)

        df = df.append(thisDict, ignore_index=True)

        curIndex += 1
        curCount += 1
        
        print(f"Progress: {curCount}/{len(filesToDownload)} files in {(time.time()-startTime)/60:.2f} minutes.")

        # DEBUG: Quit after one
        #break

    df.to_csv(os.path.join(outFolder, f"Download List {time.strftime('%Y-%m-%d_%H%M%S')}.csv"))

    print(f"All done {curCount} files in {(time.time()-startTime)/60:.2f} minutes.")


if __name__ == '__main__':
    downloadAll()
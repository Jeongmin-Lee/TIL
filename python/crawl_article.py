from urllib import request
from multiprocessing import Pool
import xml.etree.ElementTree as ET
import logging
import time
import os
from bs4 import BeautifulSoup as BS
import requests
import json
from itertools import product
import sys
from fake_useragent import UserAgent

homeDir = sys.argv[1]
#homeDir = '/home1/irteam/data-output/jstage/update/20200522'

journalDir = homeDir + '/sitemap-index'
# scriptDir = homeDir + '''/home1/irteam/data-output/jstage/script'
downDir = homeDir + '/progress'
doneDir = homeDir + '/done'
ns = {'t': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'x': 'http://www.w3.org/1999/xhtml'}
ua = UserAgent()

def getHtmlTextWithRetry(url):
    try:
        ua.random
        headers = {'User-Agent' : ua.random}
        req = requests.get(url, headers = headers)
        return req.text
    except:
        logging.error('error...retry.. url : ' + url)
        time.sleep(1)
        return getHtmlTextWithRetry(url)
        
def parseArticle(url, lang, lastmod):
    fname = url.lstrip('https://www.jstage.jst.go.jp/article/').rstrip('/_article/').replace('/', '_')
    html = getHtmlTextWithRetry(url)
    soup = BS(html, 'html.parser')
    
    logging.info('DOWNLOADED..' + fname + ' | lang : ' + lang + ' | lastmod' + lastmod)
    
    # dict = {}
    # dict['lang'] = lang
    # dict['lastmod'] = lastmod
    
    text = "<metaInfo>"
    text += "<lang>%s</lang>" % lang
    text += "<lastmod>%s</lastmod>" % lastmod
    
    for meta in soup.find_all("meta", {"name": True, "content": True}):
        key = meta.attrs['name']
        value = meta.attrs['content']
        
        text += "<%s><![CDATA[%s]]></%s>" % (key, value, key)
        
    text += "</metaInfo>"
    return text
    
def parse(urlElem):
    linkElem = urlElem.find('x:link/[@hreflang="ja"]', ns)
    ja = linkElem.attrib.get('href')
    en = urlElem.find('t:loc', ns).text
    lastmod = urlElem.find('t:lastmod', ns).text
    
    jaDictResult = parseArticle(ja, 'ja', lastmod)
    enDictResult = parseArticle(en, 'en', lastmod)
    return (jaDictResult, enDictResult)

if __name__=='__main__':
    logging.basicConfig(filename=homeDir + '/article_down.log', level=logging.INFO)
    os.makedirs(downDir, exist_ok=True)

    for fname in os.listdir(journalDir):
        tree = ET.parse(journalDir + '/' + fname)
        root = tree.getroot()
        journalName = fname.rsplit('.xml')[0]
        saveJsonPath = downDir + '/' + journalName + '.xml'
        
        logging.info('START to download journal : ' + fname + ' :: journal : ' + journalName)
        articleList = root.findall('t:url', ns)
        # param = list(map(lambda x: (x, journalName), articleList))
        
        try:
            os.remove(downDir + '/' + journalName + '.xml')
        except OSError:
            pass
        
        pool = Pool(processes=30)
        # pool.starmap(parse, param)
        
        with open(saveJsonPath, 'a') as fw:
            for result in pool.map(parse, articleList):
                fw.write(result[0] + '\n')
                # json.dump(result[0], fw, ensure_ascii=False)
                # fw.write('\n')
                # json.dump(result[1], fw, ensure_ascii=False)
                fw.write(result[1] + '\n')
        
        pool.close()
        pool.join()
        
        # result file
        os.makedirs(doneDir, exist_ok=True)
        os.makedirs(doneDir + '/raw', exist_ok=True)
        os.rename(downDir + '/' + journalName + '.xml', doneDir + '/raw/' + journalName + '.xml')
        
        # xml file
        os.makedirs(doneDir + '/list', exist_ok=True)
        os.rename(journalDir + '/' + fname, doneDir + '/list/' + fname)
        logging.info("FINISH." + fname)

import requests
import hashlib
import json
import os
import sys
import time
from datetime import datetime
class WebNotify:
    def __init__(self,pathUrlFile,pathHashFile):
        self.pathUrlFile=pathUrlFile
        self.pathHashFile=pathHashFile
        #self.time=time
    def calculatePageHash(self,url):
        if url.strip()=='':
            return None
        if url.strip().startswith("http://") or url.strip().startswith("https://"):
            content=requests.get(url.strip()).content
        else:
            content=requests.get("http://"+url.strip()).content
        return hashlib.sha512(content).hexdigest()
        
    def initPageHash(self):
            urlFile=open(self.pathUrlFile,"r")
            hashFile=open(self.pathHashFile,"w")
            for line in urlFile:
                if line.strip()!='':
                    hashFile.write(self.calculatePageHash(line))
            urlFile.close()
            hashFile.close()
        
    def isPageChanged(self):
            listChangedPages=[]
            urlFile=open(self.pathUrlFile,"r")
            hashFile=open(self.pathHashFile,"r")
            newHashFile=open(self.pathHashFile+"1","w")
            while True:
                lineUrl=urlFile.readline().strip()
                #print(lineUrl)
                newHash=self.calculatePageHash(lineUrl)
                lineHash=hashFile.readline().strip()
                if newHash!=None and lineHash!=newHash:
                    listChangedPages.append(lineUrl)
                    newHashFile.writelines([newHash+'\n'])
                else:
                    newHashFile.writelines([lineHash+'\n'])
                if not lineUrl:
                    break
                
            urlFile.close()
            hashFile.close()
            newHashFile.close()
            os.remove(self.pathHashFile)
            os.rename(self.pathHashFile+"1",self.pathHashFile)
            return listChangedPages
if __name__ == '__main__':
    #ime programa pathUrl pathHash time (broj u sekundama) s/c
    pathUrl=sys.argv[1]
    pathHash=sys.argv[2]
    tm=int(sys.argv[3])
    operation=sys.argv[4]
    notify=WebNotify(pathUrl,pathHash)
    if (operation=='s'):
        notify.initPageHash()
    beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
    while True:
        time.sleep(tm)
        listChangedPages=notify.isPageChanged()
        if len(listChangedPages)==0:
            print('Nije bilo izmena. Vreme: '+datetime.now().strftime("%H:%M:%S"))
        else:
            print(listChangedPages)
            beep(10)
    
    
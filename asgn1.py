import sys
import statistics
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from datetime import date

def readTxt():
    fileObj = open("www2007data.txt","r")
    filelines=[]
    for line in fileObj:
        l=line.strip("\r\n")
        filelines.append(l)
        #print(l)
    return filelines

def sort_dict(dict):
    sorted_dict={}
    sorted_key=sorted(dict,key=dict.get,reverse=True)
    for w in sorted_key:
        sorted_dict[w]=dict[w]
    return sorted_dict

def q1(fileLines):
    fileType={"unknown type":[0,0]}
    filecount=0
    totalsize=0
    for line in fileLines:
        word = line.split()
        if(len(word) == 9 and word[0][0] == '-'):
            
            if(word[8].rfind(".") == -1):
                fileType["unknown type"][0]+=int(word[4])
                fileType["unknown type"][1]+=1
            else:
                type=word[8].split(".")[1]
                type=type.lower()
                type=type.strip('#')
                type=type.strip('~')
                size=int(word[4])
                if(fileType.__contains__(type)):
                    fileType[type][0]+=size
                    fileType[type][1]+=1
                else:
                    fileType[type]=[size,1]
            
            filecount+=1
            totalsize+=int(word[4])
    print(filecount)
    print(totalsize)
    for item in fileType.items():
        print(item)

def q2(fileLines):
    maxName=""
    minName=""
    minmax={"min":sys.maxsize ,"max":0,"empt":0}
    for line in fileLines:
        word = line.split()
        if(len(word) == 9 and word[0][0] == '-'):
            size=int(word[4])
            if(size == 0):
                minmax["empt"]+=1
            elif(size >= minmax["max"]):
                maxName=word[8]
                minmax["max"]=size
            elif(size < minmax["min"]):
                minName=word[8]
                minmax["min"]=size
    print(minmax)
    print(maxName)
    print(minName)

def q3(fileLines):
    sizeList=[]
    for line in fileLines:
        word = line.split()
        if(len(word) == 9 and word[0][0] == '-'):
            size=int(word[4])
            sizeList.append(size)
    sizeList.sort()
    print((len(sizeList)))
    print("mean: ",statistics.mean(sizeList))
    print("standard deviation: ",statistics.pstdev(sizeList))
    print("median: ",statistics.median(sizeList))
    print("mode: ",statistics.mode(sizeList))

def q4(fileLines):
    sizeList=[]
    for line in fileLines:
        word = line.split()
        if(len(word) == 9 and word[0][0] == '-'):
            size=float(word[4])/1024
            sizeList.append(size)
    sizeList.sort()
    #mean=np.mean(sizeList)
    #std=np.std(sizeList)
    #pdf=stats.norm.pdf(sizeList,mean,std)
    #plt.plot(sizeList,pdf)
    count, bins_count = np.histogram(sizeList,bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    y=stats.norm.cdf(sizeList)
    plt.plot(sizeList, y)
    plt.xlabel("File size(KB)")
    plt.ylabel("")
    plt.title("cdf")
    plt.show()

def q5(fileLines):
    fileSize={"unknown":0}
    fileCount={"unknown":0}
    sizeSum=0
    countSum=0
    for line in fileLines:
        word = line.split()
        if(len(word) == 9 and word[0][0] == '-'):
            if(word[8].rfind(".") == -1):
                fileSize["unknown"]+=int(word[4])
                fileCount["unknown"]+=1
                countSum+=1
                sizeSum+=int(word[4])
            else:
                type=word[8].split(".")[1]
                type=type.lower()
                type=type.strip('#')
                type=type.strip('~')
                size=int(word[4])
                if(fileSize.__contains__(type)):
                    fileSize[type]+=size
                    fileCount[type]+=1
                    countSum+=1
                    sizeSum+=size
                else:
                    fileSize[type]=size
                    fileCount[type]=1
                    countSum+=1
                    sizeSum+=size
    sortedFileSize=sort_dict(fileSize)
    sortedFileCount=sort_dict(fileCount)
    otherSize=0
    otherCount=0
    counter=0
    for key,value in sortedFileSize.items():
        
        if(counter<10):
            print(key,value,float(value/sizeSum*100))
            counter+=1
            continue
        otherSize+=value
    print(otherSize,float(otherSize/sizeSum*100))
    counter=0
    print("----------------------------")
    for key,value in sortedFileCount.items():
        
        if(counter<10):
            print(key,value,float(value/countSum*100))
            counter+=1
            continue
        otherCount+=value
    print(otherCount,float(otherCount/countSum*100))
    print("----------------------------")
    print(sizeSum)
    print(countSum)

def q6(fileLines):
    flag=False
    skip=False
    fileSize=[]
    posterSize=[]
    for line in fileLines:
        if(line == "./papers:"):
            flag=True
            skip=True
            continue
        if(skip):
            skip=False
            continue
        if(flag):
            if(line == ""):
                flag=False
                continue
            word = line.split()
            fileSize.append(float(word[4])/1024)
    flag=False
    skip=False
    for line in fileLines:
        if(line == "./posters:"):
            flag=True
            skip=True
            continue
        if(skip):
            skip=False
            continue
        if(flag):
            if(line == ""):
                flag=False
                continue
            word = line.split()
            posterSize.append(float(word[4])/1024)
    #print(fileSize)
    fileSize.sort()
    posterSize.sort()
    count, bins_count=np.histogram(fileSize,bins=200)
    pdf = count/sum(count)
    cdf=np.cumsum(pdf)
    plt.plot(bins_count[1:],cdf,'y',label="paper cdf")
    count1, bins_count1=np.histogram(posterSize, bins=200)
    pdf1 = count1/sum(count1)
    cdf1=np.cumsum(pdf1)
    plt.plot(bins_count1[1:],cdf1,'c',label="poster cdf")
    #plt.hist(posterSize,bins=200)
    #plt.title("poster distribution")
    plt.legend()
    plt.title("cdf")
    plt.xlabel("File size(KB)")
    #plt.ylabel("Frequency")
    plt.show()

def q7(fileLines):
    today=date.today()
    month_dict={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
    fileDate={}
    fileDays=[]
    for line in fileLines:
        word = line.split()
        if(len(word) == 9 and word[0][0] == '-'):
            mm=month_dict[word[5]]
            dd=int(word[6])
            yy=int(word[7])
            file=date(yy,mm,dd)
            fileDate[word[8]]=int(str(today-file).split()[0])
            duration=int(str(today-file).split()[0])
            fileDays.append(duration)
    fileDays.sort()
    #print("mean: ",statistics.mean(fileDays))
    #print("median: ",statistics.median(fileDays))
    #print("mode: ",statistics.mode(fileDays))
    count,bins_count=np.histogram(fileDays,bins=200)
    pdf = count/sum(count)
    cdf=np.cumsum(pdf)
    plt.plot(bins_count[1:],cdf)
    plt.title("cdf")
    plt.xlabel("File age(days)")
    plt.show()


if __name__ == "__main__":
    print("asgn1 python script")
    fileLines=readTxt()
    q1(fileLines)

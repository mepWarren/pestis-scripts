#Author: Lizzy Porter
#Date: 9/30/2021
#This program takes GFF file, parses out cdRegions, and makes files
#Forward stand, removes the stop codons
import sys, re, os


gffFileName = "CO_92_AL590842.gff3"
dirOfChunks = "homFiles"
output = "cdFiles"
refGenome = "CO92.fa"

def main():
    print("Running...") 
    starts = []
    ends = []
    myData = openFile()   
    regions = mapAnnotationFile(myData)
    starts = regions[0]
    ends = regions[1]
    parseLength(starts, ends)
     

def openFile():
    print("Open files...")
    myData = ""
    try: 
        with open(gffFileName, "r") as data: 
            for line in data:
                myData = myData + line
            data.close() #When do I want to close this file?
    except IOError: 
        print("Could not read file: ", gffFileName)
    return(myData)

def mapAnnotationFile(data):
    #Create a map of teh annotation file
    cdMap = []
    starts = []
    ends = []
    print("Mapping annotation files..."
    cdMap = re.findall("CDS" +'\s'+'[0-9]*'+ '\s'+'[0-9]*'+ '\s' + '\.'+'\s'+ '\+' , data)
    for i in cdMap:
        cdNum = i.split()
        starts.append(cdNum[1])
        ends.append(cdNum[2])
    return(starts, ends) 


def parseLength(starts, ends):
    #Parses the sequence out
    start = starts
    end = ends    
    for filename in os.listdir(dirOfChunks):
        mauveFiles = re.findall('[0-9]+', filename) 
        mauveStart = mauveFiles[0]
        mauveEnd = mauveFiles[1] 
        refSeq = getRefSeq(filename)   
        for (cdStart, cdEnd) in zip(start, end):
            geneStart = int(cdStart) - int(mauveStart)
            geneLength = int(cdEnd) - int(cdStart) -2#-2 #Remove stop codon
            geneEnd = geneStart + geneLength
            newName = str(cdStart) + "_" + str(cdEnd)
            cdRegion = calcCDRegion(filename, int(geneStart), int(geneEnd), int(mauveStart), refSeq)
            if len(cdRegion) > 0:                
                buildFiles(newName, cdRegion)
            else:
                print("Failed to get region: " + (newName))
 
def getRefSeq(filename):
    ref = False
    seq = ""
    with open(dirOfChunks + "/" + filename, "r") as data:
        for line in data: 
            if refGenome in line:
                seq = seq+line
                ref = True
            elif ref:
                seq = seq + line.strip()
            elif ">" in line:#Different sseq
                ref = False 
        return(seq)
 

def calcCDRegion(fileName, geneStart, geneEnd, mauveStart, refSeq):
    #Calculates coding region
    cdChunk = ""
    header = ""
    seq = ""
    preCDRegion = ""
    preCDRegion = refSeq[mauveStart: geneStart]
    gaps = preCDRegion.count("-")  
    ogStart = geneStart
    ogEnd = geneEnd
    if gaps > 1:
        geneStart = geneStart + gaps -1
        geneEnd = geneEnd + gaps -1
        preCDRegion = refSeq[mauveStart: geneStart]
    gaps2 = preCDRegion.count("-")- gaps
    if gaps2 > 0:
        geneStart = geneStart + gaps -1
        geneEnd = geneEnd + gaps -1
        preCDRegion = refSeq[mauveStart: geneStart: 1]
    region = refSeq[geneStart:geneEnd]
    regionGap = region.count("-")  
    if regionGap > 0:
        geneEnd = geneEnd + regionGap   

    with open(dirOfChunks + "/" + fileName, "r") as data:
        for line in data:
            if ">" in line:
                if seq != "":
                    tempSeq = seq[geneStart:geneEnd]   
                    stopCodon = seq[geneEnd:geneEnd + 3] #Adjust to check stop codon
                    if stopCodon != "TAA" and stopCodon != "TAG" and stopCodon != "TGA":
                        gapInSeq = tempSeq.count("-")
                        if gapInSeq > 0:
                            tempSeq = seq[geneStart:geneEnd+ gapInSeq]
                            stopCodon = seq[geneEnd:geneEnd + 3]
                    if len(tempSeq)>0:
                        cdChunk =  cdChunk + header + "\n" + tempSeq + "\n"
                    seq = ""
                    header = ""
                newText = re.sub("\s[0-9]*:[0-9]*\-[0-9]*\s\+\s", "", line)
                header = newText.strip()
            elif "=" in line:
                seq = seq + line.strip()
                tempSeq = seq[geneStart:geneEnd]
                gapInSeq = tempSeq.count("-")
                stopCodon = seq[geneEnd:geneEnd+3] #Adjust to check stop codon
                if gapInSeq > 0:
                    tempSeq = seq[geneStart:geneEnd+gapInSeq] 
                    stopCodon = seq[geneEnd:geneEnd + 3]
                if len(tempSeq)>0:
                    cdChunk =  cdChunk + header + "\n" + tempSeq
                seq = ""
                header = ""
            else :
                seq = seq + line.strip()
        if len(cdChunk) != 0 and (stopCodon == "TAA" or stopCodon == "TAG" or stopCodon == "TGA"):
            return(cdChunk)
        else:
            print(stopCodon)
            return("")
   

def buildFiles(Name, cdChunk): #Builds new files 
    firstCodon = cdChunk[8: 12: 1]
    firstCodon = firstCodon.strip()
    if cdChunk.count("-") > 1:
        newFile = open(output + "/" + Name + "_" + "hasGaps", "w")
        newFile.write(cdChunk)
        newFile.close() 
    elif str(firstCodon) == "ATG":
        fileName = "cdYP_" + str(Name)
        newFile = open(output + "/" + fileName, "w")
        newFile.write(cdChunk)
        newFile.close() 
    else: 
        newFile = open(output + "/" + Name + "_" + firstCodon, "w")
        newFile.write(cdChunk)
        newFile.close()


#Application entry point
main()

#Author: Lizzy Porter
#Date: 9/30/2021
#This program takes GFF file, parses out cdRegions, and makes files
#Works on the reverse strand. Checks for and removes stop codon. 
from Bio.Seq import Seq
import sys, re, os


gffFileName = "CO_92_AL590842.gff3"
dirOfChunks = "homFiles"
output = "cdFilesRev"
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
    #Creates a map of the annotation files
    cdMap = []
    starts = []
    ends = []
    cdMap = re.findall("CDS" +'\s'+'[0-9]*'+ '\s'+'[0-9]*'+ '\s' + '\.'+'\s'+ '\-' , data)
    for i in cdMap:
        cdNum = i.split()
        starts.append(cdNum[1])
        ends.append(cdNum[2])
    return(starts, ends) 


def parseLength(starts, ends):
    #Parses the starts and stops within coding region from annotation files
    start = starts
    end = ends    
    for filename in os.listdir(dirOfChunks):
        mauveFiles = re.findall('[0-9]+', filename) 
        mauveStart = mauveFiles[0]
        mauveEnd = mauveFiles[1] 
        refSeq = getRefSeq(filename)   
        for (cdStart, cdEnd) in zip(start, end):
            geneStart = (int(cdStart) - int(mauveStart)) +3 #+3 #Remove stop codon
            geneLength = int(cdEnd) - int(cdStart)-2  #Adjust for codon move
            geneEnd = geneStart + geneLength
            newName = str(cdStart) + "_" + str(cdEnd)
            #Returns cdREgion
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
    #Calulates the cd regions
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
                    startCodon = seq[geneEnd-3:geneEnd] #Adjust to check stop codon
                    if startCodon != "CAT":
                        gapInSeq = tempSeq.count("-")
                        if gapInSeq > 0:
                            tempSeq = seq[geneStart:geneEnd+ gapInSeq]
                    if len(tempSeq)>0:
                        mySeq = Seq(tempSeq)
                        revSeq = mySeq.reverse_complement()
                        cdChunk =  cdChunk + header + "\n" + str(revSeq) + "\n"
                    seq = ""
                    header = ""
                newText = re.sub("\s[0-9]*:[0-9]*\-[0-9]*\s\+\s", "", line)
                header = newText.strip()
            elif "=" in line:
                seq = seq + line.strip()
                tempSeq = seq[geneStart:geneEnd]   
                startCodon = seq[geneEnd-3:geneEnd] #Adjust to check stop codon
                if startCodon != "CAT":
                    gapInSeq = tempSeq.count("-")
                    if gapInSeq > 0:
                        tempSeq = seq[geneStart:geneEnd+ gapInSeq]
                        startCodon = seq[geneEnd-3:geneEnd]
                if len(tempSeq)>0:
                    mySeq = Seq(tempSeq)
                    revSeq = mySeq.reverse_complement()
                    cdChunk =  cdChunk + header + "\n" + str(revSeq) + "\n"
                seq = ""
                header = ""
            else :
                seq = seq + line.strip()
        if len(cdChunk) != 0:
            return(cdChunk)
        else:
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

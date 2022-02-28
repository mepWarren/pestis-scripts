#Author: Lizzy Porter
#Date: 6/24/2021
#This program takes MAUVE output files and makes files of homologouse nature with ref Genome location as name. 
import sys, re


numberOfFiles = 24
fastaFileName = "NMsamples.xmfa"
refGenome ="CO92_genome.fasta"

def main():
    print("Running...")
    splitHeaderAndSeq()
    
def splitHeaderAndSeq(): #Parse out the files
    countOfNewFiles = 0
    headerInfo = ""
    seqInfo = ""
    try: 
        with open(fastaFileName, "r") as data: 
            for line in data:
                if "#" in line: #Gets the header information
                   headerInfo = headerInfo + line.strip()
                else: #Sequence infomation
                    seqInfo = seqInfo + line 
            sepChunksOut(seqInfo)
    except IOError: 
        print("Could not read file: ", fastaFileName)
    data.close() 

def sepChunksOut(seqInfo): #Seperate the chunks
    chunk = ""
    for line in seqInfo.splitlines():
        if "=" not in line: #grab string until end of file
            chunk = chunk + line + "\n"       
        else: #send to new funtion 
            check4Seq(chunk + "\n" + "=")
            #countCheck(chunk)
            chunk = ""

def check4Seq(chunkOfSeq): #Check all samples have seq in them     
    header = ""
    seq = ""
    homolChunk = ""
    for line in chunkOfSeq.splitlines(): 
        if ">" in line or "=" in line:
            if seq:
                if len(seq) != seq.count("-"):
                    if not homolChunk:
                        homolChunk = header +"\n" + seq
                    else:
                        homolChunk = homolChunk + "\n" + header +"\n" + seq
                header = ""
                seq = ""
            header = line
        else:
            seq = seq + line
    countCheck(homolChunk)         
   

def countCheck(chunk): #Count the num of seq in chunk compared to number of seq total
    if (chunk.count(">") == numberOfFiles): 
        fileName(chunk + "=") 
    else:    
        print("Error message: homol chunk not in all files, not saved")
       
def fileName(homolchunk): #Find loc of ref genome to name new file
    titleInfo = re.findall('>\s[0-9]*:[0-9]*-[0-9]*\s\+\s'+(refGenome), homolchunk)
    if len(titleInfo)==1:
        nameLoc = re.findall('[0-9]*-[0-9]*', titleInfo[0])
        buildFile(nameLoc[0], homolchunk)
    else:
        print("The regex found multiple matches for refence genome location") 
 

def buildFile(name, homolchunk): #Build new files
    newFile = open("Mauve_chunk_"+name, 'w+')
    newFile.write(homolchunk)
    newFile.close()

#Application entry point
main()

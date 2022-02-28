#Author: Lizzy Porter
#Date: 7/8/2021
#This program takes names of all cdRegion and makes a txt file for hyphy

import sys, re, os

refGenome = "CO92_genome.fa"
dirOfChunks = "cdFilesRev/goodStart"
outputDir = "textFilesRev"
treeFileName = "nmSeq_tree.txt"

def main():
    for filename in os.listdir(dirOfChunks):
        memeFile(filename)
        felFile(filename)
              

def memeFile(name): #Build new files
    fileName = "input_meme_" + name + ".txt"
    newFile = open(outputDir + "/" + fileName, "w")
    newFile.write(str(1)+"\n"+str(1)+"\n"+name+"\n"+treeFileName) 
    newFile.close()

def felFile(name): #Build new files
    fileName = "input_fel_" + name + ".txt"
    newFile = open(outputDir + "/" + fileName, "w")
    newFile.write(str(1)+"\n"+str(2)+"\n"+name+"\n"+treeFileName) 
    newFile.close()


#Application entry point

main() 

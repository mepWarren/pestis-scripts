# pestis-scripts
Bash scripts used for comparison of bacteria

**Bash Scripts:** createOneFile.sh: Concatinates multiple Fasta files, beast.sh, iqtree.sh, mauve.sh, megacats.sh, fel_HyPhy.sh, meme_HyPhy.sh

**cdForRegions.py and cdRegions.py**: take the GFF files for your reference organism and parses out coding regions. Output file names indicate if there are any indels in the coding regions. It also notes if the sequence doesn't start with ATG.

**hyphyTextFiles.py and hyphyTextFilesRev.py**: parses through output files from cdForRegions.py and cdRegions.py and makes text files for each coding region. These text files are used with fel_HyPhy.sh and meme_HyPhy.sh. 

**orderHomolChunk.py**: Takes MAUVE output files and parses out homologous sequences with their corresponding location in the reference genome. 

**orderMauveFiles.py**: Uses the MAUVE output file and assembles the aligned genomes. 

**ParseFelSlurm.py and parseMemeSlurm.py**: Parses through the HyPhy results for MEME and FEL. Returning only the regions that expressed selection. 

**parseNonConservedSeq.py**: Takes homologous files and parses out regions that are not conserved. 

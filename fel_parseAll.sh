#!/bin/bash

#SBATCH --time=48:00:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=65536M   # memory per CPU core
#SBATCH -J "NM_for_FEL"   # job name
#SBATCH --mail-user=elizabethporter10@gmail.com   # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL


# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

module load miniconda3
source /fslgroup/fslg_PickettLabGroup/software/group-conda/bin/activate
conda activate hyphy

#Meme Analysis

for file in input_fel_cdYP*; do
	#echo "$file | hyphy"
	cat $file | hyphy
done





#cat input_hyphy.txt | hyphy

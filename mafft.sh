#!/bin/bash
#submit with 'sbatch mafft.sh </path/name_of_afa_file>'

#SBATCH --time=24:00:00   # walltime
#SBATCH --ntasks=8   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=32G   # memory per CPU core
#SBATCH -J "mafft"   # job name
#SBATCH --qos=bep8

# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
#initialize conda and activate environment
#source /fslhome/bep8/anaconda3/bin/activate #local
#module load group-conda
module load miniconda3
source /fslgroup/fslg_PickettLabGroup/software/group-conda/bin/activate #group
conda activate mafft

#call script
date
echo "mafft $1 > $1.afa"
echo "Running mafft..."

#mafft --auto > $1.afa
#mafft --auto --memsave $1 > $1.afa
#mafft --retree 2 --maxiterate 0 $1 > $1.afa
mafft --retree 1 --maxiterate 0 --nofft --memsave --thread 8 $1 > $1_fasta.afa

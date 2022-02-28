#!/bin/bash

#SBATCH --time=08:00:00   # walltime
#SBATCH --ntasks=4   # number of processor cores (i.e. tasks)
#SBATCH --nodes=4   # number of nodes
#SBATCH --mem-per-cpu=32G   # memory per CPU core
#SBATCH -J "mauve_CP_ref"   # job name
#SBATCH --mail-user=elizabethporter10@gmail.com
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL


# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
#initialize conda and activate environment
module load miniconda3
source /fslgroup/fslg_PickettLabGroup/software/group-conda/bin/activate #group
conda activate mauve

progressiveMauve --output=$1.xmfa *.fa


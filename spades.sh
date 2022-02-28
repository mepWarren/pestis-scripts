#!/bin/bash
#submit with 'sbatch spades.sh </path/name_of_r1> </path/name_of_r2>'

#SBATCH --time=24:00:00   # walltime
#SBATCH --ntasks=4   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=32G   # memory per CPU core
#SBATCH -J "spades"   # job name
#SBATCH --qos=bep8

# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
#initialize conda and activate environment
module load miniconda3
source /fslgroup/fslg_PickettLabGroup/software/group-conda/bin/activate #group
conda activate spades

#call script
date
echo "spades PE: $1, $2"
echo "Running spades..."

#raw text command:
#spades.py --pe1-1 ./trimmed/Wt_S66_R1_001_val_1.fq.gz --pe1-2 ./trimmed/Wt_S66_R2_001_val_2.fq.gz --plasmid -o ./spades

##circularized
#spades.py --pe1-1 $1 --pe1-2 $2 --plasmid -o ~/compute/Wilson/spades_plasmid
##noncircularized
#spades.py --pe1-1 $1 --pe1-2 $2 -o ~/compute/Wilson/spades_linear -t 4 -m 128
#isolate
spades.py --pe1-1 $1 --pe1-2 $2 --isolate -o ~/compute/Wilson/spades_isolate -t 4 -m 128

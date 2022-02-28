#!/bin/bash
#submit with 'sbatch armor </path/name_of_config_file>'

#SBATCH --time=71:00:00   # walltime
#SBATCH --ntasks=4   # number of processor cores (i.e. tasks)
#SBATCH --nodes=4   # number of nodes
#SBATCH --mem-per-cpu=64G   # memory per CPU core
#SBATCH -J "megaCATS"   # job name
#SBATCH --mail-user=elizabethporter10@gmail.com
#SBATCH --mail-type=BEGIN
#SBATCH	--mail-type=END
#SBATCH --mail-type=FAIL

# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
#initialize conda and activate environment
#source /fslhome/bep8/anaconda3/bin/activate #local
#module load group-conda
module load miniconda3
source /fslgroup/fslg_PickettLabGroup/software/group-conda/bin/activate #group
conda activate megacats

#call script
date
echo "Running megaCATS..."
echo "metadata_parser.pl"

perl metadata_parser.pl


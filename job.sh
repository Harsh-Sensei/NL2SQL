#!/bin/bash

#SBATCH --job-name=mnist_job    # Job name
#SBATCH --mail-type=END, FAIL        # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=3502.stkabirdin@gmail.com     # Where to send mail	
#SBATCH --nodes=1                    # Run on a single CPU
#SBATCH --mem=0                     # Job memory request
#SBATCH --ntasks-per-node=8
#SBATCH --time=00:05:00               # Time limit hrs:min:sec
#SBATCH --output=std_out_%j.log   # Standard output and error log

module purge
module load cuda/11.6

export PATH_DATASETS="/projets/descartes/NL2SQL/data"
export MODEL_PATH="/projets/descartes/NL2SQL/models"

RUN_PATH="/users/descartes/hashah/NL2SQL/NLP-Text2SQL/src/test.py"

source /descartes-venv/bin/activate

python $RUN_PATH


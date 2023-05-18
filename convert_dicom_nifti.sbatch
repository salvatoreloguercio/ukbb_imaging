#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=gpu
#SBATCH --time=240:00:00
##SBATCH -J dicom2nifti
##SBATCH -o dicom2nifti.%J

export PYTHONUNBUFFERED=TRUE

#module load python/3.8.3
module load tensorflow
module load opencv

cd $SLURM_SUBMIT_DIR

python convert_dicom_nifti.py $start $stop
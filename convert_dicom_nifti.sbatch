#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=gpu
#SBATCH --time=3:00:00
#SBATCH -J dicom2nifti
#SBATCH -o dicom2nifti.%J

export PYTHONUNBUFFERED=TRUE

#module load python/3.8.3
module load tensorflow
module load opencv

cd /gpfs/group/torkamani/loguerci/ukbb_cardiac

python convert_dicom_nifti.py
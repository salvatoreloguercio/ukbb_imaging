#!/bin/bash -l

# spawner for batched image conversion jobs

while read batch; do

  start=echo $batch | $(cut -d "_" -f 1)
  stop=echo $batch | $(cut -d "_" -f 2)


  sbatch --export=start=$start,stop=$stop --job-name=convert_dicom_nifti_$batch --output=convert_dicom_nifti_$batch.%J convert_dicom_nifti.sbatch;
  sleep 1;

done < batches.txt


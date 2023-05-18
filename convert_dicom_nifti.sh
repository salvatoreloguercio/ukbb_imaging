#!/bin/bash -l

# spawner for batched image conversion jobs

while read batch; do

  start=$( echo $batch | cut -d "-" -f 1 )
  stop=$( echo $batch | cut -d "-" -f 2 )


  sbatch --export=start=$start,stop=$stop --job-name=convert_d_n_$batch --output=convert_d_n_$batch.%J convert_dicom_nifti.sbatch;
  sleep 1;

done < batches.txt


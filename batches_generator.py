import numpy as np
import pandas as pd
import sys

# Access individual command-line arguments
file_name = sys.argv[1]
starting = int(sys.argv[2])
ending = int(sys.argv[3])
jobs_per_node = int(sys.argv[4])

# Write batches for all the jobs
with open(file_name, 'a') as file:
    job_end = 0
    for i in range(starting,ending,jobs_per_node):
        # Keep adding constant jobs for each batches
        if job_end<=ending-jobs_per_node:
            job_end = i+800
            file.write(str(i)+'-'+str(job_end)+'\n')
        # Until the last batch that needs less jobs than others
        else:
            job_end = ending 
            file.write(str(i)+'-'+str(job_end)+'\n')
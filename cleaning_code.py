iimport sys
import os
import glob
import pandas as pd
# from ukbb_cardiac.data.biobank_utils import *
import dateutil.parser
import zipfile
import shutil
import warnings
import shutil

warnings.simplefilter(action='ignore', category=FutureWarning)

# read paths of dicom files (zip only)

file_list = pd.read_csv("dicom_list_baseline.txt",header=None)

# get id from each zip (not unique)
file_list['id'] = [file.split("/")[-1].split("_")[0] for file in file_list[0]]

# convert all id to a list (not unique)
file_list_0 = file_list[0].tolist()

# Remove CINE from id that contains cine file
file_list_0 = [item for item in file_list_0 if 'CINE' not in item]

# get id again after filter out CINE into a list
file_list_zip = [file.split("/")[-1].split("_")[0] for file in file_list_0]

# sort and get unique file
file_list_zip_unique = list(sorted((set(file_list_zip))))

print("Number of input IDs:")
print(len(file_list_zip))
print("Unique input IDs:")
print(len(file_list_zip_unique))

# create df with id (not unique)
cnt_check = pd.DataFrame(file_list_zip, columns = ['id'])

# # cnt_check['id2'] = cnt_check['id']
# # cnt_check['cnt'] = cnt_check.groupby(by = ['id2']).count()

# create df with id (unique) and a column to count each appearance
cnt_check_group = pd.DataFrame(cnt_check.value_counts(), columns = ['cnt'])
cnt_check_group

# #print(len(cnt_check_group[cnt_check_group['cnt'] == 4]))
print("Number of input IDs with at least 3 DICOM image types")
print(len(cnt_check_group[cnt_check_group['cnt'] >= 3]))
print("Number of input IDs with at least 2 DICOM image types")
print(len(cnt_check_group[cnt_check_group['cnt'] == 2]))
print("Number of input IDs with at least 1 DICOM image type")
print(len(cnt_check_group[cnt_check_group['cnt'] == 1]))
print("------")
print("counter","ID",sep="\t")
# only ids with counts 3 or 4 above
file_list_full = list(cnt_check_group[cnt_check_group['cnt'] >= 3 ].reset_index(drop = False).id)


data_root = "/mnt/stsi/stsi3/Internal/ukbb_cardiac"


# convert dicom file to nifti file

list_error = []
n = 0
for eid in file_list_full[int(sys.argv[1]):int(sys.argv[2])]:

    n += 1
    # print(n,eid,sep="\t")

    # Unpack the data
    # use eid (who has more than 3 files) to keep all file who has 3 files or more from single patient                      
    files = [s for s in file_list_0 if eid in s]
    print(files)
    
    # for f in files:   
    f = files[0]
    foldnum=f.split("/")[9]

    foldnum_dir = os.path.join(data_root,"nifti",foldnum)

                                
    nifti_dir = os.path.join(foldnum_dir,str(eid)) 
    if os.path.exists(nifti_dir):
      print(nifti_dir)  
      shutil.rmtree(nifti_dir)

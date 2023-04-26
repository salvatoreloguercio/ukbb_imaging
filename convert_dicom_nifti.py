import os
import glob
import pandas as pd
from ukbb_cardiac.data.biobank_utils import *
import dateutil.parser
import zipfile
import shutil

# read paths of dicom files (zip only)

file_list = pd.read_csv("dicom_list_baseline.txt",header=None)
file_list_0 = file_list[0].tolist()
file_list_zip = [file.split("/")[-1].split("_")[0] for file in file_list_0]
file_list_zip_unique = list(sorted((set(file_list_zip))))
print(len(file_list_zip_unique))
print(len(file_list_zip))

cnt_check = pd.DataFrame(file_list_zip, columns = ['id'])
# cnt_check['id2'] = cnt_check['id']
# cnt_check['cnt'] = cnt_check.groupby(by = ['id2']).count()
cnt_check_group = pd.DataFrame(cnt_check.value_counts(), columns = ['cnt'])
print(len(cnt_check_group[cnt_check_group['cnt'] == 4]))
print(len(cnt_check_group[cnt_check_group['cnt'] == 3]))
print(len(cnt_check_group[cnt_check_group['cnt'] == 2]))
print(len(cnt_check_group[cnt_check_group['cnt'] == 1]))

data_root = "/mnt/stsi/stsi3/Internal/ukbb_cardiac"

# convert dicom file to nifti file

list_error = []
for eid in file_list_zip_unique[0:1]:
    try:
        # Unpack the data
        
        files = [s for s in file_list_0 if eid in s]
        
        for f in files:   


            foldnum=f.split("/")[9]
            nifti_dir = os.path.join(data_root,"nifti",foldnum,str(eid))   #str(eid))
            dicom_tem = os.path.join(data_root, 'dicom')
            if not os.path.exists(nifti_dir):
                os.mkdir(nifti_dir)
            if not os.path.exists(dicom_tem):
                os.mkdir(dicom_tem)

            #압축 해제


            with zipfile.ZipFile(f, 'r') as existing_zip:
                existing_zip.extractall(dicom_tem)

            # Process the manifest file
        #     if os.path.exists(os.path.join(dicom_dir, 'manifest.cvs')):
        #         os.system('cp {0} {1}'.format(os.path.join(dicom_dir, 'manifest.cvs'),
        #                                       os.path.join(dicom_dir, 'manifest.csv')))

            # 압축 해제 한 폴더에 manifest.cvs 파일이 있으면 아래 4줄 실행해야하고, manifest.csv 파일이 있으면 주석처리 하면 됨
            src = os.path.join(dicom_tem, 'manifest.cvs')
            dst = 'manifest' + '.csv'
            dst = os.path.join(dicom_tem, dst)
            os.rename(src, dst)

            process_manifest(os.path.join(dicom_tem, 'manifest.csv'),
                             os.path.join(dicom_tem, 'manifest2.csv'))
            df2 = pd.read_csv(os.path.join(dicom_tem, 'manifest2.csv'), error_bad_lines=False)
            os.remove(os.path.join(dicom_tem, 'manifest.csv'))
            os.remove(os.path.join(dicom_tem, 'manifest2.csv'))
            # Patient ID and acquisition date
            pid = df2.at[0, 'patientid']
            date = dateutil.parser.parse(df2.at[0, 'date'][:11]).date().isoformat()

            # Organise the dicom files
            # Group the files into subdirectories for each imaging series
            for series_name, series_df in df2.groupby('series discription'):
                series_dir = os.path.join(dicom_tem, series_name)
                if not os.path.exists(series_dir):
                    os.mkdir(series_dir)
                series_files = [os.path.join(dicom_tem, x) for x in series_df['filename']]
            #     os.system('mv {0} {1}'.format(' '.join(series_files), series_dir))   # 파일을 해당 디렉토리로 옮겨야함
        #         file_source = dicom_dir
                file_destination = series_dir

        #         get_files = os.listdir(file_source)

                for g in series_files:
                    shutil.move(g, file_destination)

        # Convert dicom files and annotations into nifti images
        dset = Biobank_Dataset(dicom_tem)
        dset.read_dicom_images()
        # if not os.path.exists(dicom_dir + '\\' + 'nifti'):
        #     os.mkdir(dicom_dir + '\\' + 'nifti')
        dset.convert_dicom_to_nifti(nifti_dir)

        # Remove intermediate files
#        if os.path.exists(dicom_tem):
#            shutil.rmtree(dicom_tem)

        print(eid)
        
    except:
        list_error.append(eid)
#        if os.path.exists(dicom_tem):
#            shutil.rmtree(dicom_tem)

    list_error
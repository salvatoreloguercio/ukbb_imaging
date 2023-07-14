# Copyright 2017, Wenjia Bai. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
    This script demonstrates a pipeline for cardiac MR image analysis.
    """
import os
import urllib.request
import shutil
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))


if __name__ == '__main__':

    # Analyse show-axis images
    print('******************************')
    print('  Short-axis image analysis')
    print('******************************')

    # Deploy the segmentation network
    print('Deploying the segmentation network ...')
#    os.system('CUDA_VISIBLE_DEVICES={0} python3 common/deploy_network.py --seq_name sa --data_dir demo_image '
#              '--model_path trained_model/FCN_sa'.format(CUDA_VISIBLE_DEVICES))
    os.system('python ukbb_cardiac/common/deploy_network.py --seq_name sa --data_dir E:/hcm_seg/nifti_dest '
              '--model_path trained_model/FCN_sa')    

    # Evaluate ventricular volumes
    print('Evaluating ventricular volumes ...')
    os.system('python ukbb_cardiac/short_axis/eval_ventricular_volume.py --data_dir E:/hcm_seg/nifti_dest '
              '--output_csv demo_csv/all_table_ventricular_volume.csv')

    # Evaluate wall thickness
    print('Evaluating myocardial wall thickness ...')
    os.system('python ukbb_cardiac/short_axis/eval_wall_thickness.py --data_dir E:/hcm_seg/nifti_dest '
              '--output_csv demo_csv/all_table_wall_thickness.csv')

    # Evaluate strain values
    if shutil.which('mirtk'):
        print('Evaluating strain from short-axis images ...')
        os.system('python ukbb_cardiac/short_axis/eval_strain_sax.py --data_dir E:/hcm_seg/nifti_dest '
                  '--par_dir par --output_csv demo_csv/all_table_strain_sax.csv')

    # Analyse long-axis images
    print('******************************')
    print('  Long-axis image analysis')
    print('******************************')

    # Deploy the segmentation network
    print('Deploying the segmentation network ...')
    os.system('python ukbb_cardiac/common/deploy_network.py --seq_name la_2ch --data_dir E:/hcm_seg/nifti_dest '
              '--model_path trained_model/FCN_la_2ch')

    os.system('python ukbb_cardiac/common/deploy_network.py --seq_name la_4ch --data_dir E:/hcm_seg/nifti_dest '
              '--model_path trained_model/FCN_la_4ch')

    os.system('python ukbb_cardiac/common/deploy_network.py --seq_name la_4ch --data_dir E:/hcm_seg/nifti_dest '
              '--seg4 --model_path trained_model/FCN_la_4ch_seg4')

    # Evaluate atrial volumes
    print('Evaluating atrial volumes ...')
    os.system('python ukbb_cardiac/long_axis/eval_atrial_volume.py --data_dir E:/hcm_seg/nifti_dest '
              '--output_csv demo_csv/all_table_atrial_volume.csv')

    # Evaluate strain values
    if shutil.which('mirtk'):
        print('Evaluating strain from long-axis images ...')
        os.system('python ukbb_cardiac/long_axis/eval_strain_lax.py --data_dir E:/hcm_seg/nifti_dest '
                  '--par_dir par --output_csv demo_csv/all_table_strain_lax.csv')

    # Analyse aortic images
    print('******************************')
    print('  Aortic image analysis')
    print('******************************')

    # Deploy the segmentation network
    print('Deploying the segmentation network ...')
    os.system('python ukbb_cardiac/common/deploy_network_ao.py --seq_name ao --data_dir E:/hcm_seg/nifti_dest '
              '--model_path trained_model/UNet-LSTM_ao')

    # Evaluate aortic areas
    print('Evaluating atrial areas ...')
    # need bolld_pressure_info.csv for all data
    os.system('python ukbb_cardiac/aortic/eval_aortic_area.py --data_dir E:/hcm_seg/nifti_dest '
              '--pressure_csv demo_csv/blood_pressure_info.csv --output_csv demo_csv/all_table_aortic_area.csv')

    print('Done.')

import pandas as pd
import numpy as np
datasetpath = '../../../MachineLearning/Dataset/Kaggle'


def DataInit():
    # load image npy
    df_img1 = np.load(
        f"{datasetpath}/pannuke/Part 1/Images/images.npy", mmap_mode='r')
    df_img2 = np.load(
        f"{datasetpath}/pannuke2/Images/images.npy", mmap_mode='r')
    df_img3 = np.load(
        f"{datasetpath}/pannuke3/Images/images.npy", mmap_mode='r')
    # load mask npy
    df_mask1 = np.load(
        f"{datasetpath}/pannuke/Part 1/Masks/masks.npy", mmap_mode='r')
    df_mask2 = np.load(
        f"{datasetpath}/pannuke2/Masks/masks.npy", mmap_mode='r')
    df_mask3 = np.load(
        f"{datasetpath}/pannuke3/Masks/masks.npy", mmap_mode='r')
    # Import type npy
    df_ttype1 = pd.DataFrame(
        np.load(f"{datasetpath}/pannuke/Part 1/Images/types.npy", mmap_mode='r'))
    df_ttype1['dataset'] = 1
    df_ttype2 = pd.DataFrame(
        np.load(f"{datasetpath}/pannuke2/Images/types.npy", mmap_mode='r'))
    df_ttype2['dataset'] = 2
    df_ttype3 = pd.DataFrame(
        np.load(f"{datasetpath}/pannuke3/Images/types.npy", mmap_mode='r'))
    df_ttype3['dataset'] = 3
    df_ttype = pd.concat([df_ttype1, df_ttype2, df_ttype3], axis=0)
    df_ttype.reset_index(inplace=True)
    df_ttype.rename(columns={'index': 'IndexAtDataSet'}, inplace=True)
    df_ttype.rename(columns={'0': 'tissueType'}, inplace=True)
    data_dict ={
        'df_img1':df_img1,
        'df_img2':df_img2,
        'df_img3':df_img3,
        'df_mask1':df_mask1,
        'df_mask2':df_mask2,
        'df_mask3':df_mask3,
        'df_ttype':df_ttype,

    }
    return data_dict


def get_cell_count(image_file):
    image_file = np.random(256, 256, 6)
    # 使用Pandas处理图像文件
    image_df = pd.DataFrame(image_file.reshape(
        256*256, 6))

    # Reformat
    image_df_nobackground = image_df[image_df.columns['-1']]
    # 处理图像数据，获取每个类别的医学细胞数量
    cell_counts = image_df_nobackground[image_df_nobackground != 0].nunique(
    ).todict()

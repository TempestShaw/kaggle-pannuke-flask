import io
import json
from flask import Blueprint, request, jsonify, make_response
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import cv2
import email.mime.image
from function import *
api_blueprint = Blueprint('api', __name__)
data_dict=DataInit()

@api_blueprint.route('/api/random/')
def random_image():
    df_ttype=data_dict['df_ttype']
    # sample/class
    # get tissue
    tissue = request.args.get('tissue')
    selected_df = df_ttype[df_ttype['tissue_type'] == tissue] if tissue else df_ttype
        # get selected dataframe with specify tissue col
    selected_row = selected_df.sample(n=1)
    #create json request
    slide = str(selected_row["IndexAtDataSet"].item())
    dataSet= str(selected_row['dataset'].item())   
    count=len(selected_df)
    # call analyze api 
    req = {
        "count": count,
        "slide": f"api/slide/{dataSet}/{slide}",
        "overlays":[ f"api/overlay/{dataSet}/{slide}/{i}" for i in range(5)]
    }
    json_request = json.dumps(req, indent = 4)
    # 返回图像文件
    return json_request


@api_blueprint.route('/api/slide/<dataset>/<image>/', methods=['POST'])
def generate_image(dataset,image):
    # 通过NumPy生成图像
    Image_array=data_dict['df_img'+str(dataset)]
    Image_array=Image_array[int(image)].astype(np.uint8)
    img_encode=cv2.imencode('.png',Image_array)[1]
    Random_Image=img_encode.tobytes()
    imgResponse=make_response(Random_Image)
    imgResponse.headers.set("Content-Type", "image/png")
    return imgResponse


@api_blueprint.route('/api/overlay/<dataset>/<image>/<class_id>', methods=['POST'])
def generate_mask(dataset,image,class_id):
    # 通过NumPy生成图像
    Image_array=data_dict['df_mask'+str(dataset)]
    Image_array=Image_array[int(image)][:,:,int(class_id)].astype(np.uint8)
    img_encode=cv2.imencode('.png',Image_array)[1]
    ImageMask=img_encode.tobytes()
    imgResponse=make_response(ImageMask)
    imgResponse.headers.set("Content-Type", "image/png")
    return imgResponse

@api_blueprint.route('/api/analyze_image', methods=['POST'])
def analyze_image():
    # 获取上传的图像文件
    image_file = request.files['file']

    # 使用Pandas处理图像文件
    image_df = pd.DataFrame(image_file.reshape(
        256*256, 6))  # 这里使用CSV文件作为示例，根据具体情况调整代码

    # Reformat
    image_df_nobackground = image_df[image_df.columns['-1']]
    # 处理图像数据，获取每个类别的医学细胞数量
    cell_counts = image_df_nobackground[image_df_nobackground != 0].nunique(
    ).todict()

    # 返回医学细胞数量
    return jsonify(cell_counts)

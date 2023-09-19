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


@api_blueprint.route('/api/slide/<string:dataset>/<string:image>/', methods=['POST'])
def generate_image(dataset,image):
    # 通过NumPy生成图像
    Image_array=data_dict['df_img'+str(dataset)]
    Image_array=Image_array[int(image)].astype(np.uint8)
    img_encode=cv2.imencode('.png',Image_array)[1]
    Random_Image=img_encode.tobytes()
    imgResponse=make_response(Random_Image)
    imgResponse.headers.set("Content-Type", "image/png")
    return imgResponse


@api_blueprint.route('/api/overlay/<string:dataset>/<string:image>/<class_id>', methods=['POST'])
def generate_mask(dataset,image,class_id):
    # 通过NumPy生成图像
    Image_array=data_dict['df_mask'+str(dataset)]
    Image_array=Image_array[int(image)][:,:,int(class_id)].astype(np.uint8)
    img_encode=cv2.imencode('.png',Image_array)[1]
    ImageMask=img_encode.tobytes()
    imgResponse=make_response(ImageMask)
    imgResponse.headers.set("Content-Type", "image/png")
    return imgResponse

@api_blueprint.route('/api/slide-mask/<string:dataset>/<string:image>/', methods=['POST'])
def generate_maskimage(dataset,image):
    colorList=[(255, 0, 0),(0, 255, 0),(0, 0, 255),(255, 255, 0),(255, 0, 255)]
    #Call api
    dataset_str = str(dataset)
    image_str = str(image)
    api_url = f'http://127.0.0.1:5000/api/slide/{dataset_str}/{image_str}/'
    response = requests.post(api_url)
    if response.status_code == 200:
        image_np = np.frombuffer(response.content, np.uint8)
        originalImage = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    mergedImage = np.zeros((256, 256, 4), dtype=np.uint8)
    mergedImage[:, :, 0:3] = originalImage
    for index in range(5):
        
        #Call api
        response = requests.post(f'http://127.0.0.1:5000/api/overlay/{dataset_str}/{image_str}/{index}')
        if response.status_code == 200:
            image_np = np.frombuffer(response.content, np.uint8)
            layerColor = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
            # layer = cv2.cvtColor(layer, cv2.COLOR_BGR2GRAY)
            # layerColor = cv2.cvtColor(layer, cv2.COLOR_GRAY2BGR)
            print(layerColor)
            df = pd.DataFrame(layerColor.reshape(256,256*3))
            df.to_csv('data.csv', index=False)
            layerColor[np.where((layerColor > [0, 0, 0]).all(axis=2))] = colorList[index]

        originalImage = cv2.addWeighted(originalImage, 1, layerColor, 0.5, 0)
        
    img_encode=cv2.imencode('.png',originalImage)[1]
    ImageWithMask=img_encode.tobytes()
    imgResponse=make_response(ImageWithMask)
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

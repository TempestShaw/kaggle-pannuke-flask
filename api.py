import io
from flask import Blueprint, request, jsonify, send_file
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/api/random/')
def random_image():
    #sample/class
    randomclass = np.random.randint(1,6)
    randomimage = np.random.randint(1,6)
    tissue= request.args.get('tissue')
    # call analyze api
    req={
        "count"
    }
    if response.status_code == 200:
        cell_counts = response.json()
        # tackle with API response

    else:
        pass
    # 返回图像文件
    return send_file(image_stream, mimetype='image/png'), cell_counts


@api_blueprint.route('/api/slide/<image>/', methods=['POST'])
def generate_image(image):
    # 通过NumPy生成图像
    image_array = {image}
    fig, ax = plt.subplots()
    ax.imshow(image_array, cmap='gray')
    ax.axis('off')

    # save image into io
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # call analyze api
    response = requests.post(
        'http://localhost:5000/api/analyze_image', files={'file': image_array})

    if response.status_code == 200:
        cell_counts = response.json()
        # tackle with API response

    else:
        pass
    # 返回图像文件
    return send_file(image_stream, mimetype='image/png'), cell_counts


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

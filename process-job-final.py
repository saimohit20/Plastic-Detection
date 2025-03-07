from datetime import datetime
import json
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import io
import boto3
from PIL import Image
from io import BytesIO
from sagemaker.s3 import S3Downloader
date_today = datetime.today().strftime('%Y-%m-%d')


year = date_today[0:4]
month = date_today[5:7]
day = date_today[8:10]

#date_today = '2023-02-18'

s3 = boto3.resource('s3')
my_bucket = s3.Bucket('')




num_detections = []
file_key = f'/{year}/{month}/{day}/{year}_{month}_{day}.json'
output = S3Downloader.read_file(file_key)
detections = json.loads(output)
for i in detections:
    image_path_s3 = f'images/{year}/{month}/{day}/{i[24:-4]}'
    object = my_bucket.Object(image_path_s3)
    response = object.get()
    file_stream = response['Body']
    img = Image.open(file_stream)
    width, height = img.size
    plt.imshow(img)
    detections_in_image = []
    data = detections[i]
    colors = dict()
    for j in data:
        detections_in_image.append(j)
    for k in detections_in_image:
        klass, score ,x0 ,y0 ,x1 ,y1 = k
        if score < 0.25:
            continue
        cls_id = int(klass)
        if cls_id not in colors:
            colors[cls_id] = (random.random(),random.random(),random.random())
        xmin = int(x0 * width) 
        ymin = int(y0 * height)
        xmax = int(x1 * width)
        ymax = int(y1 * height)
        
        rect = plt.Rectangle(
            (xmin,ymin),
            xmax - xmin,
            ymax - ymin,
            fill = False,
            edgecolor = colors[cls_id],
            linewidth = 3.5,
        )
        plt.gca().add_patch(rect)
        plt.gca().text(
            xmin,
            ymin -2,
            "{:.3f}".format(score),
            bbox = dict(facecolor = colors[cls_id], alpha = 0.5),
            fontsize = 12,
            color = "white",
        )
        
        image_data = my_bucket.Object(f"output-images/{year}/{month}/{day}/{i[24:-4]}")
        file_stream = BytesIO()
        plt.savefig(file_stream, format = 'jpeg')
        image_data.put(Body = file_stream.getvalue())
    #plt.show()
    plt.close()
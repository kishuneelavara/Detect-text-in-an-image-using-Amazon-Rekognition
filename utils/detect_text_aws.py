import pandas as pd
import boto3
import cv2
from botocore.exceptions import ClientError

credential = pd.read_csv("new_user_credentials.csv")
access_key_id = credential['Access key ID'][0]
secret_access_key = credential['Secret access key'][0]

client = boto3.client('rekognition', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)


def get_text(img):
    try:

        filename=img
        img='static/uploads/'+filename
        photo1 = cv2.imread(img)
        imgHeight, imgWidth, channels = photo1.shape

        with open(img, 'rb') as source_image:
            source_bytes = source_image.read()

        response = client.detect_text(
            Image={
                'Bytes': source_bytes
            })

        res_response={}

        for i in range(len(response['TextDetections'])):
            if 'ParentId' not in response['TextDetections'][i].keys():
                res_response[i] = {}
                res_response[i]['Text']=response['TextDetections'][i]['DetectedText']
                res_response[i]['Confidence']=response['TextDetections'][i]['Confidence']
                dimensions = response['TextDetections'][i]['Geometry']['BoundingBox']
                boxWidth = dimensions['Width']
                boxHeight = dimensions['Height']
                boxLeft = dimensions['Left']
                boxTop = dimensions['Top']
                # Plotting points of rectangle
                start_point = (int(boxLeft * imgWidth), int(boxTop * imgHeight))
                end_point = (int((boxLeft + boxWidth) * imgWidth), int((boxTop + boxHeight) * imgHeight))
                # Drawing Bounding Box on the coordinates
                thickness = 2
                color = (36, 255, 12)
                photo1 = cv2.rectangle(photo1, start_point, end_point, color, thickness)
                # cv2.imshow('Target Image', photo1)
                # cv2.waitKey(0)
        print(res_response)
        cv2.imwrite("static/result/"+filename,photo1)
        statement="success"
        return response, filename, res_response,statement
    except:
        statement="Something went wrong"
        return None, None, None, statement




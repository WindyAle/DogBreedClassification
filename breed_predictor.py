import os
import numpy as np
import torch
import torchvision

from matplotlib import pyplot as plt
from PIL import Image

# 실제로 img_prediction 사용 시에는 호출하는 코드 쪽에서 모델을 로드해놓은 상태여야함!!!

os.environ['KMP_DUPLICATE_LIB_OK']='True'

transform = torchvision.transforms.Compose([ # 학습 과정에 사용한 transform과 동일한 설정.
    torchvision.transforms.Resize(256),
    torchvision.transforms.CenterCrop(224),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.RandomHorizontalFlip(p = 0.5)
    ])

# 코드 실행폴더와 동일한 위치에 dataset 폴더가 있어야한다.
cwd = os.getcwd() + '/'
trainset_path = cwd + "dataset/trainset/"
trainset = torchvision.datasets.ImageFolder(trainset_path, transform = transform)


classification_model = torch.load(cwd + "classification_model.pt") # 모델 로딩 후 평가용으로 설정.
classification_model.eval()

def breed_prediction(image_path) :

    image_test = Image.open(image_path)

    #transform the image
    img = transform(image_test)
    
    # get the class predicted 
    pred = int(np.squeeze(classification_model(img.unsqueeze(0).cuda()).data.max(1, keepdim=True)[1].cpu().numpy()))
    
    # the number is also the index for the class label
    pred_result = trainset.classes[pred]
    image_result = Image.open(trainset_path + pred_result + '/' + pred_result + '-2.jpg')
    pred_result = pred_result.lower()

    fig = plt.figure(figsize=(10, 10))
    rows = 1
    columns = 2

    fig.add_subplot(rows, columns, 1)
    plt.imshow(image_test)
    plt.axis('off')
    plt.title("Input")

    fig.add_subplot(rows, columns, 2)
    plt.imshow(image_result)
    plt.axis('off')
    plt.title("Output")

    plt.show(block=False)

    return pred_result

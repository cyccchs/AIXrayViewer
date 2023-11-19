import os
import torch
from torchvision.transforms import v2
from torchvision import tv_tensors

def toTensor(img_pil, bbox_list):
    bbox_tensor = torch.Tensor(bbox_list)
    pil2tensor = v2.PILToTensor()
    img_tensor = pil2tensor(img_pil)
    return img_tensor, bbox_tensor

def fromTensor(img_tensor, bbox_tensor):
    tensor2pil = v2.ToPILImage()
    img_pil = tensor2pil(img_tensor)
    bbox_list = bbox_tensor.tolist()
    return img_pil, bbox_list

def normalized_bbox(bbox, img):
    w, h = img.size[0], img.size[1]
    center_x = int(w*float(bbox[0]))
    center_y = int(h*float(bbox[1]))
    dx = int(w*float(bbox[2])/2)
    dy = int(h*float(bbox[3])/2)
    return [center_x-dx, center_y-dy, center_x+dx, center_y+dy]

def get_bbox(img_path, img):
    label_path = img_path.replace('jpg', 'txt')
    with open(label_path, 'r') as f:
        bbox_list = []
        for label in f.readlines():
            label = label.replace('\n', '')
            bbox = label.split(' ')[1:]
            bbox_list.append(normalized_bbox(bbox, img))
        return bbox_list

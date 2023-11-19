import torch
from torchvision.transforms import v2
from torchvision import tv_tensors

class XrayAugmentation:
    def __init__(self, target_size=None, padding=None):
        pass
        
    def augmentation(self, img, bbox, degrees=(0,0), method='Normal'):
        if method=='Demo':
            trans_list = []
            result_list = []
            trans.append(
            transforms1 = v2.Compose([
                v2.RandomHorizontalFlip(p=1),
                v2.ToDtype(torch.float32, scale=True),
            ]))
            trans_list.append(
            transforms2 = v2.Compose([
                v2.RandomVerticalFlip(p=1),
                v2.ToDtype(torch.float32, scale=True),
            ]))
            trans_list.append(
            transforms3 = v2.Compose([
                v2.RandomHorizontalFlip(p=1),
                v2.RandomVerticalFlip(p=1),
                v2.ToDtype(torch.float32, scale=True),
            ]))
            trans_list.append(
            transforms4 = v2.Compose([
                v2.RandomRotation(degrees=degrees),
                v2.ToDtype(torch.float32, scale=True),
            ]))
            for transform in trans_list:
                result_list.append(transform(img, bbox))


            return 
        elif method=='Normal':
            if self.w_state['Hflip'].get()==1:
                transforms = v2.Compose([
                    v2.RandomHorizontalFlip(p=1),
                    v2.ToDtype(torch.float32, scale=True),
                ])
                print('H')
            if self.w_state['Vflip'].get()==1:
                transforms = v2.Compose([
                    v2.RandomVerticalFlip(p=1),
                    v2.ToDtype(torch.float32, scale=True),
                ])
                print('V')

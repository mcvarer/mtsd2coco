"""
This script create coco.json format from dataset
"""
import os.path
from coco_formatter.mapillary_dataset import TrafficInventoryDataset
from coco_formatter.helper import config_reader, id_generator

import json


cfgPath = os.path.join('coco_formatter', 'schemas', 'config.json')
cocoPath = os.path.join('coco_formatter', 'schemas', 'coco.json')
export = os.path.join('coco_formatter', 'schemas', 'instances_train_coco_test.json')
labelsPath = os.path.join('coco_formatter',  'schemas', 'labels.json')

cfg = config_reader(cfgPath)
coco = config_reader(cocoPath)
labels = config_reader(labelsPath)

classnames = []

result_json = {}

for index, (key, val) in enumerate(labels.items()):
    supercategory = key.split('--')[0]
    if supercategory == 'other-sign':
        continue
    result_json[key] = index
    classnames.append(
        {"supercategory": supercategory,
         "id": val,
         "name": key})

coco.categories = classnames


def saveCocojson(export, coco):

    with open(export, 'w') as outfile:
        json.dump(coco, outfile)


def main():
    rootPath = cfg.rootPath
    imagesPath = cfg.imagesPath
    train_dataset = TrafficInventoryDataset(rootPath=rootPath,
                                            imagesPath=imagesPath,
                                            type="train",
                                            transform=False)
    imgInformations = []
    annotations = []
    from tqdm import tqdm
    image_id = 0
    for (filename, classnames, bbox, w, h, area) in tqdm(train_dataset):
        if not classnames:
            continue
        imgInformations.append({
            "license": 2021,
            "file_name": filename,
            "coco_url": None,
            "width": w,
            "height": h,
            "id": image_id
        })
        for k in range(len(bbox)):
            annotations.append(
                {
                    "segmentation": [],
                    "area": area[k],
                    "iscrowd": 0,
                    "image_id": image_id,
                    "bbox": bbox[k],
                    "category_id": classnames[k],
                    "id": id_generator()
                }
            )
        image_id += 1

    coco.images = imgInformations
    coco.annotations = annotations

    saveCocojson(export, coco)


main()

import os
import json


class TrafficInventoryDataset:
    """Face Landmarks dataset."""

    def __init__(self, rootPath, imagesPath, type, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.root = rootPath
        self.imagesPath = imagesPath
        self.annotationPath = os.path.join(rootPath, "annotations")
        self.type = self.selectType(type)
        self.readLines()
        self.transform = transform
        self.labels = read_labels(os.path.join(rootPath, 'schemas/labels.json'))
        self.transforms = transform
        self.len = self.__len__()


    def readLines(self):
        with open(self.type, 'r') as f:
            self.counts = f.read().splitlines()

    def load_anno(self, image_key):
        with open(os.path.join(self.annotationPath, f"{image_key}.json"), 'r') as fid:
            return json.load(fid)

    def __len__(self):
        self.num_lines = sum(1 for line in open(self.type))
        return self.num_lines

    def __getitem__(self, indice):
        image_key = self.counts[indice]
        filename = f"{image_key}.jpg"
        anno = self.load_anno(image_key)
        classnamesArr = []
        bboxArr = []
        areaArr = []

        print("indice:", indice)
        h, w = anno['height'], anno['width']

        for i, obj in enumerate(anno['objects']):
            # print(obj)

            x1 = obj['bbox']['xmin']
            y1 = obj['bbox']['ymin']
            x2 = obj['bbox']['xmax']
            y2 = obj['bbox']['ymax']

            name = obj['label']

            classname = self.labels.get(name)
            if name == "other-sign":
                # filename = None
                # w, h = None, None
                continue

            bbox = [x1, y1, x2-x1, y2-y1]
            area = (x2-x1) * (y2-y1)
            classnamesArr.append(classname)
            bboxArr.append(bbox)
            areaArr.append(area)
            print("-------------------")
        return filename, classnamesArr, bboxArr, w, h, areaArr

    def selectType(self, type):
        return os.path.join(self.root, 'splits', type + ".txt")

def read_labels(labelPath):
    with open('coco_formatter/schemas/labels.json', 'r') as f:
        labels = json.load(f)
        return labels
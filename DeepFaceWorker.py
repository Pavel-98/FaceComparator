from io import BytesIO

import cv2
import requests
from PIL import Image
from deepface import DeepFace
from deepface.DeepFace import represent
from deepface.commons import distance
from deepface.commons.functions import preprocess_face
from face_recognition import load_image_file
from jupyter_core.migrate import dst


class DeepFaceWorker:
    def __init__(self):
        self.model=None
        self.model_name='VGG-Face'
        self.distance_metric='euclidean'
        self.enforce_detection=False
        self.detector_backend='retinaface'

    def toGetImageFromSite(self, site):
        image = BytesIO(requests.get(site).content)
        return load_image_file(image)

    def loadingImageFile(self, path):
        result = load_image_file(path)
        return result




    def face_encodings(self, image):
        try:
            result=represent(image, detector_backend=self.detector_backend)
            return [result]
        except Exception as e:
            return []


    def face_encoding(self,image):
        return self.face_encodings(image)[0]

    def face_distance(self, encoding1, encoding2):
        result=self.compare_faces(encoding1, encoding2, self.distance_metric)
        return result

    def face_distances(self, encodings, encoding):
        distances=[]
        for encodingItem in encodings:
            distances.append(self.face_distance(encodingItem, encoding))
        return distances

    def compare_faces(self, img1_representation, img2_representation, j):
        distance1 = None
        if j == 'cosine':
            distance1 = distance.findCosineDistance(img1_representation, img2_representation)
        elif j == 'euclidean':
            distance1 = distance.findEuclideanDistance(img1_representation, img2_representation)
        elif j == 'euclidean_l2':
            distance1 = distance.findEuclideanDistance(dst.l2_normalize(img1_representation),
                                                 dst.l2_normalize(img2_representation))
        return distance1
path1='R.jpg'
path2='DV.jpg'

'''represent('Girl.jpg', detector_backend='ssd')#"Дівчина.jpg")
print(DeepFace.verify(path1, path2))'''
'''

image1= cv2.imread(path1)
image2=cv2.imread(path2)
site='https://www.goldderby.com/wp-content/uploads/2022/12/Ralph-fiennes-movies-ranked.jpg?w=620&h=360&crop=1'
image1=DeepFaceWorker().face_encoding(image1)
image2=DeepFaceWorker().face_encoding(image2)
result=DeepFaceWorker().compare_faces(image1, image2, 'cosine')

print(result)'''

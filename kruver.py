import requests
from bs4 import BeautifulSoup as bs
from PIL import Image
from pixelsort import pixelsort
import random
import urllib
import cloudinary.uploader
import re
import os
from pymongo import MongoClient

cloud_name=os.environ["cloud_name"]
api_key=os.environ["api_key"]
api_secret=os.environ["api_secret"]
db_uri=os.environ["db_client"]


cloudinary.config( 
  cloud_name=cloud_name, 
  api_key=api_key, 
  api_secret=api_secret
)

dbClient=MongoClient(db_uri)

mydb = dbClient["kruDB"]
mycol=mydb["kruv"]

class ImageManipulater:
    def __init__(self):
        self.image_name=""
        self.original_image_url=""
        self.sorted_url=""

    def find_image(self):
        r=requests.get("https://www.sozcu.com.tr/kategori/gundem/")
        soup=bs(r.content,"html.parser")
        images=soup.find_all('div',{'class':'news-item'})
        images_list=[]
        for i in images:
            img=i.find("img")
            images_list.append(img['src'])
        self.original_image_url=random.choice(images_list)    
    def sort(self):
        post_image=Image.open(urllib.request.urlopen(self.original_image_url))
        sorted_image=pixelsort(post_image)
        print(self.original_image_url)
        self.image_name = re.search(r"(?<=iecrop/)\w.*(?=\.jpg)",self.original_image_url).group()
        print(self.image_name)
        sorted_image.save(f"sorted_images_folder\{self.image_name}.png")

    def upload(self):
        sorted_response=cloudinary.uploader.upload(f"sorted_images_folder\{self.image_name}.png", folder = "kru/")
        self.sorted_url=sorted_response["secure_url"]
        os.remove(f"sorted_images_folder\{self.image_name}.png")

def insert_db(var):
    x=mycol.insert_one(var)
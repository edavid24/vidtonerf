import os
import requests
import json
from models.scene import SceneManager, Video, Image
from services.queue_service import RabbitMQService
from uuid import uuid4, UUID
from video_to_images import split_video_into_frames
from werkzeug.utils import secure_filename

from pymongo import MongoClient

class ClientService:
    def __init__(self, manager: SceneManager, rmqservice: RabbitMQService):
        self.manager = manager
        self.rmqservice = rmqservice
        
        #self.queue = queue

    # TODO No longer use video class
    def handle_incoming_video(self, video_file):
        # receive video and check for validity
        file_name = secure_filename(video_file.filename)
        if file_name == '':
            print("ERROR: file not received")
            return None

        file_ext = os.path.splitext(file_name)[1]
        if file_ext != ".mp4":
            print("ERROR: improper file extension uploaded")
            return None

        # generate new id and save to file with db record
        uuid = str(uuid4())
        video_name = uuid + ".mp4"
        videos_folder = "raw/"+uuid+"/video"
        video_file_path = os.path.join(videos_folder,video_name)
        
        video_file.save(video_file_path)

        video = Video(video_file_path)
        self.manager.set_video(uuid, video)

        ## TODO add following path into web sever
        imgs_folder = "raw/"+ uuid + "/imgs"

        # split video into images and store into imgs_folder
        blur_check = True
        split_video_into_frames(video_file_path, imgs_folder, 200, blur_check)

        # convert images into Image objects
        image_array = []
        
        for filename in os.listdir(imgs_folder):
        # Check if the file is a regular file (not a directory)
            if os.path.isfile(os.path.join(imgs_folder, filename)):
                image_array.append(Image(file_path=filename))
        
        #TODO change this from publishing a video to publishing a set of images
        self.rmqservice.publish_sfm_job(uuid, image_array)

        return uuid

    # Returns a string describing the status of the video in the database
    # along with a path to the final video, if available
    def get_nerf_video_path(self, uuid):
        # TODO: depend on mongodb to load file path
        # return None if not found
        nerf = self.manager.get_nerf(uuid)
        if nerf:
            return ("Video ready", nerf.rendered_video_path)
        return None
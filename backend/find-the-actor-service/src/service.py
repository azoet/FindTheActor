import base64
import json
from repository.imdb import IMDbRepository, IMDbRepositoryException
from repository.images import ImagesRepository, ImagesRepositoryException
from repository.storage import StorageRepository, StorageRepositoryException


class FindTheActorService():
    def __init__(self, conf):
        self.imdbRepository = IMDbRepository(**conf['repository']['imdb'])
        self.imagesRepository = ImagesRepository(
            **conf['repository']['images'])
        self.storageRepository = StorageRepository(
            **conf['repository']['storage'])

    def search_movie(self, movie_name):
        try:
            return self.imdbRepository.search_movies(movie_name)
        except IMDbRepositoryException:
            return []

    def list_cast_from_movie(self, movie_id):
        try:
            return self.imdbRepository.list_cast(movie_id)
        except IMDbRepositoryException:
            return []

    def list_images_from_actor_name(self, actor_name):
        try:
            return self.imagesRepository.search(actor_name)
        except ImagesRepositoryException:
            return []

    def download_store_actor_image(self, actor_name, image_url):
        try:
            return self.storageRepository.download(actor_name.replace(' ', '_').lower(), image_url)
        except StorageRepositoryException:
            return []

    def prepare_movie_db(self, movie_id):
        # Calls IMDB to get the cast
        cast = self.list_cast_from_movie(movie_id)
        # Find images for each cast members
        for c in cast:
            # Download each files
            for i in self.list_images_from_actor_name(
                    c['name']):
                self.download_store_actor_image(c['name'], i)

        return {
            'Status OK'
        }

    def run_image_facerec(self, file_name, file_content):
        (boxed_image, boxes) = self.imagesRepository.face_recognition(
            file_name, file_content)
        # Store main image
        self.storageRepository.store('transient', file_name, file_content)
        # Store boxed image
        self.storageRepository.store(
            'transient', 'Boxed_%s' % file_name, boxed_image)
        # Store boxes coordinates
        file_wo_ext = file_name.rsplit('.')
        self.storageRepository.store_json(
            'transient', 'Boxes_%s.json' % file_wo_ext[0], boxes_to_dict(boxes)
        )

        return {'yes'}

    def get_file(self, file_name):
        return self.storageRepository.get_file("transient/%s" % file_name)

    def get_cropped_image(self, file_name, box_number):
        file_name_wo_ext = file_name.rsplit('.')[0]
        boxes_payload = self.get_file("Boxes_%s.json" % file_name_wo_ext)
        boxes = json.loads(base64.b64decode(
            boxes_payload['encoded_binary_content']))
        image = self.storageRepository.get_file("transient/%s" % file_name)
        return self.imagesRepository.crop_image(image['encoded_binary_content'], boxes[box_number-1])

    def store_image(self, file_name, encoded_binary_content, encode=False):
        self.storageRepository.store(
            'transient', file_name, encoded_binary_content, encode)


def boxes_to_dict(boxes):
    return [box_to_dict(box) for box in boxes]


def box_to_dict(box):
    return {
        'x': box[0],
        'y': box[1],
        'width': box[2],
        'height': box[3]
    }

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
            'cast': cast,
        }

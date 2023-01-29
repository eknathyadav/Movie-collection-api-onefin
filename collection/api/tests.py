from rest_framework import status
from rest_framework.test import APITestCase
from collection.models import User, Collection, Genre, Movie
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class CollectionAPITestCase(APITestCase):
    def setUp(self):
        self.sample_user = "eknath2023"
        self.sample_password = "eknath2023"
        user_obj = User.objects.create(
            username=self.sample_user, password=self.sample_password)
        self.token = RefreshToken.for_user(user_obj)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer '+str(self.token.access_token))
        genre_obj1 = Genre.objects.create(genre_name="Crime")
        genre_obj2 = Genre.objects.create(genre_name="Thriller")
        movie_obj = Movie.objects.create(
            title="Dabang",
            description="Movie_desc"
        )
        movie_obj.genres.add(genre_obj1, genre_obj2)
        self.collection_obj = Collection.objects.create(
            title="MY_collection_1",
            description="Collection_desc",
            user=user_obj
        )
        self.collection_obj.movies.add(movie_obj)

    def test_api_jwt(self):
        token_gen_url = reverse('register_user')
        client = APIClient()
        resp = client.post(
            token_gen_url, {'username': "dummy_user",
                            'password': "dummy_pass"}, format='json')

        '''
        testing jwt_auth when user registers. Checking whether it generates a token
        upon user registration
        '''

        self.assertTrue("access_token" in resp.json())
        user_access_token = resp.json()["access_token"]
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        client.credentials(
            HTTP_AUTHORIZATION=f'Bearer gibberishstring')

        api_service = reverse('get_movies')
        resp = client.get(api_service, data={'format': 'json'})

        '''
        testing when user sends an invalid jwt token
        '''
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        '''
        testing when user sends a valid jwt token
        '''
        client.credentials(
            HTTP_AUTHORIZATION='Bearer '+user_access_token)

        resp = client.get(api_service, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_list_collections(self):
        list_url = reverse('collection-list')
        resp = self.client.get(
            list_url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_collection(self):
        get_url = reverse('collection-detail',
                          kwargs={'pk': str(self.collection_obj.uuid)})
        resp = self.client.get(
            get_url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_collection_failed(self):
        get_url = reverse('collection-detail',
                          kwargs={'pk': str(self.collection_obj.uuid)})
        resp = self.client.get(
            get_url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_collection_failed(self):
        get_url = reverse('collection-detail',
                          kwargs={'pk': "eac299d0-6d4f-4a27-8bbd-3fefc2ba6571"})
        resp = self.client.get(
            get_url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_collection(self):
        create_url = reverse('collection-list')
        request_payload = {
            "title": "MY collection 2",
            "description": "Collection Desc",
            "movies": [
                {
                    "title": "The Morning After",
                    "description": "The Morning After is a feature film that consists of 8 vignettes that are inter-cut throughout the film. The 8 vignettes are about when you wake up next to someone the next morning...",
                    "genres": [{"genre_name": "Comedy"}, {"genre_name": "Drama"}],
                    "uuid": "9a4fcb67-24f6-4cda-8f49-ad66b689f481"
                },
                {
                    "title": "Maa",
                    "description": "The bliss of a biology teacher’s family life in Delhi is shattered when her daughter, Arya  is physically assaulted by Jagan and gang. Does Devki Sabarwal wait for the law to take its course? Or does Devki become Maa Durga and hunt down the perpetrators of the crime?",
                    "genres": [{"genre_name": "Comedy"}, {"genre_name": "Drama"}],
                    "uuid": "587a1f5b-d36a-41a3-8bf8-ea0788ebc752"
                }
            ]
        }
        resp = self.client.post(
            create_url, request_payload,
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_post_collection_failed(self):
        create_url = reverse('collection-list')

        '''
        BAD Request Payload
        '''
        request_payload = {
            "title": "MY collection 2",
            "description": "Collection Desc",
        }
        resp = self.client.post(
            create_url, request_payload,
            format='json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_collection(self):
        update_url = reverse(
            'collection-detail', kwargs={'pk': str(self.collection_obj.uuid)})

        request_payload = {
            "movies": [
                {
                    "title": "The Morning After",
                    "description": "The Morning After is a feature film that consists of 8 vignettes that are inter-cut throughout the film. The 8 vignettes are about when you wake up next to someone the next morning...",
                    "genres": [{"genre_name": "Comedy"}, {"genre_name": "Drama"}],
                    "uuid": "9a4fcb67-24f6-4cda-8f49-ad66b689f675"
                },
                {
                    "title": "Maa",
                    "description": "The bliss of a biology teacher’s family life in Delhi is shattered when her daughter, Arya  is physically assaulted by Jagan and gang. Does Devki Sabarwal wait for the law to take its course? Or does Devki become Maa Durga and hunt down the perpetrators of the crime?",
                    "genres": [{"genre_name": "Comedy"}, {"genre_name": "Drama"}],
                    "uuid": "587a1f5b-d36a-41a3-8bf8-ea0788ebc222"
                }
            ]
        }
        resp = self.client.put(
            update_url, request_payload,
            format='json')

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_collection(self):
        delete_url = reverse(
            'collection-detail', kwargs={'pk': str(self.collection_obj.uuid)})
        resp = self.client.delete(
            delete_url)

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

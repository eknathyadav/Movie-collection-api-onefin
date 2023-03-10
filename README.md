
# Movie Collection API

A Movie Collection API where users can create collections where they can add movies.


## Technologies

- Django
- Django Rest Framework
- PostgreSQL



## API Reference

Except the Register API, all the other APIs need authorization.

Make sure you hit the register API(http://localhost:8000/register/) to get the access token. You can use this token with the prefix (Bearer <access_token>) in the Authorization Header of the request.

### Endpoints

| Endpoint                                            | Method | Payload                                                                                                            | Description                                               |
|-----------------------------------------------------|--------|--------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| http://localhost:8000/register/                     | POST   | {"username","password}                                                                                             | To register and get the access token                      |
| http://localhost:8000/movies/?page={page_number}    | GET    |                                                          -                                                         | To get the movies list from the third  Party API          |
| http://localhost:8000/collection/                   | GET    |                                                          -                                                         | To get the list of collections with top 3 favorite genres |
| http://localhost:8000/collection/                   | POST   | { "title", "description",  "movies"[ {"title", "description", "genres", "uuid"} ] }                                | To create a collection with the list of movies to be add  |
| http://localhost:8000/collection/<collection_uuid>/ | PUT    | { "title":<optional Collection title> ,"description":<optional collection desc>, "movies":<optional movies list> } | To update an existing collection                          |
| http://localhost:8000/collection/<collection_uuid>/ | GET    |                                                          -                                                         | To fetch the details of an existing collection            |
| http://localhost:8000/collection/<collection_uuid>/ | DELETE |                                                          -                                                         | To delete an existing collection                          |
| http://localhost:8000/request-count/                | GET    |                                                          -                                                         | To get the number of requests served by the server        |
| http://localhost:8000/request-count/reset/          | POST   |                                                          -                                                         | To reset the requests count                               |

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`
`username_tp`
`password_tp`
`DB_NAME`
`DB_USER`
`DB_PASSWORD`
`DB_HOST`
`DB_PORT`



## Installation

1. Clone the project

```
  git clone https://github.com/eknathyadav/Movie-collection-api-onefin.git

```
2. Access the `Movie-collection-api-onefin` folder

3. Install all the required python packages in your virtual environment

```
  pip install -r requirements.txt
```
  
4. Run the Django Server

```
python manage.py runserver
```


## Running Tests

To run tests, run the following command

```
python manage.py test collection.api.tests
```

## Screenshots

```
http://localhost:8000/register/
```

![register](https://user-images.githubusercontent.com/48616375/215349510-b6f8293b-c1fd-4404-97f4-f0132a897680.PNG)

```
http://localhost:8000/movies/
```

![movies_third_party](https://user-images.githubusercontent.com/48616375/215349601-a2171ed3-a4f5-4089-972f-55fce180f8eb.PNG)

```
http://localhost:8000/collection/
```

![collection_list](https://user-images.githubusercontent.com/48616375/215349658-c76ae5f6-16ac-49f5-8e1d-6974a9bc9625.PNG)

![post_collection](https://user-images.githubusercontent.com/48616375/215349682-4e29db9f-f53a-4e9a-bbe6-8786988ef9ea.PNG)

![update_collection](https://user-images.githubusercontent.com/48616375/215349690-6421f150-bab9-45cc-b291-3c6dcd5afc91.PNG)

![get_collection](https://user-images.githubusercontent.com/48616375/215349709-f7199e00-21b3-4bf1-8a2a-f8f7502c6f50.PNG)

![delete_collection](https://user-images.githubusercontent.com/48616375/215349718-3913e564-42fc-494b-a813-9ef4cc91a703.PNG)

```
http://localhost:8000/request-count/
```

![image](https://user-images.githubusercontent.com/48616375/215349788-3bdf8f62-fe9d-437e-9ee8-714d97af45ab.png)

```
http://localhost:8000/request-count/reset/
```

![image](https://user-images.githubusercontent.com/48616375/215349826-210f9a94-4fa9-427c-a9e1-768c5ce02191.png)







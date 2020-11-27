## Description

This project acts as a Microservices backend stack for the FindTheActor project. It contains several services serving part of the features set of the application.

> Currently, only part of the service is implemented and is not the full solution. Please refer to the endpoints part.

## Endpoints

- GET /movie/search: Research movies (and shows) through the IMDB API based on a provided term (example: GET /movie/search?q=Ratched)
- POST /movie/<int:movieId>/prepare: Downloads 5 photos for each cast member of the provided MovieID and store them in S3

## Requirements

### Softwares

- docker
- docker-compose
- make (optional)


### Services

- Amazon S3 API Key
- Azure account with Cognitive searvices and Advanced Bing Research

## Usage

- make build-images
- docker-compose up
- Use Postman, cUrl or Insomnia (for example) to perform API calls
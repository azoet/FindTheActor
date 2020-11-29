# Python Labs Project :
   ## Find The Actor
### Introduction
Watching a serie or movie on TV, seeing this actor, and forgetting his names. Searching for hours in the deep inside of my thoughts, not finding!

Let’s say I was watching “Joséphine, Ange Gardien”, tonight at 9:35 PM, and who’s this person? (update : he’s Omar Mebrouk)

So, here comes the idea of the project!

## Main Idea :	
 1. Open the web app, take a picture of the screen with “the actor”, possibly resize it and send !
 2. Web App is getting the picture with geoloc and timestamp on it to the API server!
 3. The API is taking geoloc, and find the corresponding linear-television scheduled programs
 4. It’s taking the timestamp, find all the matching possible programs name broadcast at the same time slot at this precise location (ex. https://www.programme-television.org/series-tv  )
 5. It gets the full cast & crew people names from all these possible programs(ex. https://www.imdb.com/title/tt0172014/fullcredits?ref_=ttrel_ql_1  )	
 6. For each names, get the first 10 pictures from google image search and compare to the one provided
 7. And send back the one name with the best % of accuracy, and its corresponding last event (ex. http://www.allocine.fr/personne/fichepersonne_gen_cpersonne=575311.html 
 “OF COURSE, I saw him in H24 with Anne Parillaud!”)
 
## General approach of services :
The micro services are divided in 4 part : 
The public one : find the actor is the one that the client Access , it provides all the functions that the client need to access.  
The 3 others private: 
- IMDB service : We use the IMDB API to make 2  calls : 
     -First call : we pass a string of the movie/show name and it returns the movie/show ID. 
     -Second call: we pass the movie/show ID and it returns the list of all cast members names. 
- Image services : we use the bing API to make an images research. 
      We get All images URLs for every cast  member . 
      It contains also the face detection,the face recognition and cropped images. 
- Storage  service :  We download the images using the URLs and store them on S3
    
    
A simple diagrams shows how all services mentioned above connecting between each other :
 
 <img src="https://github.com/azoet/FindTheActor/blob/master/images/service.JPG" align="center" height="500" width="800"/>


All Microservices are divided in three layers: 
  -Main : it's the adapter. 
   -Service : the business logic , contains all the actions. 
    -Repository:  make the connection between the others services. 

<img src="https://github.com/azoet/FindTheActor/blob/master/images/services.JPG" align="center" height="500" width="800"/>
 
 ## Face recognition:
 <img src="https://github.com/azoet/FindTheActor/blob/master/images/recognition.JPG" align="center" height="500" width="800"/>
 
 ## Feeding the train :
 <img src="https://github.com/azoet/FindTheActor/blob/master/images/feeding_the_train.JPG" align="center" height="500" width="800"/>
 
 ## The Model :
 
<img src="https://github.com/azoet/FindTheActor/blob/master/images/model.JPG" align="center" height="500" width="500"/>
 
<img src="https://github.com/azoet/FindTheActor/blob/master/images/model2.JPG" align="center" height="500" width="500"/>
  
 ## Web Application:
 The Frontend uses a Flask web application. It is devided into 3 pages: 
 1- First page : provides an "Upload" field where to drop the photo. 
 2- Second page : Choose the box showing the actor face (use of MTCNN). 
 3- Third page : the result page ( use of YOLO model)  
 
<img src="https://github.com/azoet/FindTheActor/blob/master/images/output1.JPG" align="center" height="500" width="800"/>
 
 
 Then the app gives an output of the actor/actress' Name with the best accurancy. However, the app tells you two other prediction!
 
<img src="https://github.com/azoet/FindTheActor/blob/master/images/output2.JPG" align="center" height="500" width="800"/>
 
 ## Authors :
 #### DSTI Spring Cohort 2020 – Python Labs 
##### Professor : Assan Sanogo
#### Team members :
###### Barbara Martino : *Data scientist Student*
###### Bala Veeraiah Yarabikki: *Data scientist Student*
###### Amir Zoet: *Data scientist Student*
###### Nawress Mahmoudi: *Data Engineer Student*
###### Helene Huss-Magnin: *Data scientist Student*
 

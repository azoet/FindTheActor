# Find the Actor

Watching a serie or movie on TV, seeing this actor, and forgetting his name, searching for hours in the deep inside of my thoughts, not finding. I hate it.

Let’s say I was watching “Joséphine, ange gardien”, tonight, at 9:35 PM, and bim, who’s the guy? (update : he’s Omar Mebrouk)

So, here comes idea of the project :

	
 1. Open the web app, take a picture of the screen with “the guy”, possibly resize it and send !
 2. Web app is getting the picture with geoloc and timestamp on it to the API server (thanks AWS, thanks Leo)
 3. The API is taking geoloc, and find the corresponding linear-television scheduled programs
 4. It’s taking the timestamp, find all the matching possible programs name broadcast at the same time slot at this precise location (ex. https://www.programme-television.org/series-tv  )
 5. It gets the full cast & crew people names from all these possible programs(ex. https://www.imdb.com/title/tt0172014/fullcredits?ref_=ttrel_ql_1  )	
 6. For each names, get the first 10 pictures from google image search and compare to the one provided
 7. And send back the one name with the best % of accuracy, and its corresponding last event (ex. http://www.allocine.fr/personne/fichepersonne_gen_cpersonne=575311.html  “OF COURSE, I saw him in H24 with Anne Parillaud!”)

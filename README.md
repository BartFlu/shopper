Web app to store meal Recipes in an accesible and comfort way. Its goal is to make the planning of groceries shopping easier and more enjoyable. 

The main view allows user to search through stored recipes, add them to 'basket' or remove from it.
Basket view gathers chosen recipes and generate the shopping list. 
Shopping list view allows to edit the list (for example remove the items that are in stock), add notes and send the list to desired email addres. 
App is connected to ElasticSearch which is used to search recipes based on phrases in title. 
It also offers api endpoints for further development. 

Right now it is deployed localy so login is no required however I plan to deploy it to the public host for easier access. Before that the authenticaation features will be added. 

Near future plans:
Improve recipe add view to make it easier to use and more intuitive
Add authentication and tie models to users group to make it possible to use by several households
Finish tests writing

Far future plans
Crwaler that updates the prices of products in chosen stores


How to run
  With Docker:
  1. Clone the repository. Go to './shopper/Shopper' directory and run 'docker-compose build' 
  3. Run 'docker-compose up'. Once all the containers are up and running open django cli and run
     python manage.py makemigrations
     python manage.py migrate
     python manage.py search_engine --rebuild - Note. This command often cause error when running in docker-compose. However program can run without it until I find the cause.  
     python manage.py runscript add_tags_and_categories

     
  5. App is running at http://localhost:8000
  
  Warning: app is not configured for production use and should not be use in that way. 
  Note: File with email credentials is for obvious reason not a part of this repo. It should be added manualy with one's credentials. 
  

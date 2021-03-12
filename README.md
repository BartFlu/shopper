How to run
  With Docker:
  1. Clone the repository. Go to './shopper/Shopper' directory and run 'docker-compose build' 
  2. Since it takes Postgress some time to initialize I recomend to run 'docker-compose up db' and, once the first run is finished, shut it down. 
  3. Run 'docker-compose up'. Once all the containers are up and running open django cli and run 'python manage.py migrate'
  4. App is running at http://localhost:8000
  
  Warning: app is not configured for production use and should not be use in that way. 
  Note: File with email credentials is for obvious reason not a part of this repo. It should be added manualy with one's credentials. 
  

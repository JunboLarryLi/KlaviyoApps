## KlayvioApp:  Weather Powered Email

---------
### Installation Guide:
-----------
1. clone/download this repository to your local

2. ```cd KlaviyoApps/``` and install all required packages
   ```
   $ pip install -r requirements.txt
   ```
3. install MySQL (preferred the UI development app MySQL Workbench as well).
  Download MySQL Workbench at: [MySQ\-Workbench](https://dev.mysql.com/downloads/workbench/)

4. migrate and create database schema
   ```
   # python manage.py migrate
   ```
4. run our app on server
   ```
   $ python manage.py runserver
   ```
5. now try to open your browser and type in `http://localhost:8000/weatherApp/`, put a few emails with different locations, and click subscribe. Meanwhile open up your MySQL database management system, or Workbench. You should be able to see the info you just entered from your database.

6. now you can test the `sendEmails` command. Each of the email address you just entered should receive an customized email based on the location associated with that email.
   ```
   $ python manage.py sendEmails
   ```

7. (**Extra**) Above steps seem to much? No worries! I also hosted on Heroku. Click this link:
  [https://klaviyo-weather-powered-email.herokuapp.com/](https://klaviyo-weather-powered-email.herokuapp.com/).

8. (**Extra**) Want to peak inside and modify the subscribers? Simply setup a new connection with that remote database! Here are the credentials (Message me and I'll give you the passcode):
  ```
    CONNECTION NAME:  heroku_112c84ebeeb128b
    HOST NAME: us-cdbr-iron-east-05.cleardb.net
    USER NAME: b51dc2bd6e1c12  
  ```

---------
#### Functionalities
---------
At this stage, the app can mainly support the following two basic functions.

1. User is able to enter their email address and choose their location from a list of the top 100 cities in the US by population.

    * Email format sanity check
    * Duplicated email address check


2. Customized emails
    *  Created a Django management command ```$ python manage.py sendEmails``` to send customized emails.

    * Fetch the current weather for that recipient's location, and change the subject of the email based on the weather.

    * Customized the body of the email as required. Included an image of the current weather. (**Extra**)

See [here](https://www.klaviyo.com/weather-app) for more details of the app design requirments. Of course, more features will come!


-----------
#### Methods/Tech Stack
-----------
Technologies used are
1. Backend
    * Django
    * MySQL
2. Frontend
    * HTML, CSS
4. Third-party API
    * WounderGround
    * SendGrid
4. Hosting
    * Localhost
    * Heroku


-------
#### Results
-------

**[Klayvio Weather](https://demo-klayvio-weather.herokuapp.com/)**


![alt text](/weatherApp/static/puppy.jpg "Logo Title Text 1")




#### Future works
Quite a few improvements can be made
1. rabbitMQ + celery to queue up the task
2. better templatize the email building

I would love the chance to go into more detail to discuss

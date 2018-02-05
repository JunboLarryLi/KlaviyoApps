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

4. assume we are going to work on local first. Go to `/klaviyo/settings.py` and comment out line 112 - 121. Meanwhile, get rid of the comments from line 98 - 107. The purpose behind is to switch back to local database settings.

5. migrate and create database schema
   ```
   $ python manage.py migrate
   ```
6. run our app on server
   ```
   $ python manage.py runserver
   ```
7. now try to open your browser and type in `http://localhost:8000/weatherApp/`, put a few emails with different locations, and click subscribe. Meanwhile open up your MySQL database management system, or Workbench. You should be able to see the info you just entered from your database.

8. now you can test the `sendEmails` command. Each of the email address you just entered should receive an customized email based on the location associated with that email.
   ```
   $ python manage.py sendEmails
   ```

9. (**Extra**) Above steps seem to much? No worries! I also hosted on Heroku. Click this link:
  [https://klaviyo-weather-powered-email.herokuapp.com/](https://klaviyo-weather-powered-email.herokuapp.com/).

10. (**Extra**) Want to peak inside and modify the subscribers? Simply setup a new connection with that remote database! Here are the credentials (Message me and I'll give you the passcode):
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

**[Klayvio Weather Powered App (hosted on Heroku)](https://klaviyo-weather-powered-email.herokuapp.com/)**

**Subscribe page**:
![alt text](/static/demo_img/demo_subsribe_page.png "subscribe page")

**Successfully subscribed page**:
![alt text](/static/demo_img/demo_success.png "Successfully subscribed")

**Duplicated email address page**:
![alt text](/static/demo_img/demo_duplicate_email_addr.png "Duplicated email address"
)

**Invalid email address page**:
![alt text](/static/demo_img/demo_invalid_addr.png "Invalid email address"
)

**Email template: Sunny**:
![alt text](/static/demo_img/demo_sunny_email.png "Email template: Sunny"
)

**Email template: Rainy**:
![alt text](/static/demo_img/demo_rainy_email.png "Email template: Rainy"
)

#### Future works
1. Add admin page. In this way, the administrator can easily modify the subscribers without digging into MySQL database.

2. Adopt a more scientific way to calculate the average weather for a particular location through history.

3. Add more features.

## Please feel free to contact me. I would love to walk through my design and code.

# AutoLog

AutoLog is a parts manager for Car enthusiasts. The site will keep a record of all car parts with the benefit of giving a total price as well as giving other the chance to vote on users builds.

You can view the project [here on Heroku.](http://autolog-msped.herokuapp.com/)

## UX

- A user will want to be able to 'Create a build' to see pricing on future projects.

- A user will wish to read previous 'Builds' that have been created.

- A user will want the functionality to see the total of all the parts added to 'Build'.

- A user will want to update a 'Build' should a link to an external website become inactive or find a different part they wish to buy in the future.

- Each user will be able to create builds and either have them public on the builds page for other users to see or keep them private to be seen only on the my builds page.

- Users will wish to delete 'Builds' previously created.

## Database Design

Design of database can be view [here](https://github.com/msped/AutoLog/blob/master/assets/Autolog%20ERD.png).

## Features

### Existing Features

This is a web application that providers users with a place to plan new car builds. The application provide create, read, update and delete (CRUD) functionality for each Build.

- The builds page gives an overview of the builds that all user have created with the visibility of Public as well as the option to sort the builds on the amount of likes and the price.

- On clicking the view button it will take you to a page where the user can view the build (Read).

- When logged in on the My Builds page and clicking on the users own builds, 'Edit' will appear at the bottom.

- By clicking on the top right of the website, or on the hamburger if on mobile, the user can select 'Create a Build' in-order to create a new build. Create a build will allow users to input the products name, a link to a webpage where the product can be purchased (The input box will give a green or red outline depending on whether the link is valid or not.) as well as the price of the product.
  - When creating a new build the user will be able to add any parts they wish from the dropdown provided and populate the fields that appear with the information required by the site (Create). Any of this information can be edited in the future as described previously.

- On the view page users will be able to vote on other peoples builds.

- Users are not be able to edit other users build and if they attempt to access via the address bar (build/<build_id>/edit) they will be redirected to the builds page with a visible error message.

### Features left to implement

- An option to say whether the item has been brought or not so it can be removed from the running total.

- API in-order to populate the car fields (make, model, trim, year).

## Technologies Used

Below are the libraries and languages used in creating this project.

- [HTML5](https://en.wikipedia.org/wiki/HTML5)

- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS33)

- [JavaScript](https://www.javascript.com/)

- [jQuery](https://jquery.com/)

- [Font Awesome](https://fontawesome.com)

- [Flask](https://flask.palletsprojects.com/en/1.0.x/)
  - [Flask-Login](https://flask-login.readthedocs.io/en/latest/)

- [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)

- [PyMongo](https://api.mongodb.com/python/current/)

## Testing

Auotmated testing can be found in testing.py. It can be ran with `python testing.py` in the appropriate directory on the command line.

CSS and JS passed through Jigsaw & JShint without any errors.

The site was manually tested for an errors with the HTML and CSS. All pages worked as expected, making use of the space of each screen size, the only issue found is outlined below.

### Bugs to be fixed

The only minor bug to be fixed is on the create and edit pages where the use of the tables make for very short input boxes. A fixed to move them onto another line with smaller screen sizes.

## Deployment

This application was deloyed using Heroku. It can be view [here.](http://autolog-msped.herokuapp.com/)

For this application to be deployed it first requires two files, requirements.txt and a Procfile.

Requirements.txt can be created using `pip freeze > requirements.txt` in the command line. The Procfile can be added by typing `echo web: python app.py > Procfile` into the command line.

With both of these file create a new app on [Heroku](https://dashboard.heroku.com/login). Download the Heroku CLI toolbelt and login to Heroku via the command line. Then in the command line type git init, git add ., git commit, git push heroku master. Finally initalise the app on the Heroku server by typing `heroku ps:scale web=1` and press enter.

Now in the Heroku Settings add the CONFIG VARS IP (0.0.0.0), PORT (5000), MONGO_DBNAME, MONGO_URI and SECERT_KEY.

### Local Deployment

To run the site locally, install venv with `pip install venv` and run `python -m venv (path to the env)`. Move to this directory and clone the git repository using `git clone https://github.com/msped/AutoLog.git`, install the packages / dependancies from the requirements.txt using `pip install -r requirements.txt`.

In order for the application to work it will need some environment variables, these and either be stored in your systems environment variables, or create a .env file and add a MONGO_URI, MONGO_DBNAME and a SECERT_KEY

To run the application, open up a terminal and move into the directory where 'app.py' is located. Once there run `python app.py`, this will start the application where it will run on the link shown in the terminal when the server starts.

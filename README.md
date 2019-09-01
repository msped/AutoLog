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
- On clicking the view button it will take you to a page where the user can view the build (Read)
- When logged in on the My Builds page and clicking on the users own builds, 'Edit' will appear at the bottom.
- By clicking on the top right of the website, or on the hamburger if on mobile, the user can select 'Create a Build' in-order to create a new build.
  - When creating a new build the user will be able to add any parts they wish from the dropdown provided and populate the fields that appear with the information required by the site (Create). Any of this information can be edited in the future as described previously.
- On the view page users will be able to vote on other peoples builds.

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

## Deployment

This application was deloyed using Heroku. It can be view [here.](http://autolog-msped.herokuapp.com/)

For this application to be deployed it first requires two files, requirements.txt and a Procfile.

Requirements.txt can be created using `pip freeze > requirements.txt` in the command line. The Procfile can be added by typing `echo web: python app.py > Procfile` into the command line.

With both of these file create a new app on [Heroku](https://dashboard.heroku.com/login). Download the Heroku CLI toolbelt and login to Heroku via the command line. Then in the command line type git init, git add ., git commit, git push heroku master. Finally initalise the app on the Heroku server by typing `heroku ps:scale web=1` and press enter.

Now in the Heroku Settings add the CONFIG VARS IP (0.0.0.0), PORT (5000), MONGO_DBNAME and MONGO_URI.

### Local Deployment

To run the site locally, first download the .zip from GitHub and extract it.

In app.py change:

```python
    if __name__ == '__main__':
        app.run(host=os.environ.get('IP'),
                port=int(os.environ.get('PORT')),
                debug=False)
```

to

```python
    if __name__ == '__main__':
        app.run(debug=False)
```

This will ensure that the project runs diectly on 127.0.0.0:5000, or if you have specified an IP and PORT on your local systems environment variables already you can use the preivous option.

In order for the application to work it will need some environment variables, these and either be stored in your systems environment variables, or by install flask-dotenv with `pip intsall flask-dotenv` and added `from flask-dotenv import DotEnv` and `env = DotEnv(app) env.initapp(app)` to app.py. Lastly a .env file will need to be created with the environment variables you wish to use in.

To run the application, open up a terminal and move into the directory where 'app.py' is located. Once there run `python app.py`, this will start the application where it will run on the link shown in the terminal when the server starts.

## Credits

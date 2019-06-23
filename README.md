## Airtech-API


## Description

The **Airtech-API** is the backbone of a flight booking application where 
users can make flight reservations and buy flight tickets.

The API documentation can be found here: 
[Doc](https://documenter.getpostman.com/view/5828093/S1a1bUm1?version=latest)

Staging Link: N/A


## Key Application features

1. Register and login users.
2. Be a vendor and sell wears.
3. Users can upload passport photographs.
4. Users can book tickets.
5. Users can receive tickets as an email.
5. Users can check the status of their flight.
6. Users can make flight reservations.
7. Users can purchase tickets.


# Table of Contents

- [Getting Started](#getting-started)
- [Technologies](#technologies)
- [Installation and Usage](#Setting-up-for-development)
- [Testing](#Running-tests-and-generating-report)
- [License](#license)

## Getting Started

This is a python API built with [**Django v2.2**](https://docs.djangoproject.com) and [**Django Rest Framework**](https://www.django-rest-framework.org) framework. Authentication of users is done via [**JSON Web Tokens**](https://jwt.io/).

## Technologies

- `Python 3.7.0`

- [**Django v2.2**](https://docs.djangoproject.com)

- [**Django Rest Framework**](https://www.django-rest-framework.org) 

- [**PostgreSQL**](https://www.postgresql.org/)


### Setting up for development

```
NOTE: This setup is for MacOS only, Windows setup will be coming soon.
```

-   Check that python 3 is installed:

    ```bash
    python --v
    >> Python 3.7
    ```


-   Install pipenv:

    ```bash
    brew install pipenv
    ```

-   Check pipenv is installed:
    ```bash
    pipenv --version
    >> pipenv, version 2018.11.26
    ```
-   Check that postgres is installed:

    ```bash
    postgres --version
    >> postgres (PostgreSQL) 10.5
    ```

-   Clone the Airtech-API repo and cd into it:

    ```bash
    git clone https://github.com/veeqtor/Airtech-API.git
    ```

-   Install dependencies:

    ```
    pipenv install
    ```

-   Install dev dependencies to setup development environment:

    ```bash
    pipenv install --dev
    ```

-   Rename the .env.sample file to .env and update the variables accordingly:

-   Activate a virtual environment:

    ```bash
    pipenv shell
    ```

-   Apply migrations and create a superuser:

    ```bash
    python manage.py migrate  && python manage.py createsuperuser
    ```

-   Run the application:

    ```bash
    python manage.py runserver
    ```


-   Should you make changes to the database models, run migrations as follows:

    ```bash
    python manage.py makemigrations && python manage.py migrate
    ```


-   Deactivate the virtual environment once you're done:
    ```bash
    exit
    ```
    

##  Running tests and generating report

   On command line run: 
   
   ```bash
   pytest
   ```

   To further view the lines not tested or covered if there is any, 

   An `htmlcov` directory will be created, get the `index.html` file by entering the directory and view it in your browser.


## Contribution guide

##### Contributing

All proposals for contribution must satisfy the guidelines in the product wiki.
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.This Project shall be utilising a [Pivotal Tracker board](https://www.pivotaltracker.com/n/projects/2355429) to track the work done.

## License

This project is authored by **Nwokeocha victor** and is licensed for your use, modification and distribution under the **MIT** license.

# New York Food Bank Backend

Demo: https://nyfoodbank.herokuapp.com/allpantries<br/>
Frontend: https://github.com/yuyingsu/NewYorkFoodBank

## Stack

<ul>
  <li>React</li>
  <li>Redux</li>
  <li>Flask</li>
  <li>SQLite</li>
  <li>Bootstrap</li>
</ul>

## Features

<ul>
  <li>Geolocation on Google Maps</li>
  <li>Mapping U.S. Census Data on Mapbox</li>
  <li>Donation System</li>
  <li>Organization Management</li>
  <li>Pantry Management</li>
</ul>

## User Stories

<ul>
  <li>As a user, I can register</li>
  <li>As a user, I can make a donation</li>
  <li>As a user, I can add/edit/remove/read an organization</li>
  <li>As a user, I can add/edit/remove/read a pantry</li>
</ul>

## Installation

### Run Backend

```
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install -r requirements.txt
$ flask db init
$ flask db migrate -m "1st Migration"
$ flask db upgrade
$ flask run
```

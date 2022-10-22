# NEECT RALLY-TASCAS API
API that handles data to and from neect rally-tascas' databases

## API Documentation

### Rally Tascas

1. [Teams](#teams)
    1. [Structure](#teams-structure)
    1. [Add Team](#add-team)
    1. [Get Team](#get-team)
    1. [Delete Team](#delete-team)
    1. [Update Team](#update-team)
1. [Members](#members)
    1. [Structure](#members-structure)
    1. [Add Member](#add-member)
    1. [Get Member](#get-member)
    1. [Delete Member](#delete-member)
    1. [Update Member](#update-member)
1. [Bars](#bars)
    1. [Structure](#bars-structure)
    1. [Add Bar](#add-bar)
    1. [Get Bar](#get-bar)
    1. [Delete Bar](#delete-bar)
    1. [Update Bar](#update-bar)
1. [Games](#games)
    1. [Structure](#games-structure)
    1. [Add Game](#add-game)
    1. [Get Game](#get-game)
    1. [Delete Game](#delete-game)
    1. [Update Game](#update-game)
1. [Prizes](#prizes)
    1. [Structure](#prizes-structure)
    1. [Add Prize](#add-prize)
    1. [Get Prize](#get-prize)
    1. [Delete Prize](#delete-prize)
    1. [Update Prize](#update-prize)
1. [QR Codes](#qr-codes)
    1. [Generate QR Code](#generate-qr-code)
    1. [Get QR Code](#get-qr-code)
    1. [Delete QR Code](#delete-qr-code)

### Administration    

1. [Admin](#admin)
    1. [Create Admin Account](#create-admin-account)
    1. [Get Admin Token](#get-admin-token)

## Teams

Teams that compete against each other in the bar hopping event.

***[POST, GET, DELETE, PATCH]***

### Teams Structure

Example of the information fetched from **/teams**:
```json5
{
    "id": 1,
    "name": "Crocodiles",
    "email": "example@example.com",
    "points": 45,
    "drinks": 3,
    "qr_code": "http://127.0.0.1:8000/qrcodes/qr_team1.png",
    "has_egg": true,
    "puked": 2,
    "members": [
        ...
    ],
    "bars": [
        {
            "id": 1,
            "bar": {
                ...
            },
            "points": 30,
            "drinks": 2,
            "has_egg": true,
            "puked": 1,
            "visited": true,
            "won_game": true
        },
        ...
    ]
}
```

#### **Fields**
| ID | Name | Data Type | Default | Description |
|----|------|-----------|:-------:| ----------- |
| **id** | Team ID | integer | *[auto gen]* | Team number identifier | 
| **name** | Name | string | ✖ | Team name | 
| **email** | Email | string | ✖ | Team email |
| **points** | Points | integer | 0 | Total number of points won |
| **drinks** | Drinks | integer | 0 | Total number of drinks |
| **qr_code** | QR Code | string | *[auto gen]* | URL to the team's QR Code image |
| **has_egg** | Has Egg | boolean | true | Whether or not the team still has the egg (unbroken) |
| **puked** | Puked | integer | 0 | Total number of times the team members have puked |
| **members** | Team Members | list<[Member](#Members)> | ✖ | List of members in the team |
| **[bars](#Fields-team-bars)** | Bars | list<{..., [Bar](#Bars)}> | *[auto gen]* | Team stats on each bar |

#### **Fields [team-bars]**
| ID | Name | Data Type | Description |
|----|------|-----------|-------------|
| **id** | Bar ID | integer | Bar number identifier | 
| **bar** | Bar | [Bar](#Bars) | Bar data | 
| **points** | Team Points | integer | Total number of points won on this bar |
| **drinks** | Team Drinks | integer | Total number of drinks on this bar |
| **has_egg** | Has Egg | boolean | Whether or not the team still had the egg on this bar |
| **puked** | Puked | integer | Total number of times the team members have puked on this bar |
| **visited** | Visited | boolean | Whether or not the team has already visited this bar |
| **won_game** | Won Game | boolean | Whether or not the team has won the game on this bar |

### Add Team

Add a new team to the database.

**HTTP Request**

``` POST .../api/teams```

**Request Body**
```json5
{
    "name": "Crocodiles",
    "email": "example@example.com",
    "members": [
        {
            "name": "John Doe",
            "nmec": 12345,
            "course": "Computadores e Telemática"
        },
        ...
    ]
}
```

#### **Fields**
| ID | Mandatory | Data Type |
|----|:---------:|-----------|
| **name** | ✔ | string |
| **email** | ✔ | string |
| **members** | ✔ | list<[Member](#Members)> |

### Get Team

Get teams from the database.  
If no team ID is specified, all teams are returned. 

**HTTP Request**

``` GET .../api/teams```
``` GET .../api/teams/{team_id}```

**Response Body**

See [Structure](#teams-structure)

### Delete Team

Delete a team from the database.  
Must specify the team ID.

**HTTP Request**

``` DELETE .../api/teams/{team_id}```

### Update Team

Update a team's information.  
Provide the team ID and the fields to be updated.  
Unspecified fields will be left unchanged.  
Updatable fields are: ***name, email, points, drinks, has_egg, puked***

**HTTP Request**

``` PATCH .../api/teams/{team_id}```

## Members

Members that are part of a team

***[POST, GET, DELETE, PATCH]***

### Members Structure

Example of the information fetched from **/members**:
```json5
{
    "id": 1,
    "name": "John Doe",
    "nmec": 12345,
    "course": "Computadores e Telemática",
    "points": 15,
    "drinks": 1,
    "team": {
        ...
    },
    "bars": {
        "id": 1,
        "bar": {
            ...
        },
        "points": 15,
        "drinks": 1
    }
}
```

#### **Fields**
| ID | Name | Data Type | Default | Description |
|----|------|-----------|:-------:| ----------- |
| **id** | Member ID | integer | *[auto gen]* | Member number identifier |
| **name** | Name | string | ✖ | Member name |
| **nmec** | NMEC | integer | ✖ | Member NMEC |
| **course** | Course | string | ✖ | Member course |
| **points** | Points | integer | 0 | Total number of points won |
| **drinks** | Drinks | integer | 0 | Total number of drinks |
| **team** | Team | [Team](#Teams) | ✖ | Data from the member's team |
| **[bars](#Fields-member-bars)** | Bars | list<{..., [Bar](#Bars)}> | *[auto gen]* | Member stats on each bar |

#### **Fields [member-bars]**
| ID | Name | Data Type | Description |
|----|------|-----------|-------------|
| **id** | Bar ID | integer | Bar number identifier |
| **bar** | Bar | [Bar](#Bars) | Bar data |
| **points** | Member Points | integer | Total number of points won on this bar |
| **drinks** | Member Drinks | integer | Total number of drinks on this bar |

### Add Member

Add a new member to the database.

**HTTP Request**

``` POST .../api/members```

**Request Body**
```json5
{
    "name": "John Doe",
    "nmec": 12345,
    "course": "Computadores e Telemática",
    "team": 1
}
```

#### **Fields**
| ID | Mandatory | Data Type |
|----|:---------:|-----------|
| **name** | ✔ | string |
| **nmec** | ✔ | integer |
| **course** | ✔ | string |
| **team** | ✔ | integer |

### Get Member

Get members from the database. 
If no member ID is specified, all members are returned.

**HTTP Request**

``` GET .../api/members```
``` GET .../api/members/{member_id}```

**Response Body**

See [Structure](#members-structure)

### Delete Member

Delete a member from the database.
Must specify the member ID.

**HTTP Request**

``` DELETE .../api/members/{member_id}```

### Update Member

Update a member's information.  
Provide the member ID and the fields to be updated.  
Unspecified fields will be left unchanged.  
Updatable fields are: ***name, nmec, course, team, points, drinks***

**HTTP Request**

``` PATCH .../api/members/{member_id}```

## Bars

Bars that are part of the bar hopping course.

***[POST, GET, DELETE, PATCH]***

### Bars Structure

Example of the information fetched from **/bars**:
```json5
{
    "id": 1,
    "name": "Bar 1",
    "address": "Rua 1",
    "latitude": 38.736946,
    "longitude": -9.142685,
    "picture": "http://127.0.0.1/bar1.jpg",
    "points": 45,
    "drinks": 3,
    "puked": 1,
    "visited": 2,
    "game": {
        ...
    }
}
```

#### **Fields**
| ID | Name | Data Type | Default | Description |
|----|------|-----------|:-------:| ----------- |
| **id** | Bar ID | integer | *[auto gen]* | Bar number identifier |
| **name** | Name | string | ✖ | Bar name |
| **address** | Address | string | ✖ | Bar address |
| **latitude** | Latitude | double | ✖ | Bar latitude |
| **longitude** | Longitude | double | ✖ | Bar longitude |
| **picture** | Picture | string | *[null]* | Bar picture |
| **points** | Points | integer | 0 | Total number of points won in the bar |
| **drinks** | Drinks | integer | 0 | Total number of drinks in the bar |
| **puked** | Puked | integer | 0 | Total number of puked drinks in the bar |
| **visited** | Visited | integer | 0 | Total number of visits to the bar |
| **game** | Game | [Game](#Games) | *[null]* | Data from the bar's game |

### Add Bar

Add a new bar to the database.

**HTTP Request**

``` POST .../api/bars```

**Request Body**
```json5
{
    "name": "Bar 1",
    "address": "Rua 1",
    "latitude": 38.736946,
    "longitude": -9.142685,
    "picture": "http://127.0.0.1/bar1.jpg",
    "game": 1
}
```

#### **Fields**
| ID | Mandatory | Data Type |
|----|:---------:|-----------|
| **name** | ✔ | string |
| **address** | ✔ | string |
| **latitude** | ✔ | double |
| **longitude** | ✔ | double |
| **picture** | ✖ | string |
| **game** | ✖ | integer |

### Get Bar

Get bars from the database.  
If no bar ID is specified, all bars are returned.

**HTTP Request**

``` GET .../api/bars```
``` GET .../api/bars/{bar_id}```

**Response Body**

See [Structure](#bars-structure)

### Delete Bar

Delete a bar from the database.  
Must specify the bar ID.

**HTTP Request**

``` DELETE .../api/bars/{bar_id}```

### Update Bar

Update a bar's information.
Provide the bar ID and the fields to be updated.
Unspecified fields will be left unchanged.
Updatable fields are: ***name, address, latitude, longitude, picture, points, drinks, puked, visited, game***

**HTTP Request**

``` PATCH .../api/bars/{bar_id}```

## Games

Games that are played in each bar

***[POST, GET, DELETE, PATCH]***

### Games Structure

Example of the information fetched from **/games**:
```json5
{
    "id": 1,
    "name": "Game 1",
    "description": "Game 1 description",
    "points": 10,
    "completed": 2,
}
```

#### **Fields**
| ID | Name | Data Type | Default | Description |
|----|------|-----------|:-------:| ----------- |
| **id** | Game ID | integer | *[auto gen]* | Game number identifier |
| **name** | Name | string | ✖ | Game name |
| **description** | Description | string | *[None]* | Game description |
| **points** | Points | integer | ✖ | Total number of points a team can win by completing the game |
| **completed** | Completed | integer | 0 | Total number of times the game has been completed |

### Add Game

Add a new game to the database.

**HTTP Request**

``` POST .../api/games```

**Request Body**
```json5
{
    "name": "Game 1",
    "description": "Game 1 description",
    "points": 10
}
```

#### **Fields**
| ID | Mandatory | Data Type |
|----|:---------:|-----------|
| **name** | ✔ | string |
| **description** | ✖ | string |
| **points** | ✔ | integer |

### Get Game

Get games from the database.  
If no game ID is specified, all games are returned.

**HTTP Request**

``` GET .../api/games```
``` GET .../api/games/{game_id}```

**Response Body**

See [Structure](#games-structure)

### Delete Game

Delete a game from the database.  
Must specify the game ID.

**HTTP Request**

``` DELETE .../api/games/{game_id}```

### Update Game

Update a game's information.
Provide the game ID and the fields to be updated.
Unspecified fields will be left unchanged.
Updatable fields are: ***name, description, points, completed***

**HTTP Request**

``` PATCH .../api/games/{game_id}```

## Prizes

Prizes for the best teams.  
A scoreboard position for the prize to be awarded must be specified.

***[POST, GET, DELETE, PATCH]***

### Prizes Structure

Example of the information fetched from **/prizes**:
```json5
{
    "id": 1,
    "name": "Prize 1",
    "place": 1,
    "ammount": 2,
    "winner": 4
}
```

#### **Fields**
| ID | Name | Data Type | Default | Description |
|----|------|-----------|:-------:| ----------- |
| **id** | Prize ID | integer | *[auto gen]* | Prize number identifier |
| **name** | Name | string | ✖ | Prize name |
| **place** | Place | integer | ✖ | Scoreboard position where the prize is awarded |
| **ammount** | Ammount | integer | ✖ | Number of prize items awarded to the winning team |
| **winner** | Winning team | [Team](#teams) | *[null]* | Team that won the prize |

### Add Prize

Add a new prize to the database.

**HTTP Request**

``` POST .../api/prizes```

**Request Body**
```json5
{
    "name": "Prize 1",
    "place": 1,
    "ammount": 2
}
```

#### **Fields**

| ID | Mandatory | Data Type |
|----|:---------:|-----------|
| **name** | ✔ | string |
| **place** | ✔ | integer |
| **ammount** | ✔ | integer |

### Get Prize

Get prizes from the database.  
If no prize ID is specified, all prizes are returned.

**HTTP Request**

``` GET .../api/prizes```
``` GET .../api/prizes/{prize_id}```

**Response Body**

See [Structure](#prizes-structure)

### Delete Prize

Delete a prize from the database.  
Must specify the prize ID.

**HTTP Request**

``` DELETE .../api/prizes/{prize_id}```

### Update Prize

Update a prize's information.
Provide the prize ID and the fields to be updated.
Unspecified fields will be left unchanged.
Updatable fields are: ***name, place, ammount, winner***

**HTTP Request**

``` PATCH .../api/prizes/{prize_id}```

## QR Codes

Each team has a QR code that can be scanned to add points to the team's score.  
The QR code is generated automatically when a team is created and its png is saved in ***/static/qrcodes/***.  
Only authorized accounts can scan the QR code successfully.  

***[POST, GET, DELETE]***

### Generate QR Code

Generate a QR code for a team.
This is only used when, for some reason, the qr code image is lost or deleted.

**HTTP Request**

``` POST .../api/qrcodes/{team_id}```

### Get QR Code

Get the url for a QR code image from the database.
Must specify the team ID.

**HTTP Request**

``` GET .../api/qrcodes/{team_id}```

**Response Body**

```json5
{
    "qrcode": "http://127.0.0.1:8000/static/qrcodes/1.png"
}
```

#### Fields
| ID | Data Type |
|----|-----------|
| **qrcode** | string |

### Delete QR Code

Delete a QR code from the database.
Must specify the team ID.

**HTTP Request**

``` DELETE .../api/qrcodes/{team_id}```

## Create Admin Account

Create an admin account to manage teams, members, bars, games and prizes.
Must be superuser to use.

**HTTP Request**

``` POST .../api/register```

**Request Body**
```json5
{
    "username": "admin",
    "password": "admin"
}
```

#### **Fields**
| ID | Mandatory | Data Type |
|----|:---------:|-----------|
| **username** | ✔ | string |
| **password** | ✔ | string |

## Get Admin Token

Get an admin token to use in the Authorization header of requests.

**HTTP Request**

``` POST .../api/token```

**Request Body**
```json5
{
    "username": "admin",
    "password": "admin"
}
```

#### **Fields**
| ID | Mandatory | Data Type |
|----|:---------:|-----------|
| **username** | ✔ | string |
| **password** | ✔ | string |


**Response Body**
```json5
{
    "token": "<random_value>"
}
```

#### **Fields**
| ID | Data Type |
|----|-----------|
| **token** | string |
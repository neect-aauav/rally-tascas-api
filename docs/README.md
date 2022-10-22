# NEECT RALLY-TASCAS API
API that handles data to and from neect rally-tascas' databases

## API Documentation

1. [Teams](#teams)
    1. [Structure](#teams-structure)
    1. [Add Team](#add-team)
    1. [Get Team](#get-team)
    1. [Delete Team](#delete-team)
    1. [Update Team](#update-team)

## Teams

Teams that compete against each other in the bar hopping event

*[POST, GET, DELETE, PATCH]*

### Teams Structure

Example of the information fetched from **/teams**:
```json
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
|----|------|-----------|---------| ----------- |
| **id** | Team ID | number | *[auto gen]* | Team number identifier | 
| **name** | Name | string | ❌ | Team name | 
| **email** | Email | string | ❌ | Team email |
| **points** | Points | number | 0 | Total number of points won |
| **drinks** | Drinks | number | 0 | Total number of drinks |
| **qr_code** | QR Code | string | *[auto gen]* | URL to the team's QR Code image |
| **has_egg** | Has Egg | boolean | true | Whether or not the team still has the egg (unbroken) |
| **puked** | Puked | number | 0 | Total number of times the team members have puked |
| **members** | Team Members | list<[Member](#Members)> | ❌ | List of members in the team |
| **[bars](#Fields-[bars])** | Bars | list<{..., [Bar](#Bars)}> | *[auto gen]* | Team stats on each bar |

#### **Fields [bars]**
| ID | Name | Data Type | Description |
|----|------|-----------|-------------|
| **id** | Bar ID | number | Bar number identifier | 
| **bar** | Bar | [Bar](#Bars) | Bar data | 
| **points** | Team Points | number | Total number of points won on this bar |
| **drinks** | Team Drinks | number | Total number of drinks on this bar |
| **has_egg** | Has Egg | boolean | Whether or not the team still had the egg on this bar |
| **puked** | Puked | number | Total number of times the team members have puked on this bar |
| **visited** | Visited | boolean | Whether or not the team has already visited this bar |
| **won_game** | Won Game | boolean | Whether or not the team has won the game on this bar |

### Add Team

Add a new team to the database

**HTTP Request**

``` POST .../api/teams```

**Request Body**
```json
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
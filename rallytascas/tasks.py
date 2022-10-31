import requests

from celery.utils.log import get_task_logger
from celery import shared_task

from api.models import Teams, Members, Bars, Games

from neectrally.celery import app

logger = get_task_logger(__name__)
logger.propagate = True

from neectrally.settings import BASE_IRI

@shared_task
def put_data(msg):
    AUTH_KEY = msg['token']
    data = msg['data']

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {AUTH_KEY}"
    }

    print("Making PATCH...")

    team = Teams.objects.get(id=data["team_id"])
    bar = Bars.objects.get(id=data["bar_id"])
    game = Games.objects.get(id=bar.game.id)
    
    # update team
    requests.patch(f"{BASE_IRI}/api/teams/{data['team_id']}", json={
        "points": team.points + data["points"],
        "drinks": team.drinks + data["drinks"],
        "has_egg": data["has_egg"],
        "puked": team.puked + data["puked"],
        "bar": {
            "id": bar.id,
            "points": data["points"],
            "drinks": data["drinks"],
            "has_egg": data["has_egg"],
            "puked": data["puked"],
            "won_game": data["game_completed"]
        }
    }, headers=headers)

    for member in data["members"]:
        member_object = Members.objects.get(id=member["id"])
        # update members
        requests.patch(f"{BASE_IRI}/api/members/{member['id']}", json={
            "points": member_object.points + member["points"],
            "drinks": member_object.drinks + member["drinks"],
            "bar": {
                "id": bar.id,
                "points": member["points"],
                "drinks": member["drinks"]
            }
        }, headers=headers)

    # update bars
    requests.patch(f"{BASE_IRI}/api/bars/{data['bar_id']}", json={
        "points": bar.points + data["points"],
        "drinks": bar.drinks + data["drinks"],
        "puked": bar.puked + data["puked"],
    }, headers=headers)

    # update games
    requests.patch(f"{BASE_IRI}/api/games/{game.id}", json={
        "completed": game.completed + 1 if data["game_completed"] else 0
    }, headers=headers)

    return True
import requests

from celery.utils.log import get_task_logger
from celery import shared_task

from api.models import Teams, Members, Bars, Games
from api.views import patch_team, patch_member, patch_bar, patch_game

from neectrally.celery import app

logger = get_task_logger(__name__)
logger.propagate = True

from neectrally.settings import BASE_IRI

@app.task
def put_data(data):
    print("Making PATCH...")

    team = Teams.objects.get(id=data["team_id"])
    bar = Bars.objects.get(id=data["bar_id"])
    game = Games.objects.get(id=bar.game.id)
    
    # update team
    patch_team({
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
    }, team.id)

    for member in data["members"]:
        member_object = Members.objects.get(id=member["id"])
        # update members
        patch_member({
            "points": member_object.points + member["points"],
            "drinks": member_object.drinks + member["drinks"],
            "bar": {
                "id": bar.id,
                "points": member["points"],
                "drinks": member["drinks"]
            }
        }, member_object.id)

    # update bars
    patch_bar({
        "points": bar.points + data["points"],
        "drinks": bar.drinks + data["drinks"],
        "puked": bar.puked + data["puked"],
    }, bar.id)

    # update games
    patch_game({
        "completed": game.completed + 1 if data["game_completed"] else 0
    }, game.id)

    return True
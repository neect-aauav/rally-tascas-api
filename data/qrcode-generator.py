import json
import random
import qrcode

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import *

FRONTEND_URL = 'https://rally-tascas.herokuapp.com'

def generate_qrcode(path, data):
    l = [RadialGradiantColorMask(), SquareGradiantColorMask(), HorizontalGradiantColorMask(), VerticalGradiantColorMask()]
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=2
    )
    qr.add_data(data)

    img = qr.make_image(image_factory=StyledPilImage, color_mask=l[random.randint(0,3)])
    img.save(path)

# import teams.json
with open('teams.json', 'r') as f:
    teams = json.load(f)

    # generate qrcode for each team
    counter = 1
    for team in teams:
        # generating print
        print(f"Generating {counter}/{len(teams)} QR Codes...", end="", flush=True)

        if counter < len(teams):
            print('\r', end='')
        else:
            print('')
        
        generate_qrcode(f"qrcodes/{team['team']}.png", FRONTEND_URL + f"/admin/equipas/{counter}")
        counter += 1
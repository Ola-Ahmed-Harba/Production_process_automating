from django.utils import timezone
from django.contrib.auth.models import  User
from howdy.models import Manger

def getTime():
    datee = timezone.localdate()
    year = datee.year
    month = datee.month
    day = datee.day
    hour = timezone.localtime().hour

    if hour > 8 and hour < 16:
        shift = "صباحية"
    else:
        shift = "مسائية"
    return year, month, day, hour, shift


def create_user():
    # content_type = ContentType.objects.get_for_model(User)
    users = [
        {'username':'coating', 'password':'lolwacode'},
        {'username':'cutting', 'password':'lolwacode'},
        {'username':'loom', 'password':'lolwacode'},
        {'username':'extruder', 'password':'lolwacode'},
        {'username':'sales', 'password':'lolwacode'},
        {'username':'quality', 'password':'lolwacode'},
        {'username':'printing', 'password':'lolwacode'},
        {'username':'production', 'password':'lolwacode'},
     ]
    for user in users:
        username = user['username']
        password = user['password']
        user_ = User.objects.create_user(username=username, password=password)
        if user_:
            print('User:{} Was Created.\nCreating Permissions...'.format(user_))
            manage = Manger.objects.create(user_id=user_, position=username)
            if manage:
                print('Manger: {} Was Created.'.format(manage.user_id.username))


from PIL import Image
import cv2
import io
import base64
import numpy as np

# Take in base64 string and return cv image
def stringToRGB(base64_string):
    if base64_string.rfind(',') != -1:  # <<cut data:image/png;base64 ','
        base64_string = base64_string.split(',')[1]

    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(io.BytesIO(imgdata))

    dimg = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    return dimg

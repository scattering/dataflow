from django.utils.translation import ugettext as _T
from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile

# Create your models here.
class UserProfile(UserenaBaseProfile):
    """
    User details such as home institution, etc., which we may wish to store
    in addition to the user details such as name and email maintained by
    django User.  The UserenaBaseProfile maintains the mug shot.  For now
    we are not maintaining a user profile.
    """
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_T('user'),
                                related_name='profile',
                                )

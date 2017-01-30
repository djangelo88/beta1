from datetime import datetime
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from base.models import Business


class CaterBackend(ModelBackend):
    def authenticate(self,username=None, password=None):

        UserModel = get_user_model()

        try:
            user = User.objects.get(email=username, is_active=True)

            if user.check_password(password):
                if settings.CHECK_SUBSCRIPTION_STATUS_ON_LOGIN:
                    business = Business.objects.get_business_by_user(user=user)
                    try:
                        business.check_subscription_status()
                    except:
                        pass
                return user
        except UserModel.DoesNotExist:
            print("Ex")
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)

        # user = ModelBackend().authenticate(username=username, password=password)
        #
        # if user:
        #     groups = user.groups.all()
        #     if(len(groups)) and groups.first().name in settings.BUSINESS_GROUPS:
        #         b = Business.objects.filter(owner=user).first()
        #         sub = b.subscription_set.filter(current=True).first()
        #         if sub.expire_date > datetime.date(datetime.today()) and sub.active:
        #             return user
        #         else:None
        #     else:
        #         return user
        # else:
        #     return None

    def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None
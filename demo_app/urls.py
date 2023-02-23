from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import CarListView
from .views import AddCarFormView
from .views import AdminLoginView
from .views import ThanksTemplateView
from .views import BuyFormView
from .views import MakeCarAvailableView


urlpatterns = [
    path("home/", CarListView.as_view(), name="home"),
    path("add_car/", AddCarFormView.as_view(), name="addcar"),
    path(
        "login/",
        AdminLoginView.as_view(redirect_authenticated_user=True),
        name="login_page",
    ),
    path("thankyou/", ThanksTemplateView.as_view(), name="thankyou"),
    path("buy/<str:cid>/", BuyFormView.as_view(), name="buy"),
    path("make_available/<str:cid>/", MakeCarAvailableView.as_view(), name="available"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

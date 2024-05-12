from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    # path('room/', views.room, name="room"),
    # path('signin/', views.signin, name="signin"),
    # path('signup/', views.signup, name="signup"),
    # path('employee_signin/', views.employee_signin, name="employee_signin"),
    # path('employee_signup/', views.employee_signup, name="employee_signup"),
    # path('signout/', views.signout, name='signout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
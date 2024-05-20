from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    # path('room/', views.room, name="room"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signout/', views.signout, name='signout'),
    path('create/', views.create_product, name='create_product'),
    path('room/<int:product_id>/', views.room, name='room'),
    path('cart/', views.cart, name='cart'),
    path('orders/', views.orders, name="orders"),
    path('payment/', views.payment, name='payment'),
    path('crocheter/', views.crocheter, name='crocheter'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
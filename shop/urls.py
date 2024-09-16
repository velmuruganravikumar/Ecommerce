from django.urls import path
from . import views

urlpatterns = [
   path('login/',views.login_page,name='login'),
   path('logout',views.logout_page,name='logout'),
   path('',views.home, name='home'),
   path('collections/',views.collections, name='collections'),
   path('register/',views.register, name='register'),
   path('collectionsview/<str:name>',views.collections_view, name='collectionsview'),  
   path('product_details/<str:cname>/<str:pname>',views.product_details, name='product_details'),
   path('addtocart/',views.add_To_Cart,name='addtocart'),
   path('cart/',views.cart_page,name='cart'),
   path('remove/<int:id>/',views.remove_page, name="remove"),
   path('favourite/',views.favourite_page,name="favourite"),
   path('favourite_view/',views.favourite_view,name="favourite_view"),
   path('remove_fav/<int:id>/',views.remove_fav,name="remove_fav"),
   
]
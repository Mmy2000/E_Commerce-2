from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('signup' , views.signup , name='signup'),
    path('profile/' , views.profile , name='profile'),
    path('profile/edit' , views.edit_profile , name='edit_profile'),
    path('dashboard/' , views.dashboard , name='dashboard'),
    path('' , views.dashboard , name='dashboard'),
    path('my_orders/' , views.my_orders , name='my_orders'),
    path('order_detail/<int:order_id>/' , views.order_detail , name='order_detail'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('favorite/' , views.user_favourites , name='user_favourites'),
]
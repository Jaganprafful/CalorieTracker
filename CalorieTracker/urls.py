from django.urls import path, include
from django.views.generic import TemplateView

from CalorieTracker.views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile_view, name='profile'),
    path('foodactivities/', food_activities_view, name='food_activities'),
    path('deleteitem/<int:id>/', delete_consumed_food, name='delete_item'),
    path('statisticalInfo/', statistical_view, name='statistical')
]

from . import views
from django.urls import path
urlpatterns=[
    path('',views.ShowChatHome,name='showchat'),
    # path('showDetails/',views.Details,name='showchat'),
    path('room/<str:room_name>/<str:person_name>', views.ShowChatPage, name='showchat'),
]
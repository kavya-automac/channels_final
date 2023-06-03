
from django.urls import path, re_path
from. import consumers



websocket_urlpatterns=[

    path('ws/sc/<str:groupname>/',consumers.MySyncConsumer.as_asgi()),#dynamic group name
    # path('ws/sc/', consumers.MySyncConsumer.as_asgi()),

    path('ws/ac/', consumers.MyAsyncConsumer.as_asgi()),

    # re_path(r'ws/sc/$', consumers.MySyncConsumer.as_asgi()),

]
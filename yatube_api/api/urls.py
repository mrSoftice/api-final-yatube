from django.urls import include, path

urlpatterns = [
    path('v1/jwt/', include('djoser.urls.jwt')),
]

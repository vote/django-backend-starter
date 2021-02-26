from django.urls import include, path

app_name: str = "api"
urlpatterns = [
    path("first_party/", include("first_party_app.api_urls")),
]

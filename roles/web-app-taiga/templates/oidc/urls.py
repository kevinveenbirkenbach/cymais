from taiga.urls import *
urlpatterns += [
    url(r"^oidc/", include("mozilla_django_oidc.urls")),
]
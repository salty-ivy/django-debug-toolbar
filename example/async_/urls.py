from django.urls import path

from example.async_ import views

urlpatterns = [
    path("async/db/", views.async_db_view, name="async_db_view"),
]

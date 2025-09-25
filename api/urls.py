from django.urls import path
from .views import CreateLinkTokenView

urlpatterns = [
    path('create_link_token/', CreateLinkTokenView.as_view(), name='create_link_token'),
]

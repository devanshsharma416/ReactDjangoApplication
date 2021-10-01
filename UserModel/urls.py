from django.urls import path
from .views import index, RegisterView, LoginAPIView, ArticleView
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'UserModel'
urlpatterns = [
    path('', index, name = 'index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('article/', ArticleView.as_view(), name = 'article')



]

urlpatterns = format_suffix_patterns(urlpatterns)
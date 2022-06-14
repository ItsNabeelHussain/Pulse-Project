from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import *

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenObtainPairView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/home/<int:pk>/', Home.as_view(), name="Home"),
    path('api/project/list/', ProjectList.as_view(), name="ProjectList"),
    path('api/project/<int:pk>/', ProjectView.as_view(), name="Project"),
    path('api/project/', ProjectView.as_view(), name="Project"),
    path('api/stock/list/<str:keyword>/', StockView.as_view(), name="Stock"),
    path('api/stock/classes/', StockClassesView.as_view())
]

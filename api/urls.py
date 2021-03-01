from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.cars.views import CarViewSet, CreateRatingView, PopularView


router = routers.DefaultRouter()
router.register(r'cars', CarViewSet)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('rate/', CreateRatingView.as_view()),
    path('popular/', PopularView.as_view()),
]

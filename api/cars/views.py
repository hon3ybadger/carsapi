from django.db.models import Count
from rest_framework import viewsets
from rest_framework import generics
from .models import Car, Rating
from .serializers import CarSerializer, RatingSerializer, PopularSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CreateRatingView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class PopularView(generics.ListAPIView):
    queryset = Car.objects.all().annotate(rates_number=Count('rating')).order_by('-rates_number')
    serializer_class = PopularSerializer

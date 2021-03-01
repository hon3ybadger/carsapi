from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Car, Rating
from .services import get_models_for_make


class CarSerializer(serializers.ModelSerializer):

    avg_rating = serializers.SerializerMethodField()

    def get_avg_rating(self, obj):
        average = Rating.objects.filter(car_id=obj.id).aggregate(Avg('rating')).get('rating__avg')
        return average

    def validate(self, data):
        make = data['make']
        model = data['model']
        if model.lower() not in get_models_for_make(make):
            raise serializers.ValidationError(f'Invalid make or model for: {make} {model}')
        return data

    class Meta:
        model = Car
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Car.objects.all(),
                fields=['make', 'model'],
                message='Car already exists in the database.'
            )
        ]


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'

    def validate_rating(self, value):
        min_value, max_value = 1, 5
        if value < min_value or value > max_value:
            raise serializers.ValidationError(f'Rating has to be in inclusive range of {min_value} - {max_value}')
        return value


class PopularSerializer(serializers.ModelSerializer):

    rates_number = serializers.IntegerField()

    class Meta:
        model = Car
        fields = '__all__'

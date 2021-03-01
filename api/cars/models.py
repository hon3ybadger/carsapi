from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        for field in ['make', 'model']:
            val = getattr(self, field, False)
            if val:
                setattr(self, field, val.capitalize())
        super().save(*args, **kwargs)


class Rating(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()

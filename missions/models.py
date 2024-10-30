from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

from missions.validators import validate_breed


class Cat(models.Model):
    name = models.CharField(max_length=30)
    years_of_experience = models.IntegerField(validators=[MaxValueValidator(15)])
    breed = models.CharField(max_length=30, validators=[validate_breed])
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Mission(models.Model):
    cat = models.ForeignKey(
        to=Cat,
        related_name='missions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    complete = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if self.cat:
            raise ValidationError('Cannot delete mission with assigned cat.')
        return super().delete(*args, **kwargs)


class Target(models.Model):
    mission = models.ForeignKey(
        to=Mission,
        related_name='targets',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)

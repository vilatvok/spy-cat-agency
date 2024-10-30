from django.core import exceptions
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from missions.models import Cat, Mission, Target
from missions.serializers import (
    CatSerializer,
    MissionSerializer,
    TargetSerializer,
    UpdateMissionSerializer,
    UpdateCatSerializer,
)


class CatViewSet(ModelViewSet):
    queryset = Cat.objects.all()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UpdateCatSerializer
        return CatSerializer


class MissionViewSet(ModelViewSet):
    queryset = Mission.objects.select_related('cat').prefetch_related('targets')

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UpdateMissionSerializer
        return MissionSerializer

    def perform_destroy(self, instance):
        try:
            super().perform_destroy(instance)
        except exceptions.ValidationError:
            raise ValidationError(
                detail='Cannot delete mission with assigned cat.'
            )


class TargetViewSet(ModelViewSet):
    queryset = Target.objects.select_related('mission')
    serializer_class = TargetSerializer

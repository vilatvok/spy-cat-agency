from rest_framework import serializers

from missions.models import Cat, Mission, Target


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary']


class UpdateCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ['salary']


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['name', 'country', 'notes', 'complete']


class MissionSerializer(serializers.ModelSerializer):
    cat = serializers.ReadOnlyField(source='cat.name')
    complete = serializers.ReadOnlyField()
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'complete', 'targets']

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)

        # Create each target and associate it with the created mission
        targets = []
        for target_data in targets_data:
            targets.append(Target(mission=mission, **target_data))
        
        Target.objects.bulk_create(targets)
        return mission


class UpdateMissionSerializer(serializers.ModelSerializer):
    complete = serializers.BooleanField()

    class Meta:
        model = Mission
        fields = ['cat', 'complete']



class TargetSerializer(serializers.ModelSerializer):
    mission_id = serializers.ReadOnlyField(source='mission.id')
    name = serializers.ReadOnlyField()
    country = serializers.ReadOnlyField()

    class Meta:
        model = Target
        fields = [
            'id',
            'mission_id',
            'name',
            'country', 
            'notes',
            'complete',
        ]

    def update(self, instance, validated_data):
        # Check if the mission is completed
        if instance.mission.complete or instance.complete:
            if 'notes' in validated_data:
                raise serializers.ValidationError(
                    'Cannot update notes if target or mission is completed.'
                )

        return super().update(instance, validated_data)

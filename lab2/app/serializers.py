from rest_framework import serializers
from .models import Team, Person, Coach, Osoba, Position

class TeamSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=60)
    country = serializers.CharField(max_length=2)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Team.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'shirt_size', 'month_added', 'team']

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'

class OsobaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Osoba
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

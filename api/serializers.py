from rest_framework import serializers

from api.models import Curator, Student, Specialty, StudyGroup, Discipline


class CuratorSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=80)
    last_name = serializers.CharField(max_length=80)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return Curator.objects.create_user(**validated_data)


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'


class SpecialtySerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(
        many=True,
        default=None,
        read_only=True
    )
    disciplines = DisciplineSerializer(
        many=True,
        default=[],
        read_only=True)

    class Meta:
        model = Specialty
        fields = '__all__'


class StudyGroupSerializer(serializers.ModelSerializer):
    specialty = serializers.PrimaryKeyRelatedField(queryset=Specialty.objects.all())

    class Meta:
        model = StudyGroup
        fields = '__all__'


class StudentSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=80)
    last_name = serializers.CharField(max_length=80)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    group = StudyGroupSerializer(default=None)

    def create(self, validated_data):
        validated_data.pop('group')
        return Student.objects.create_user(**validated_data)

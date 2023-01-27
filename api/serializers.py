from typing import OrderedDict

from rest_framework import serializers

from api.models import (
    Curator,
    Student,
    Specialty,
    StudyGroup,
    Discipline
)


class CuratorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data: dict) -> Curator:
        return Curator.objects.create_user(**validated_data)

    class Meta:
        model = Curator
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'


class SpecialtySerializer(serializers.ModelSerializer):
    curator = serializers.PrimaryKeyRelatedField(
        default=None,
        queryset=Curator.objects.all()
    )
    disciplines = serializers.PrimaryKeyRelatedField(
        many=True,
        default=[],
        queryset=Discipline.objects.all()
    )

    def create(self, validated_data: dict) -> Specialty:
        return Specialty.objects.create(name=validated_data.get('name'))

    def update(self, instance: Specialty, validated_data: dict) -> Specialty:
        method = self.context.get('request').method

        if method == 'PATCH':
            if 'disciplines' in validated_data:
                disciplines: list = validated_data.get('disciplines')

                for i in disciplines:
                    instance.disciplines.add(i)

            if 'curator' in validated_data:
                instance.curator = validated_data.get('curator')

        if method == 'DELETE':
            if 'disciplines' in validated_data:
                disciplines: list = validated_data.get('disciplines')

                for i in disciplines:
                    instance.disciplines.remove(i)

            if 'curator' in validated_data:
                instance.curator = None

        instance.save()
        return instance

    def to_representation(self, instance: Specialty) -> OrderedDict:
        representation = super().to_representation(instance)

        curator = CuratorSerializer(instance.curator).data
        if curator['email']:
            representation['curator'] = curator

        representation['disciplines'] = DisciplineSerializer(
            instance.disciplines.filter(id__in=representation['disciplines']),
            many=True
        ).data

        return representation

    class Meta:
        model = Specialty
        fields = ('id', 'name', 'curator', 'disciplines')


class StudyGroupSerializer(serializers.ModelSerializer):
    specialty = serializers.PrimaryKeyRelatedField(queryset=Specialty.objects.all())

    def to_representation(self, instance: StudyGroup) -> OrderedDict:
        representation = super().to_representation(instance)

        representation['specialty'] = SpecialtySerializer(
            Specialty.objects.get(id=representation['specialty'])
        ).data

        representation['students'] = StudentSerializer(
            Student.objects.filter(study_group_id=instance.id),
            many=True
        ).data

        return representation

    class Meta:
        model = StudyGroup
        fields = ('id', 'group_code', 'specialty', 'max_students')


class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    study_group = serializers.PrimaryKeyRelatedField(
        default=None,
        queryset=StudyGroup.objects.all()
    )

    def create(self, validated_data: dict) -> Student:
        validated_data.pop('study_group')
        return Student.objects.create_user(**validated_data)

    def update(self, instance: Student, validated_data: dict) -> Student:
        method = self.context.get('request').method

        if method == 'PATCH':
            study_group = validated_data.get('study_group')
            study_group.add_student(instance)

        if method == 'DELETE':
            instance.study_group = None

        instance.save()
        return instance

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'study_group')

from typing import OrderedDict, Optional

from django.contrib.auth.models import Permission
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
        password = validated_data.pop('password')
        curator = Curator.objects.create(**validated_data)
        curator.set_password(password)

        perms = Permission.objects.filter(
            codename__in=(
                'change_student',
                'add_studygroup',
                'change_studygroup'
            )
        )
        curator.user_permissions.set(perms)

        curator.save()
        return curator

    class Meta:
        model = Curator
        fields = ('id', 'first_name', 'last_name', 'email',
                  'password', 'work_experience', 'post')


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
        if self.context.get('request').method == 'PATCH':
            curator = validated_data.get('curator')

            if curator:
                instance.curator = curator
            else:
                instance.curator = None

            instance.save()
            return instance
        return super().update(instance, validated_data)

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
    specialty = serializers.PrimaryKeyRelatedField(
        queryset=Specialty.objects.all()
    )

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
        password = validated_data.pop('password')
        student = Student.objects.create(**validated_data)
        student.set_password(password)
        student.save()
        return student

    def update(self, instance: Student, validated_data: dict) -> Student:
        if self.context.get('request').method == 'PATCH':
            study_group: Optional[StudyGroup] \
                = validated_data.get('study_group')

            if study_group:
                study_group.add_student(instance)
            else:
                instance.study_group = None

            instance.save()
            return instance
        return super().update(instance, validated_data)

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'email',
                  'password', 'study_group', 'sex')


class SpecialtyAddDisciplinesSerializer(serializers.ModelSerializer):
    disciplines = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Discipline.objects.all()
    )

    def update(self, instance: Specialty, validated_data: dict) -> Specialty:
        disciplines: Optional[list] = validated_data.get('disciplines')

        if disciplines:
            for discipline in disciplines:
                instance.disciplines.add(discipline)

        instance.save()
        return instance

    class Meta:
        model = Specialty
        fields = ('id', 'name', 'disciplines')


class SpecialtyRemoveDisciplinesSerializer(serializers.ModelSerializer):
    disciplines = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Discipline.objects.all()
    )

    def update(self, instance: Specialty, validated_data: dict) -> Specialty:
        disciplines: Optional[list] = validated_data.get('disciplines')

        if disciplines:
            for discipline in disciplines:
                instance.disciplines.remove(discipline)

        instance.save()
        return instance

    class Meta:
        model = Specialty
        fields = ('id', 'name', 'disciplines')

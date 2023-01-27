from rest_framework import serializers

from api.models import Curator, Student, Specialty, StudyGroup, Discipline


class CuratorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return Curator.objects.create_user(**validated_data)

    class Meta:
        model = Curator
        fields = ('first_name', 'last_name', 'email', 'password')


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

    def to_representation(self, instance):
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
        fields = ('name', 'curator', 'disciplines')


class StudyGroupSerializer(serializers.ModelSerializer):
    specialty = serializers.PrimaryKeyRelatedField(queryset=Specialty.objects.all())

    class Meta:
        model = StudyGroup
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    group = StudyGroupSerializer(default=None)

    def create(self, validated_data: dict) -> Student:
        validated_data.pop('group')
        return Student.objects.create_user(**validated_data)

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email', 'password', 'group')

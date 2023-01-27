from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import (
    Curator,
    Student,
    Discipline,
    StudyGroup,
    Specialty
)
from api.serializers import (
    CuratorSerializer,
    StudentSerializer,
    DisciplineSerializer,
    StudyGroupSerializer,
    SpecialtySerializer,
    SpecialtyAddDisciplinesSerializer,
    SpecialtyRemoveDisciplinesSerializer
)


class EditableViewSet(ModelViewSet):
    """
    ViewSet that defines partial_update() behavior
    in order to conveniently manipulate with Specialty and Student
    """

    def partial_update(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class CuratorViewSet(ModelViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer
    # permission_classes = (CreateOrOwnerPermission,)


class StudentViewSet(EditableViewSet):
    queryset = Student.objects.select_related('study_group')
    serializer_class = StudentSerializer
    # permission_classes = (CreateOrIsCurator,)


class DisciplineViewSet(ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    # permission_classes = (permissions.IsAdminUser,)


class StudyGroupViewSet(ModelViewSet):
    queryset = StudyGroup.objects.select_related('specialty')
    serializer_class = StudyGroupSerializer
    # permission_classes = (IsCurator,)


class SpecialtyViewSet(EditableViewSet):
    queryset = Specialty.objects.select_related('curator').prefetch_related('disciplines')
    # permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action == 'add_disciplines':
            return SpecialtyAddDisciplinesSerializer
        elif self.action == 'remove_disciplines':
            return SpecialtyRemoveDisciplinesSerializer
        return SpecialtySerializer

    @action(methods=['PATCH'], detail=True)
    def add_disciplines(self, request, pk=None):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @action(methods=['PATCH'], detail=True)
    def remove_disciplines(self, request, pk=None):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

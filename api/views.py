from rest_framework import permissions
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
    SpecialtySerializer
)
from api.permissions import CreateOrOwnerPermission


class EditableViewSet(ModelViewSet):
    """
    ViewSet that defines partial_update() and destroy() behavior
    in order to conveniently manipulate with Specialty and Student
    """
    def partial_update(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        If there is some data in DELETE request, then we update fields by deleting
        these data from them
        Else just delete the object
        """
        if request.data:
            return self.partial_update(request)

        return super().destroy(request, *args, **kwargs)


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
    serializer_class = SpecialtySerializer
    # permission_classes = (permissions.IsAdminUser,)

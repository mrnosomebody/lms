from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.db import models
from rest_framework.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(
            self,
            email,
            first_name,
            last_name,
            password,
            is_superuser=False,
            is_admin=False
    ):
        password_invalid = validate_password(password, user=User)
        if password_invalid:
            return password_invalid

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            is_admin=is_admin
        )
        user.set_password(password)
        user.save(self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password):
        return self.create_user(
            email,
            first_name,
            last_name,
            password,
            is_superuser=True,
            is_admin=True
        )


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    deleted = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return perm in self.get_user_permissions()


class Curator(User):
    work_experience = models.IntegerField()
    post = models.CharField(max_length=255)


class Specialty(models.Model):
    name = models.CharField(max_length=255, unique=True)
    curator = models.ForeignKey(
        Curator,
        on_delete=models.PROTECT,
        related_name='specialty',
        null=True,
        blank=True
    )
    disciplines = models.ManyToManyField(
        'Discipline',
        related_name='specialties',
        blank=True
    )


class Discipline(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Student(User):
    study_group = models.ForeignKey(
        'StudyGroup',
        on_delete=models.PROTECT,
        related_name='students',
        null=True,
        blank=True
    )
    avg_grade = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )


class StudyGroup(models.Model):
    GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    group_code = models.CharField(max_length=6, unique=True)
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        related_name='study_groups'
    )
    sex = models.CharField(
        max_length=6,
        choices=GENDERS
    )
    max_students = models.IntegerField(default=20)

    def add_student(self, student: Student):
        if not student.study_group:
            if self.max_students > StudyGroup.objects.get(id=self.id) \
                    .students.count():
                student.study_group = self
                student.save()
                return self
            raise ValidationError(
                'Max amount of students in this group exceeded'
            )
        raise ValidationError('User is already in the group')

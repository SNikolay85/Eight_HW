from django.conf import settings
from django.db import models


class Student(models.Model):

    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):

    name = models.TextField()

    students = models.ManyToManyField(
        Student,
        blank=True,
    )

    def is_full(self):
        return self.students.count() >= settings.MAX_STUDENTS_PER_COURSE

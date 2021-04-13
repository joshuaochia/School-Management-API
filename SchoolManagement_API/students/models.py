from django.db import models
from django.conf import settings
from school.models import School, Courses, Employees
from school.conf import sex, status
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.

days = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]

sem = [
    ('First', 'First'),
    ('Second', 'Second')
]

grade_status = [
    ('Passed', 'Passed'),
    ('Completed', 'Completed'),
    ('Failed', 'Failed'),
    ('INC', 'INC')
]


class Schedule(models.Model):

    start = models.TimeField()
    end = models.TimeField()
    day = models.CharField(max_length=55, choices=days)

    def __str__(self):

        return f"{self.start} - {self.end} ({self.day})"


class Section(models.Model):

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, verbose_name='Room Code')

    def __str__(self):
        return f"{self.name} (Room {self.code})"


class Subjects(models.Model):

    name = models.CharField(max_length=556)
    teacher = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name='subject'
        )
    course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        )
    code = models.CharField(max_length=55, verbose_name='Subject Code')
    unit = models.PositiveSmallIntegerField()
    lab = models.PositiveSmallIntegerField()
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='subject'
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='subject'
    )

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

    def __str__(self):
        return f"{self.name} ({self.section.code}) {self.schedule}"


class Students(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student',
        null=True
    )
    pic = models.ImageField(
        upload_to='student_pic',
        null=True,
        blank=True
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='students'
    )
    course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        related_name='students'
        )
    bday = models.DateField(null=True, verbose_name='Birth Day')
    country = CountryField(null=True)
    city = models.CharField(max_length=255, null=True)
    zip_code = models.PositiveSmallIntegerField(
        verbose_name='Zip Code',
        null=True
        )
    sex = models.CharField(max_length=55, choices=sex, null=True)
    civil_status = models.CharField(
        max_length=55,
        choices=status,
        verbose_name='Civil Status',
        null=True
        )
    subjects = models.ManyToManyField(Subjects, through='StudentSubject')
    school_yr = models.CharField(default='2012', max_length=255)
    sem = models.CharField(choices=sem, max_length=55)
    slug = models.SlugField(null=True)

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    def save(self, *args, **kwargs):

        self.slug = slugify(self.user.first_name + '' + self.user.last_name)
        return super().save(*args, **kwargs)

    @property
    def get_year(self):
        date = timezone.datetime.strptime('%Y', self.school_yr)
        return date

    def __str__(self):

        return f"{self.user}"


class StudentSubject(models.Model):

    student = models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        related_name='student_subject'
    )
    abs = models.IntegerField(default=0)
    grade = models.IntegerField(default=0)

    def __str__(self):

        return f'{self.student}'


class SubjectAverage(models.Model):

    stud_sub = models.ForeignKey(
        StudentSubject,
        on_delete=models.CASCADE,
        related_name='average'
    )
    avg = models.IntegerField()
    status = models.CharField(max_length=255, choices=grade_status)

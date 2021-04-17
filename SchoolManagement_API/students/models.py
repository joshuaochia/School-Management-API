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
        related_name='student_sub'
    )
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        related_name='student_subject'
    )
    period_1 = models.IntegerField(default=0)
    abs_1 = models.IntegerField(default=0)
    period_2 = models.IntegerField(default=0)
    abs_2 = models.IntegerField(default=0)
    period_3 = models.IntegerField(default=0)
    abs_3 = models.IntegerField(default=0)
    avg = models.IntegerField(default=0)
    status = models.CharField(max_length=255, choices=grade_status)

    def __str__(self):

        return f'{self.student}'


class Project(models.Model):

    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    title = models.CharField(max_length=255)
    dead_line = models.DateTimeField(verbose_name='Dead Line')
    description = models.TextField(max_length=5006)
    assign = models.ManyToManyField(
        StudentSubject,
        related_name='my_project',
        verbose_name='Members'
    )
    sample = models.FileField(
        upload_to='project/',
        null=True
        )
    files = models.ManyToManyField(
        StudentSubject,
        through='FileProject',
        blank=True
    )


class Assignment(models.Model):

    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        related_name='assignment'
    )
    title = models.CharField(max_length=255)
    dead_line = models.DateTimeField(verbose_name='Dead Line')
    description = models.TextField(max_length=5006)
    assign = models.ManyToManyField(
        StudentSubject,
        related_name='my_assignment',
        verbose_name='Members',
        blank=True
    )
    sample = models.FileField(
        upload_to='assignment/',
        null=True
        )
    files = models.ManyToManyField(
        StudentSubject,
        through='FileAssignment',
        blank=True
    )


class FileAssignment(models.Model):

    student = models.ForeignKey(
        StudentSubject,
        on_delete=models.CASCADE,
        related_name='assignment_file',
        null=True
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='assignment_files',
        null=True
    )
    file = models.FileField(upload_to='assignment/')


class FileProject(models.Model):

    student = models.ForeignKey(
        StudentSubject,
        on_delete=models.CASCADE,
        related_name='project_file',
        null=True
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_files',
        null=True
    )
    file = models.FileField(upload_to='project/')

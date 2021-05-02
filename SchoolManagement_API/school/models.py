from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from .conf import majors, courses, status, sex
from django.conf import settings
from django.utils.text import slugify

days = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]

class School(models.Model):

    name = models.CharField(max_length=255, unique=True)
    vision = models.CharField(max_length=255, null=True)
    mission = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    country = CountryField(null=True)
    city = models.CharField(max_length=255)
    zip_code = models.PositiveSmallIntegerField(
        verbose_name='Zip Code',
        null=True
        )
    date_funded = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Policies(models.Model):

    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='policies'
        )
    policy = models.CharField(max_length=556)

    class Meta:
        verbose_name = _('Policie')
        verbose_name_plural = _("Policies")

    def __str__(self):
        return f'{self.school} Policy'


class Department(models.Model):

    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='departments'
        )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Courses(models.Model):

    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='courses'
        )
    course = models.CharField(max_length=556, choices=courses)
    major = models.CharField(max_length=556, choices=majors)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _("Courses")

    def __str__(self):

        return self.course + ' major in ' + self.major

class Employees(models.Model):

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='employee',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='e_user',
        on_delete=models.CASCADE,
        null=True
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='workers'
    )
    position = models.CharField(max_length=255, null=True)
    bday = models.DateField(null=True, verbose_name='Birth Day')
    country = CountryField(default='PH')
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
        null=True,
        default='Single'
        )
    rate = models.PositiveSmallIntegerField(verbose_name='Daily Rate')
    days_week = models.PositiveSmallIntegerField(verbose_name='Weekly Hrs')
    salary = models.PositiveIntegerField(default=0)
    slug = models.SlugField(null=True)
    is_employee = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.first_name + '' + self.user.last_name)
        return super().save(*args, **kwargs)

    def __str__(self):

        return f'{self.user} of {self.department} ({self.school})'


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
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        )
    course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        related_name = 'subject_course'
        )
    code = models.CharField(max_length=55, verbose_name='Subject Code')
    unit = models.PositiveSmallIntegerField()
    lab = models.PositiveSmallIntegerField()
    cost = models.IntegerField()


    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

    def __str__(self):
        return f"{self.name}"

class TeacherSubject(models.Model):

    teacher = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        null=True,
        related_name='teacher_sub'
        )
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        related_name='sub_teacher'
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,

    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.subject} ({self.section.code}) {self.schedule}'

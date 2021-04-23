from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from .conf import majors, courses, sex, status
from django.conf import settings
from django.utils.text import slugify


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
    staff = models.ManyToManyField(School, through='employees')
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

    slug = models.SlugField(null=True)

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.first_name + '' + self.user.last_name)
        return super().save(*args, **kwargs)

    def __str__(self):

        return f'{self.user} of {self.department} ({self.school})'

from django.db import models
from django.conf import settings


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username

    class Info(models.Model):
        FRESHMAN = "FR"
        SOPHOMORE = "SO"
        JUNIOR = "JR"
        SENIOR = "SR"
        GRADUATE = "GR"
        YEAR_IN_SCHOOL_CHOICES = {
            (FRESHMAN, "Freshman"),
            (SOPHOMORE, "Sophomore"),
            (JUNIOR, "Junior"),
            (SENIOR, "Senior"),
            (GRADUATE, "Graduate"),
        }

        SINGLE = "SI"
        MARRIED = "MA"
        SEPARATED = "SE"
        MARITAL_CHOICES = {
            (SINGLE, "Single"),
            (MARRIED, "Married"),
            (SEPARATED, "Separated"),
        }

        age = models.PositiveSmallIntegerField()
        gender = models.CharField(max_length=30)
        ethnicity = models.CharField(max_length=30)
        veteran = models.BooleanField(default=False)
        qada = models.BooleanField(default=False)
        income = models.FloatField()

        year_in_school = models.CharField(
            max_length=2,
            choices=YEAR_IN_SCHOOL_CHOICES,
            default=FRESHMAN,
        )

        marital_status = models.CharField(
            max_length=2,
            choices=MARITAL_CHOICES,
            default=SINGLE,
        )
        employment = models.CharField(max_length=100)
        involvement = models.CharField(max_length=5000)

        def __str__(self):
            return self.username


class Info(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='info')

    FRESHMAN = "FR"
    SOPHOMORE = "SO"
    JUNIOR = "JR"
    SENIOR = "SR"
    GRADUATE = "GR"
    YEAR_IN_SCHOOL_CHOICES = {
        (FRESHMAN, "Freshman"),
        (SOPHOMORE, "Sophomore"),
        (JUNIOR, "Junior"),
        (SENIOR, "Senior"),
        (GRADUATE, "Graduate"),
    }

    SINGLE = "SI"
    MARRIED = "MA"
    SEPARATED = "SE"
    MARITAL_CHOICES = {
        (SINGLE, "Single"),
        (MARRIED, "Married"),
        (SEPARATED, "Separated"),
    }

    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=30)
    ethnicity = models.CharField(max_length=30)
    veteran = models.BooleanField(default=False)
    qada = models.BooleanField(default=False)
    income = models.FloatField()

    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )

    marital_status = models.CharField(
        max_length=2,
        choices=MARITAL_CHOICES,
        default=SINGLE,
    )
    employment = models.CharField(max_length=100)
    involvement = models.CharField(max_length=5000)

    def __str__(self):
        return {"age": str(self.age),
                "gender": str(self.gender),
                "ethnicity": str(self.ethnicity),
                "veteran": str(self.veteran),
                "qada": str(self.qada),
                "income": str(self.income),
                "year_in_school": str(self.year_in_school),
                "marital_status": str(self.marital_status),
                "employment": str(self.employment),
                "involvement": str(self.involvement)
                }


class Scholarship(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

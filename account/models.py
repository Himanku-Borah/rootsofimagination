from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User

class MyAccountManager(BaseUserManager):
  def create_user(self, first_name, last_name, username, email, password=None):
    if not email:
      raise ValueError('User must have an email address')

    if not username:
      raise ValueError('User must have an username')

    user = self.model(
      email = self.normalize_email(email),
      username = username,
      first_name = first_name,
      last_name = last_name
    ) 

    user.set_password(password)
    user.save(using = self._db)
    return user
  
  def create_superuser(self, first_name, last_name, email, username, password):
    user = self.create_user(
      email = self.normalize_email(email),
      username = username,
      password = password,
      first_name = first_name,
      last_name = last_name,

    )
    user.is_admin = True
    user.is_active = True
    user.is_staff = True
    user.is_superadmin = True
    user.save(using=self._db)
    return user

class Account(AbstractBaseUser):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  username = models.CharField(max_length=50, unique=True)
  email = models.EmailField(max_length=100, unique=True)
  phone_number = models.CharField(max_length=30, unique=True, null=True)

  #required fields
  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now_add=True)
  is_admin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  is_superadmin = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  objects = MyAccountManager()

  def __str__(self):
    return self.email
  
  def has_perm(self, obj=None):
    return self.is_admin
  
  def has_module_perms(self, add_label):
    return True
  
  @property
  def has_student_details(self):
    try:
        self.student_details
        return True
    except Account.student_details.RelatedObjectDoesNotExist:
        return False

class Academic(models.Model):
  x_board = models.CharField(max_length=200, null=True)
  x_year = models.CharField(max_length=20, null=True)
  x_subjects = models.CharField(max_length=300, null=True)
  x_percentage = models.DecimalField(max_digits=5, decimal_places=2, null = True)

  xii_board = models.CharField(max_length=200, null=True)
  xii_year = models.CharField(max_length=20, null=True)
  xii_subjects = models.CharField(max_length=300, null=True)
  xii_percentage = models.DecimalField(max_digits=5, decimal_places=2, null = True)

  degree_university = models.CharField(max_length=200, null=True)
  degree_year = models.CharField(max_length=20, null=True)
  degree_subjects = models.CharField(max_length=300, null=True)
  degree_percentage = models.DecimalField(max_digits=5, decimal_places=2, null = True)

  pg_university = models.CharField(max_length=200, null=True)
  pg_year = models.CharField(max_length=20, null=True)
  pg_subjects = models.CharField(max_length=300, null=True)
  pg_percentage = models.DecimalField(max_digits=5, decimal_places=2, null = True)

  other_university = models.CharField(max_length=200, null=True)
  other_year = models.CharField(max_length=20, null=True)
  other_subjects = models.CharField(max_length=300, null=True)
  other_percentage = models.DecimalField(max_digits=5, decimal_places=2, null = True)

  def __str__(self):
    return "Academic Details"

  class Meta:
        db_table = 'academics'
        managed = True
        verbose_name = 'Academic'
        verbose_name_plural = 'Academics'

class Student(models.Model):
  Male = 'M'
  Female = 'F'
  Others = 'Others'
  GENDER_CHOICES = (
    (Male, 'Male'),
    (Female, 'Female'),
    (Others, 'Others'),
  )

  user = models.OneToOneField(Account, on_delete=models.DO_NOTHING, null = True, related_name='student_details')
  name = models.CharField(max_length=100, null=True)
  father_name = models.CharField(max_length=100, null=True)
  mother_name = models.CharField(max_length=100, null=True)
  father_occupation = models.CharField(max_length=300, null=True)
  mother_occupation = models.CharField(max_length=300, null=True)
  mailing_address = models.EmailField(max_length=100, unique=True)
  address = models.CharField(max_length=200, null = True)
  dob = models.DateField(auto_now=False, auto_now_add=False)
  gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True)
  course = models.CharField(max_length=50, null=True)
  profile_photo = models.ImageField(upload_to = 'students/profile_photos/', null = True, default = 'students/profile_photos/profile.png')
  academic = models.OneToOneField(Academic, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return "%s %s %s" % (self.name, self.father_name, self.course)

  class Meta:
        db_table = 'students'
        managed = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

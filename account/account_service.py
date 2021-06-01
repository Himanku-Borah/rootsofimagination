
from account.models import Academic, Account, Student
from django.urls import reverse
from django.utils.html import format_html
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import datetime

# Email Sending
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import random


class AccountService(object):
    instance = None

    def __new__(cls):
        if cls.instance is not None:
            return cls.instance
        else:
            ins = cls.instance = super(AccountService, cls).__new__()
            return ins

    def __init__(self):
        pass

    def linkToForeignKey(column_name):
        def _linkToForeignKey(obj):
            linked_obj = getattr(obj, column_name)
            if linked_obj is None:
                return '-'
            app_label = linked_obj._meta.app_label
            model_name = linked_obj._meta.model_name
            view_name = f'admin:{app_label}_{model_name}_change'
            link_url = reverse(view_name, args=[linked_obj.pk])
            return format_html('<a href="{}">{}</a>', link_url, linked_obj)

        _linkToForeignKey.short_description = column_name
        return _linkToForeignKey

    def saveAcademicDetails(cleaned_data):
        academic = Academic(
            x_board=cleaned_data['x_board'],
            x_year=cleaned_data['x_year'],
            x_subjects=cleaned_data['x_subjects'],
            x_percentage=cleaned_data['x_percentage'],

            xii_board=cleaned_data['xii_board'],
            xii_year=cleaned_data['xii_year'],
            xii_subjects=cleaned_data['xii_subjects'],
            xii_percentage=cleaned_data['xii_percentage'],

            degree_university=cleaned_data['degree_university'],
            degree_year=cleaned_data['degree_year'],
            degree_subjects=cleaned_data['degree_subjects'],
            degree_percentage=cleaned_data['degree_percentage'],

            pg_university=cleaned_data['pg_university'],
            pg_year=cleaned_data['pg_year'],
            pg_subjects=cleaned_data['pg_subjects'],
            pg_percentage=cleaned_data['pg_percentage'],

            other_university=cleaned_data['other_university'],
            other_year=cleaned_data['other_year'],
            other_subjects=cleaned_data['other_subjects'],
            other_percentage=cleaned_data['other_percentage'],
        )
        academic.save()
        return academic

    def saveStudentDetails(cleaned_data, user, academic):
        student = Student(
            user=user,
            name=cleaned_data['name'],
            father_name=cleaned_data['father_name'],
            mother_name=cleaned_data['mother_name'],
            father_occupation=cleaned_data['father_occupation'],
            mother_occupation=cleaned_data['mother_occupation'],
            mailing_address=user.email,
            address=cleaned_data['address'],
            dob=cleaned_data['dob'],
            gender=cleaned_data['gender'],
            course=cleaned_data['course'],
            academic=academic,
        )
        student.save()
        return student

    def getUniqueProfileImageName(user, filename):
        profile_name = f'{datetime.datetime.now()}_{user.username}_{filename}'
        return profile_name

    def saveProfile(student, files, filename):
        profile = files['profile_photo']
        if profile:
            new_profile = Image.open(profile)
            new_profile.thumbnail((300, 300), Image.ANTIALIAS)
            profile_bytes = BytesIO()
            new_profile.save(profile_bytes, format=new_profile.format)
            profile_buffer = ContentFile(profile_bytes.getvalue())
            profile_to_save = InMemoryUploadedFile(
                profile_buffer, None, filename, 'image/jpeg', profile_buffer.tell, None)
            student.profile_photo = profile_to_save
            student.save()
            return student

    # sending email

    def sendEmail(user, current_site, mail_subject, template):
        message = render_to_string(template, {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

    def saveUser(cleaned_data):
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        phone_number = cleaned_data['phone_number']
        email = cleaned_data['email']
        password = cleaned_data['password']

        r1 = random.randint(0, 1000)
        username = email.split('@')[0] + str(r1)

        user = Account.objects.create_user(
            first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.phone_number = phone_number

        user.save()
        return user

    def checkActivation(email, password):
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            return user.is_active

    def validateEmailLink(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        return user, uid

    def updateUserPassword(uid, password):
        user = Account.objects.get(pk=uid)
        user.set_password(password)
        user.save()

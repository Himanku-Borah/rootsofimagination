from django.db import transaction
from django.db import IntegrityError
from account.account_service import AccountService
from django.shortcuts import render, redirect
from .forms import AdmissionForm, SignupForm
from .models import Account, Student
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

# Email Verification
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator


# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = AccountService.saveUser(cleaned_data=form.cleaned_data)

            # User Activation
            template = 'account/acc_verification_mail.html'
            AccountService.sendEmail(user=user, current_site=get_current_site(
                request), mail_subject="Please activate your account", template=template)

            # messages.success(request, 'Registration Successfull. Please check your mail to activate your account.')
            return redirect('/account/login/?command=verification&email='+user.email)
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return render(request, 'account/signup.html', context)


# Resend Verification Link View
def resendEmail(request, email):
    if Account.objects.filter(email=email).exists():

        user = Account.objects.get(email__exact=email)
        template = 'account/acc_verification_mail.html'
        # send email
        AccountService.sendEmail(user=user, current_site=get_current_site(
            request), mail_subject="Please activate your account", template=template)

        # messages.success(request, 'Registration Successfull. Please check your mail to activate your account.')
        return redirect('/account/login/?command=verification&email='+email)
    else:
        messages.error(
            request, "There is something wrong. Please try to signup again with a different email id.")
        return redirect('resendemail')

    return render(request, 'account/resendemail.html')


# Login View
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        #checking if the account is active
        if AccountService.checkActivation(email=email, password=password) is False:
          return redirect('/account/login/?command=notactive&email='+email)

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'account/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('login')


def activate(request, uidb64, token):
    user, uid = AccountService.validateEmailLink(uidb64=uidb64)

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "Congratulations, Your account is activated.")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link!")
        return redirect('signup')


@login_required(login_url='login')
def dashboard(request):
    studentDetails = Student.objects.filter(user=request.user.pk).first()
    context = {'studentDetails': studentDetails}
    return render(request, 'account/dashboard.html', context=context)


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            # Reset Password Email
            template = 'account/reset_password_email.html'
            AccountService.sendEmail(user=user, current_site=get_current_site(
                request), mail_subject="Reset your password", template=template)

            messages.success(
                request, "Password reset email has been sent to your email address.")
            return redirect('login')
        else:
            messages.error(request, 'Account doesnot exist')
            return redirect('forgotpassword')
    return render(request, 'account/forgotpassword.html')


def resetpassword_validate(request, uidb64, token):

    user, uid = AccountService.validateEmailLink(uidb64=uidb64)

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password")
        return redirect('resetPassword')

    else:
        messages.error(request, "This link has been expired!")
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = AccountService.updateUserPassword(uid=uid, password=password)
            messages.success(request, "Password reset successfull.")
            return redirect('login')

        else:
            messages.error(request, "Password doesnot match")
            return redirect('resetPassword')
    else:
        return render(request, 'account/resetPassword.html')


@method_decorator(login_required(login_url='login'), name='dispatch')
class AdmissionView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'account/admission.html')

    def post(self, request, *args, **kwargs):
        form = AdmissionForm(request.POST, request.FILES)
        # getting the logged in user
        user = request.user
        print(request.FILES)
        if form.is_valid():
            with transaction.atomic():
                # save data to database
                try:
                    academic = AccountService.saveAcademicDetails(
                        cleaned_data=form.cleaned_data)
                    if academic:
                        student = AccountService.saveStudentDetails(
                            cleaned_data=form.cleaned_data, user=user, academic=academic)

                        # save profile photo
                        if request.FILES.get('profile_photo', False):
                            print("profile photo found")
                            profile_name = AccountService.getUniqueProfileImageName(
                                user=user, filename=request.FILES['profile_photo'])
                            profile = AccountService.saveProfile(
                                student=student, files=request.FILES, filename=profile_name)

                        messages.success(
                            request, "Your application is in process. Please wait until team contacts you. Thanks")
                        return redirect('dashboard')
                except(IntegrityError):
                    messages.error(request, "You have already enrolled")
                    return redirect('dashboard')

        context = {'form': form}
        return render(request, 'account/admission.html', context=context)

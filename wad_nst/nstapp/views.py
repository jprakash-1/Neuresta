import os
import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm, FeedbackForm, UserUpdateForm, ProfileUpdateForm, ImageForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pathlib import Path

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from nstapp.ML.nst_run import run


def home(request):
    return render(request, "home.html")
    """
    Signup function to register the user into the website
    for that We are using django inbuilt model User and added
    extra field email in USerCreationForm and Created a new Form
    As User RegistrationForm in forms.py.

    When we get a request.POST method we are checking for some
    variables and afterwards we are the form into database.

    Returns
    -------
        After sucess we are redirection user to the home page.
    """

def signupuser(request):

    if request.method == "GET":
        return render(request, "signupuser.html", {"forms": UserRegistrationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"],
                    password=request.POST["password1"],
                    email=request.POST["email"],
                )
                user.save()
                # When user signed in redirect to new url.
                login(request, user)
                return redirect("home")

            except IntegrityError:
                return render(
                    request,
                    "signupuser.html",
                    {
                        "forms": UserRegistrationForm(),
                        "error": "Username is already taken try other!",
                    },
                )

        else:
            # Tell the use user password didn't match.
            return render(
                request,
                "signupuser.html",
                {"forms": UserCreationForm(), "error": "Password did not match"},
            )


def about(request):
    return render(request, "about.html")


def gallery(request):
    return render(request, "gallery.html")

    """
    Logging out the user using django inbuilt function logout()

    Returns
    -------
        After logging out we are redirectiong user to the home
        page.
    """

@login_required
def logoutuser(request):

    logout(request)
    return redirect("home")

    """
    Logging in the user into the website for that we are using
    django form AuthenticationForm() when we get POST method we
    authenticate the user from data we have in database. If didn't
    match e return an error. Then redirect it to the home page.

    Parameters
    ----------
    request :
        Httprequest Django creates an HttpRequest object that
        contains metadata about the request. Then Django loads
        the appropriate view, passing the HttpRequest as the
        first argument to the view function. Each view is
        responsible for returning an HttpResponse object.


    Returns
    -------
    If it's a get method e return form. Else if a post method
    and no error if redirect to home page or else we return error.

    """
def loginuser(request):

    if request.method == "GET":
        return render(request, "loginuser.html", {"forms": AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"]
        )
        if user is None:
            return render(
                request,
                "loginuser.html",
                {"forms": AuthenticationForm(), "error": "Username and password did not match"},
            )
        else:
            login(request, user)
            return redirect("home")



@login_required
def profile(request):
    return render(request, "profile.html")


    """
    Feedback Form where user can post their views experiance and
    suggestions for the admin. Similar to login page here we have
    to create model and the using forms swe can take input from
    user and store in the database.


    Returns
    -------
    If it's a get method e return form. Else if a post method
    and no error if redirect to home page or else we return error.

    """
@login_required
def feedback(request):

    if request.method == "GET":
        return render(request, "feedback.html", {"form": FeedbackForm()})
    else:
        try:
            form = FeedbackForm(request.POST)  # Put all the data we get from webpage
            newtodo = form.save()  # Saving the value.
            return redirect("home")
        except ValueError:
            return render(
                request, "feedback.html", {"form": FeedbackForm(), "error": "Bad Data Try Again !"}
            )


    """
    Updating user profile but we keep the user data filled in
    it so that they have to edit only those part that they wish
    to change. Using two form UserUpdateForm and ProfileUpdateForm
    As there is no field of image in User model so we can't do it
    directly. Checking if form is valid if valid update the data.
    Else error.


    Returns
    -------
    Redirecting it to the Profile page
    """
@login_required
def profileUpdate(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("profile")
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

            context = {"u_form": u_form, "p_form": p_form}
            return render(
                request, "profileUpdate.html", context, {"error": "Bad Data ! Try Again"}
            )

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {"u_form": u_form, "p_form": p_form}
        return render(request, "profileUpdate.html", context)

    """
    Image upload app to take user input two images and run it through the 
    ML algorithm and generate the new styled image. For the run function
    we need the address of images that we are collecting in path1,path2 
    and path3. For the simplicity sake as of now we fix the output image name.


    Returns:
            If it's a get method return form. Else if a post method
    and no error if redirect to image Generated page where user can 
    see the image genrated or else we return error.
    """    

def imageupload(request):

    if request.method == "GET":
        return render(request, "imageupload.html", {"form": ImageForm()})
    else:
        try:
            BASE_DIR = Path(__file__).resolve().parent.parent
            form = ImageForm(request.POST, request.FILES)  # Put all the data we get from webpage
            newtodo = form.save()  # Saving the value.
            imageName1 = request.FILES["Content"].name
            imageName2 = request.FILES["Style"].name
            imageName3 = "abaa.jpg"
            path1 = BASE_DIR / "media" / "style" / imageName1
            path2 = BASE_DIR / "media" / "base" / imageName2
            path3 = BASE_DIR / "media" / "generated" / imageName3

            run(path2, path1, path3)

            return render(
                request,
                "about.html",
                {
                    "path1": path1,
                    "path2": path2,
                    "path3": path3,
                },
            )

        except ValueError:
            return render(
                request, "imageupload.html", {"form": ImageForm(), "error": "Bad Data Try Again !"}
            )


def generated(request):
    return render(request, "generatedimage.html")
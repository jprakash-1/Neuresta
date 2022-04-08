from django.db import models
from PIL import Image
from django.contrib.auth.models import User



class Profile(models.Model):
    """
    Creating a new model name Profile for our profile
    page that is having Foreign key constraint with User
    model. And other image field for profile pics that
    will stored in profile_pics subolder inside media if they
    upload or else default.jpg pic.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"

    """
    Creating a new model name Feedback to get the views of user 
    about our website. We are storing thier mail id for their 
    refrence. Created will automatically store the time feedback
    posted.

    """
class Feedback(models.Model):
    email = models.EmailField(max_length=254)
    title = models.CharField(max_length=100)
    feedback = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



    """
    Created a model name Image to get user image and feed it to the 
    ML model and display the output. And storing the images in media
    folder in their respective subfolder. 
    """ 
class Image(models.Model):
   
    image1 = models.ImageField(upload_to="style")
    image2 = models.ImageField(upload_to="base")
    image3 = models.ImageField(upload_to="generated")

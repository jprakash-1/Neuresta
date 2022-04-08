# from nstapp.ML import *
# from nstapp.ML.img_loader import ImageLoader
# from nstapp.ML.img_unloader import Unloader
# from nstapp.ML.nst import get_input_optimizer, get_style_model_and_losses
import os
import sys

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from ML import *
from ML.img_loader import ImageLoader
from ML.img_unloader import Unloader
from ML.nst import get_input_optimizer, get_style_model_and_losses


def run_style_transfer(
    cnn,
    normalization_mean,
    normalization_std,
    content_img,
    style_img,
    input_img,
    num_steps=300,
    style_weight=1000000,
    content_weight=1,
):
    """This function runs the neural style transfer algorithm. This is not to be used eternally
    outside the ML library

    Parameters
    ----------
    cnn : torch model
        Convolutional neural network
    normalization_mean : float
        mean
    normalization_std : float
        standard deviation
    content_img : img
        The original content image
    style_img : img
        The style image
    input_img : img
        copy of content image
    num_steps : int, optional
        number of steps in optimization, by default 300
    style_weight : int, optional
        hyperparam to adjust amount of styling, by default 1000000
    content_weight : int, optional
        hyperparam to adjust amount of styling, by default 1

    Returns
    -------
    img
        The final stylized image
    """
    print("Building the style transfer model..")
    model, style_losses, content_losses = get_style_model_and_losses(
        cnn, normalization_mean, normalization_std, style_img, content_img
    )
    optimizer = get_input_optimizer(input_img)

    print("Optimizing..")
    run = [0]
    while run[0] <= num_steps:

        def closure():
            # correct the values of updated input image
            input_img.data.clamp_(0, 1)

            optimizer.zero_grad()
            model(input_img)
            style_score = 0
            content_score = 0

            for sl in style_losses:
                style_score += sl.loss
            for cl in content_losses:
                content_score += cl.loss

            style_score *= style_weight
            content_score *= content_weight

            loss = style_score + content_score
            loss.backward()

            run[0] += 1
            if run[0] % 50 == 0:
                print("run {}:".format(run))
                print(
                    "Style Loss : {:4f} Content Loss: {:4f}".format(
                        style_score.item(), content_score.item()
                    )
                )
                print()

            return style_score + content_score

        optimizer.step(closure)

    input_img.data.clamp_(0, 1)

    return input_img


def run(contentpath, stylepath, savepath):
    """This is the external facing run fucntion. Calling this function runs the Neural Style
    Transfer algorithm.

    Parameters
    ----------
    contentpath : str
        The path to the content image.
    stylepath : str
        The path to the style image.
    savepath : str
        The path to save the stylized image.
    """
    loader = ImageLoader(contentpath=contentpath, stylepath=stylepath)

    content_img, style_img = loader.open_images()
    input_img = content_img.clone()

    img = run_style_transfer(
        cnn=cnn,
        normalization_mean=cnn_normalization_mean,
        normalization_std=cnn_normalization_std,
        content_img=content_img,
        style_img=style_img,
        input_img=input_img,
    )

    pil_img = Unloader().pil_img(img)
    pil_img.save(savepath)


if __name__ == "__main__":
    run(
        "/Users/shreyasms/1.Data/2.College_new/Assignments/Sem4/WAD/Project/WAD_NST/wad_nst/nstapp/static/gallery_images/panda.jpg",
        "/Users/shreyasms/1.Data/2.College_new/Assignments/Sem4/WAD/Project/WAD_NST/wad_nst/nstapp/static/gallery_images/abstract_woman.jpg",
        "/Users/shreyasms/Desktop/picture.jpg",
    )

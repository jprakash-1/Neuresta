from . import *


class ImageLoader:
    """This is the image loader class.

    Parameters
    ----------
    contentpath : str
        path to the content image.
    stylepath : str
        path to the style image.
    """

    def __init__(self, contentpath, stylepath):

        self.stylepath = stylepath
        self.contentpath = contentpath

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.imsize = 512 if torch.cuda.is_available() else 128  # use small size if no gpu
        self.loader = transforms.Compose(
            [
                transforms.Resize((self.imsize, self.imsize)),
                transforms.ToTensor(),
            ]  # scale imported image
        )

    # transform it into a torch tensor

    def image_loader(self, image_name):
        """Function to load the image.

        Parameters
        ----------
        image_name : str
            The name of the image.

        Returns
        -------
        image: torch.Tensor
            Returns the image ready to be passed through the model.
        """
        image = Image.open(image_name)
        image = self.loader(image).unsqueeze(0)

        return image.to(device, torch.float)

    # style_img = image_loader("./data/images/neural-style/picasso.jpg")
    # content_img = image_loader("./data/images/neural-style/dancing.jpg")
    def open_images(self):
        """Function to open the image.

        Returns
        -------
        tuple
            Returns a tuple of the content image and the style image.
        """
        style_img = self.image_loader(self.stylepath)
        content_img = self.image_loader(self.contentpath)
        print(style_img.size())
        print(content_img.size())
        assert style_img.size() == content_img.size()

        return content_img, style_img

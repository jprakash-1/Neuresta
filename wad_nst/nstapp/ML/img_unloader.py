from . import *


class Unloader:
    """This is a helper class to unload an image. It converts the torch.Tensor to a PIL image amd
    returns it.
    """

    def __init__(self):
        self.unloader = transforms.ToPILImage()

    def pil_img(self, tensor):
        """Function to return the image in a readable and savable image PIL format.

        Parameters
        ----------
        tensor : torch.Tensor
            Image tensor.

        Returns
        -------
        image: PIL.Image
            Unloads the image and returns it.
        """
        image = tensor.cpu().clone()
        image = image.squeeze(0)  # remove the fake batch dimension
        image = self.unloader(image)

        return image

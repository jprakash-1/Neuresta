from . import *


class ContentLoss(nn.Module):
    """Class to implement loss for content image

    Parameters
    ----------
    target : torch.Tensor
        Target on which loss is calculated.
    """

    def __init__(self, target):
        super(ContentLoss, self).__init__()
        self.target = target.detach()

    def forward(self, input):
        """Forward function

        Parameters
        ----------
        input : torch.Tensor
            Used to calculate Loss

        Returns
        -------
        input: torch.Tensor
            Returns the same input.
        """
        self.loss = F.mse_loss(input, self.target)
        return input


class StyleLoss(nn.Module):
    """Class to implement loss for style image.

    Parameters
    ----------
    input: torch.Tensor
        the input that is later reshaped.
    """

    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = self.gram_matrix(target_feature).detach()

    def gram_matrix(self, input):
        """Calculate the gram matrix.

        Parameters
        ----------
        input : torch.Tensor
            The input tensor.

        Returns
        -------
        gm: torch.Tensor
            returns the gram matrix.
        """
        a, b, c, d = input.size()
        features = input.view(a * b, c * d)
        G = torch.mm(features, features.t())

        return G.div(a * b * c * d)

    def forward(self, input):
        """Forward function

        Parameters
        ----------
        input : torch.Tensor
            Used to calculate loss

        Returns
        -------
        input: torch.Tensor
            Returns the same input.
        """
        G = self.gram_matrix(input)
        self.loss = F.mse_loss(G, self.target)
        return input


class Normalization(nn.Module):
    """Normalization helper class

    Parameters
    ----------
    mean : float
        The mean of the data.
    std: float
        The standard deviation of the data.
    """

    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        self.mean = torch.tensor(mean).view(-1, 1, 1)
        self.std = torch.tensor(std).view(-1, 1, 1)

    def forward(self, img):
        """The forward function.

        Parameters
        ----------
        img : torch.Tensor
            The input data to be normalized.

        Returns
        -------
        img: torch.Tensor
            The normalized image.
        """
        return (img - self.mean) / (self.std)


def get_style_model_and_losses(
    cnn,
    normalization_mean,
    normalization_std,
    style_img,
    content_img,
    content_layers=content_layers_default,
    style_layers=style_layers_default,
):
    """This function is used to get the style and content losses for the model.

    Parameters
    ----------
    cnn : nn.Module
        The convolutional neural network model.
    normalization_mean : float
        The mean to use for normalization.
    normalization_std : float
        The standard deviation for the normalization.
    style_img : torch.Tensor
        The style image.
    content_img : torch.Tensor
        The content image.

    Returns
    -------
    tuple
        tuple of model, style loss and content loss.
    """
    cnn = copy.deepcopy(cnn)

    normalization = Normalization(normalization_mean, normalization_std).to(device)

    content_losses = []
    style_losses = []

    model = nn.Sequential(normalization)

    i = 0
    for layer in cnn.children():
        if isinstance(layer, nn.Conv2d):
            i += 1
            name = "conv_{}".format(i)
        elif isinstance(layer, nn.ReLU):
            name = "relu_{}".format(i)
            layer = nn.ReLU(inplace=False)
        elif isinstance(layer, nn.MaxPool2d):
            name = "pool_{}".format(i)
        elif isinstance(layer, nn.BatchNorm2d):
            name = "bn_{}".format(i)
        else:
            raise RuntimeError("Unrecognized layer: {}".format(layer.__class__.__name__))

        model.add_module(name, layer)

        if name in content_layers:
            target = model(content_img).detach()
            content_loss = ContentLoss(target)
            model.add_module("content_loss_{}".format(i), content_loss)
            content_losses.append(content_loss)

        if name in style_layers:
            target_feature = model(style_img).detach()
            style_loss = StyleLoss(target_feature)
            model.add_module("style_loss_{}".format(i), style_loss)
            style_losses.append(style_loss)

    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
            break

    model = model[: (i + 1)]

    return model, style_losses, content_losses


def get_input_optimizer(input_img):
    """This function initializes and returns the optimizer.

    Parameters
    ----------
    input_img : torch.Tensor
        input image.

    Returns
    -------
    optimizer
        torch.optim
    """
    optimizer = optim.LBFGS([input_img.requires_grad_()])
    return optimizer

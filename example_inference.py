from skimage import io
import cv2
import torch, os
from PIL import Image
from briarmbg import BriaRMBG
from utilities import preprocess_image, postprocess_image
from huggingface_hub import hf_hub_download
from matplotlib import pyplot as plt

def example_inference():

    # im_path = f"{os.path.dirname(os.path.abspath(__file__))}/example_input.jpg"

    im_path = 'example_input.jpg'
    im_path = 'selfie.jpg'
    im_path = 'selfie2.png'

    net = BriaRMBG()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = BriaRMBG.from_pretrained("briaai/RMBG-1.4")
    net.to(device)
    net.eval()
    # im_g = cv2.imread(im_path)
    # print(im_g)
    # cv2.imshow('image',im_g)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    # prepare input
    model_input_size = [1024,1024]
    orig_im = io.imread(im_path)
    orig_im_size = orig_im.shape[0:2]
    image = preprocess_image(orig_im, model_input_size).to(device)

    # inference 
    result=net(image)

    # post process
    result_image = postprocess_image(result[0][0], orig_im_size)

    # save result
    pil_im = Image.fromarray(result_image)
    no_bg_image = Image.new("RGBA", pil_im.size, (0,0,0,0))
    orig_image = Image.open(im_path)
    no_bg_image.paste(orig_image, mask=pil_im)
    # no_bg_image.save("example_image_no_bg.png")
    no_bg_image.save("selfie2_image_no_bg.png")


if __name__ == "__main__":
    example_inference()
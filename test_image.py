import time

import streamlit as st
import torch
from torch.autograd import Variable
from torchvision.transforms import ToTensor, ToPILImage

from model import Generator


def test_single_image(lr_image, upscale_factor):
    TEST_MODE = False
    MODEL_NAME = 'netG_epoch_4_100.pth'

    st.image(lr_image, use_column_width=True)
    st.write('The original LR image')
    model = Generator(upscale_factor).eval()
    if TEST_MODE:
        model.cuda()
        model.load_state_dict(torch.load('epochs/' + MODEL_NAME))
    else:
        model.load_state_dict(torch.load('epochs/' + MODEL_NAME, map_location=lambda storage, loc: storage))

    image = Variable(ToTensor()(lr_image), volatile=True).unsqueeze(0)
    if TEST_MODE:
        image = image.cuda()

    start = time.clock()
    out = model(image)
    elapsed = (time.clock() - start)
    print('cost' + str(elapsed) + 's')
    out_img = ToPILImage()(out[0].data.cpu())
    st.image(out_img, use_column_width=True)
    st.write('The output SR image')

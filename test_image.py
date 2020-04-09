import time

import streamlit as st
import torch
from torch.autograd import Variable
from torchvision.transforms import ToTensor, ToPILImage

from model import Generator


def test_single_image(lr_image, upscale_factor, epoch_num):
    test_mode = False
    model_name = 'netG_epoch_{}_{}.pth'.format(upscale_factor, epoch_num)

    st.image(lr_image, use_column_width=True)
    st.write('The original LR image')
    model = Generator(upscale_factor).eval()
    if test_mode:
        model.cuda()
        model.load_state_dict(torch.load('epochs/' + model_name))
    else:
        model.load_state_dict(torch.load('epochs/' + model_name, map_location=lambda storage, loc: storage))

    image = Variable(ToTensor()(lr_image), volatile=True).unsqueeze(0)
    if test_mode:
        image = image.cuda()

    start = time.clock()
    out = model(image)
    elapsed = (time.clock() - start)
    print('cost' + str(elapsed) + 's')
    out_img = ToPILImage()(out[0].data.cpu())
    st.image(out_img, use_column_width=True)
    st.write('The output SR image')

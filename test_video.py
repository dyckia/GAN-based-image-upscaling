import argparse

import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image
from torch.autograd import Variable
from torchvision.transforms import ToTensor, ToPILImage
from tqdm import tqdm

from model import Generator


def test_single_video(video_name, upscale_factor):
    model_name = 'netG_epoch_4_100.pth'

    model = Generator(upscale_factor).eval()
    if torch.cuda.is_available():
        model = model.cuda()
    # for cpu
    model.load_state_dict(torch.load('epochs/' + model_name, map_location=lambda storage, loc: storage))
    # model.load_state_dict(torch.load('epochs/' + model_name))

    videoCapture = cv2.VideoCapture(video_name)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    frame_numbers = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    sr_video_size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH) * upscale_factor),
                     int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)) * upscale_factor)
    compared_video_size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH) * upscale_factor * 2 + 10),
                           int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)) * upscale_factor + 10 + int(
                               int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH) * upscale_factor * 2 + 10) / int(
                                   10 * int(int(
                                       videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH) * upscale_factor) // 5 + 1)) * int(
                                   int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH) * upscale_factor) // 5 - 9)))
    output_sr_name = 'out_srf_' + str(upscale_factor) + '_' + video_name.split('.')[0] + '.avi'
    output_compared_name = 'compare_srf_' + str(upscale_factor) + '_' + video_name.split('.')[0] + '.avi'
    fourcc = cv2.VideoWriter_fourcc('M', 'P', 'E', 'G')
    sr_video_writer = cv2.VideoWriter(output_sr_name, fourcc, fps, sr_video_size)
    compared_video_writer = cv2.VideoWriter(output_compared_name, fourcc, fps,
                                            compared_video_size)
    # read frame
    success, frame = videoCapture.read()
    test_bar = tqdm(range(int(frame_numbers)), desc='[processing video and saving result videos]')
    for index in test_bar:
        if success:
            image = Variable(ToTensor()(frame), volatile=True).unsqueeze(0)
            if torch.cuda.is_available():
                image = image.cuda()

            out = model(image)
            out = out.cpu()
            out_img = out.data[0].numpy()
            out_img *= 255.0
            out_img = (np.uint8(out_img)).transpose((1, 2, 0))
            # save sr video
            sr_video_writer.write(out_img)

            # make compared video and crop shot of left top\right top\center\left bottom\right bottom
            out_img = ToPILImage()(out_img)
            crop_out_imgs = transforms.FiveCrop(size=out_img.width // 5 - 9)(out_img)
            crop_out_imgs = [np.asarray(transforms.Pad(padding=(10, 5, 0, 0))(img)) for img in crop_out_imgs]
            out_img = transforms.Pad(padding=(5, 0, 0, 5))(out_img)
            compared_img = transforms.Resize(size=(sr_video_size[1], sr_video_size[0]), interpolation=Image.BICUBIC)(
                ToPILImage()(frame))
            crop_compared_imgs = transforms.FiveCrop(size=compared_img.width // 5 - 9)(compared_img)
            crop_compared_imgs = [np.asarray(transforms.Pad(padding=(0, 5, 10, 0))(img)) for img in crop_compared_imgs]
            compared_img = transforms.Pad(padding=(0, 0, 5, 5))(compared_img)
            # concatenate all the pictures to one single picture
            top_image = np.concatenate((np.asarray(compared_img), np.asarray(out_img)), axis=1)
            bottom_image = np.concatenate(crop_compared_imgs + crop_out_imgs, axis=1)
            bottom_image = np.asarray(transforms.Resize(
                size=(int(top_image.shape[1] / bottom_image.shape[1] * bottom_image.shape[0]), top_image.shape[1]))(
                ToPILImage()(bottom_image)))
            final_image = np.concatenate((top_image, bottom_image))
            # save compared video
            compared_video_writer.write(final_image)
            # next frame
            success, frame = videoCapture.read()

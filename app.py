import os
from os import listdir
from os.path import join
import random
import urllib

import streamlit as st
from PIL import Image

from data_utils import is_image_file
from test_benchmark import test_benchmark
from test_image import test_single_image

# Streamlit encourages well-structured code, like starting execution in a main() function.
# from test_video import test_single_video


def get_display_name(image_path):
    image_name = os.path.split(image_path)[1]
    psnr = "psnr"
    ssim = "ssim"
    psnr_pos = image_name.find(psnr)
    ssim_pos = image_name.find(ssim)
    return image_name[:psnr_pos-1] + " with PSNR=" + image_name[psnr_pos+5:ssim_pos-1] + \
        " and SSIM=" + image_name[ssim_pos+5:-4]


def main():
    # Render the readme as markdown using st.markdown.
    readme_text = st.markdown(get_file_content_as_string("instructions.md"))

    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose the app mode",
                                    ["Process Single Image", "Show Benchmark Datasets", "Process Single Video"])
    upscale_factor = st.sidebar.selectbox('Please select an upscale factor', (2, 4, 8))
    epoch_num = st.sidebar.slider('Choose the epoch number of the model', 90, 100, 100)
    if app_mode == "Show Benchmark Datasets":
        st.header("Benchmark Results")
        st.subheader('Statistical Data at {}x upscale factor'.format(upscale_factor))

        readme_text.empty()
        data_frame = test_benchmark(upscale_factor, epoch_num)

        st.dataframe(data_frame)
        out_path = 'benchmark_results/SRF_' + str(upscale_factor) + '/'
        image_filenames = [join(out_path, x) for x in listdir(out_path) if is_image_file(x)]
        result_images = random.sample(image_filenames, 4)
        st.subheader('Randomly selected test results (scaled at {}x)'.format(upscale_factor))
        st.markdown("> **Left:** Low-res Image, **Mid:** Ground Truth, **Right:** Super-res Image")
        st.markdown("")
        for index, result_image in enumerate(result_images):
            st.markdown("- " + get_display_name(result_image))
            st.image(result_image, use_column_width=True)
        st.markdown('#### PSNR:Peak Signal-to-Noise Ratio ')
        st.markdown('#### SSIM:Structural Similarity Index ')

    elif app_mode == "Process Single Image":
        st.subheader("Process Single Image")

        readme_text.empty()
        uploaded_file = st.file_uploader("Upload a low resolution image", type=['png', 'jpg'])

        if uploaded_file is not None:
            lr_image = Image.open(uploaded_file)
            st.text("Your Uploaded Image")
            st.image(lr_image)

            if st.button('Generate'):
                test_single_image(lr_image, upscale_factor, epoch_num)

    elif app_mode == "Process Single Video":
        st.subheader("Process Single Video")

        readme_text.empty()
        st.info("Feature coming soon!")
        # video_name = 'VC.mp4'
        # video_file = open(video_name, 'rb')
        # video_bytes = video_file.read()
        # st.video(video_bytes)
        # st.text("Original Video")
        #
        # test_single_video(video_name, upscale_factor)
        #
        # output_sr_name = 'out_srf_' + str(upscale_factor) + '_' + video_name.split('.')[0] + '.mp4'
        # output_sr_video = open(output_sr_name, 'rb')
        # output_sr_bytes = output_sr_video.read()
        # st.video(output_sr_bytes)
        # st.text("The output SR Video")
        #
        # output_compared_name = 'compare_srf_' + str(upscale_factor) + '_' + video_name.split('.')[0] + '.mp4'
        # output_compared_video = open(output_compared_name, 'rb')
        # output_compared_bytes = output_compared_video.read()
        # st.video(output_compared_bytes)
        # st.text("The output compared Video")


# Download a single file and make its content available as a string.
@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/ENGI9805-COMPUTER-VISION/Term-Project/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")


if __name__ == "__main__":
    main()

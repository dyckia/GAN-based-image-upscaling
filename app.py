import time
import urllib

import streamlit as st
import torch
from PIL import Image
from torch.autograd import Variable
from torchvision.transforms import ToTensor, ToPILImage

from model import Generator


# Streamlit encourages well-structured code, like starting execution in a main() function.
def main():
    # Render the readme as markdown using st.markdown.
    readme_text = st.markdown(get_file_content_as_string("instructions.md"))

    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose the app mode",
                                    ["Test Benchmark Datasets", "Test Single Image", "Test Single Video"])
    upscale_factor = st.sidebar.selectbox('Please give the upscale factor', (2, 4, 8))
    if app_mode == "Test Benchmark Datasets":
        st.subheader("Test Benchmark Datasets")

        readme_text.empty()
        st.code(get_file_content_as_string("app.py"))
    elif app_mode == "Test Single Image":
        st.subheader("Test Single Image")

        readme_text.empty()
        uploaded_file = st.file_uploader("Upload a LR image", type=['png', 'jpg'])

        if uploaded_file is not None:
            lr_image = Image.open(uploaded_file)
            st.text("Original Image")
            st.image(lr_image)

            if st.button('SR it!'):
                test_single_image(lr_image, upscale_factor)

    elif app_mode == "Test Single Video":
        st.subheader("Test Single Video")

        readme_text.empty()


# This is the main app app itself, which appears when the user selects "Run the app".
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


# Download a single file and make its content available as a string.
@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/ENGI9805-COMPUTER-VISION/Term-Project/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")


if __name__ == "__main__":
    main()

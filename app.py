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
                                    ["Show instructions", "Run the app", "Show the source code"])
    if app_mode == "Show instructions":
        st.sidebar.success('To continue select "Run the app".')
    elif app_mode == "Show the source code":
        readme_text.empty()
        st.code(get_file_content_as_string("app.py"))
    elif app_mode == "Run the app":
        readme_text.empty()
        run_the_app()


# This is the main app app itself, which appears when the user selects "Run the app".
def run_the_app():
    UPSCALE_FACTOR = st.sidebar.selectbox('Please give the upscale factor', (2, 4, 8))
    TEST_MODE = False
    IMAGE_NAME = 'BSD100_007.png'
    MODEL_NAME = 'netG_epoch_4_100.pth'

    st.image(IMAGE_NAME, use_column_width=True)
    st.write('The original LR image')
    model = Generator(UPSCALE_FACTOR).eval()
    if TEST_MODE:
        model.cuda()
        model.load_state_dict(torch.load('epochs/' + MODEL_NAME))
    else:
        model.load_state_dict(torch.load('epochs/' + MODEL_NAME, map_location=lambda storage, loc: storage))

    image = Image.open(IMAGE_NAME)
    image = Variable(ToTensor()(image), volatile=True).unsqueeze(0)
    if TEST_MODE:
        image = image.cuda()

    start = time.clock()
    out = model(image)
    elapsed = (time.clock() - start)
    print('cost' + str(elapsed) + 's')
    out_img = ToPILImage()(out[0].data.cpu())
    out_img_name = 'out_srf_' + str(UPSCALE_FACTOR) + '_' + IMAGE_NAME
    out_img.save(out_img_name)
    st.image(out_img_name, use_column_width=True)
    st.write('The output SR image')


# Download a single file and make its content available as a string.
@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/streamlit/demo-self-driving/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")


if __name__ == "__main__":
    main()

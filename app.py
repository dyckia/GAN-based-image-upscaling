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
        test_benchmark(upscale_factor)

        out_path = 'benchmark_results/SRF_' + str(upscale_factor) + '/'
        image_filenames = [join(out_path, x) for x in listdir(out_path) if is_image_file(x)]
        result_images = random.sample(image_filenames, 4)
        for index, result_image in enumerate(result_images):
            st.image(result_image, use_column_width=True)
            st.write('Sample result {}'.format(index))

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
        st.info("Feature coming soon!")


# Download a single file and make its content available as a string.
@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/ENGI9805-COMPUTER-VISION/Term-Project/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")


if __name__ == "__main__":
    main()

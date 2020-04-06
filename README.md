# Term-Project
A web app for SRGAN

## Installation

Clone the report

```
git clone git@github.com:ENGI9805-COMPUTER-VISION/Term-Project.git
```

cd into the project root folder
```
cd Term-Project
```

### Create virtual environment

```
conda create -n srgan_env python=3.7.6
```

and activate environment

```
activate srgan_env
```

Then you need to install the project dependencies

```
pip install -r requirements.txt
```

## Usage

Run the app
```
streamlit run app.py
```

### Available models

- [x] netG epoch 100 upscale factor 2
- [x] netG epoch 100 upscale factor 4
- [x] netG epoch 100 upscale factor 8

## Checklist

- [x] Machine learning resource management
- [x] Data ingestion and collection
- [x] Machine learning training
- [x] Integrating trained model with web app
- [ ] Process Single Video(Ian)
- [x] Add statistic terms definition
- [ ] Deploying the web app on cloud hosting platform
- [ ] Writing project report
    - [ ] introduction
    - [ ] problem definition
    - [ ] proposed solution(Ian)
    - [ ] results and discussion
    - [ ] conclusion
- [ ] Writing presentation slides
- [ ] Recording project presentation

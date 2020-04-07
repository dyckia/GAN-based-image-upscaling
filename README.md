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
conda create -n srgan_env python=3.6.8
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

## Work Log

- [ ] **Build the program**
    - [x] Machine learning resource management
    - [x] Data ingestion and collection (Jason)
    - [x] Model training (Jason, Luo)
    - [x] Integrating trained model with web app
    - [ ] Process Single Video (Ian)
    - [x] Add statistic terms definition
    - [ ] Fix png file alpha channel bug
    - [ ] Fix Show Benchmark Datasets bug
    - [ ] Refactor code and add comments
- [x] **Deploying working demo on cloud hosting platform**
    - [ ] Add startup file (Jason)
    - [ ] Inject necessary dependencies (Jason)
    - [ ] Fix deployment error (Jason)
- [ ] **Write project report**
    - [ ] introduction (Jason)
    - [ ] problem definition (Luo)
    - [ ] proposed solution (Ian)
    - [ ] results and discussion
    - [ ] conclusion
- [ ] **Write presentation slides**
- [ ] **Record presentation video**

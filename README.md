# Title
This product is for ...

### Table of Contents
- [Prerequisites](#prerequisites)
- [Architecture](#architecture)
- [Features](#features)
- [Demo](#demo)
- [Reports](#reports)
- [Installation](#installation)
- [File Structure](#file-structure)
- [Version Control System](#version-control-system)
- [Upcoming](#upcoming)
- [Documentations](#documentations)
- [License](#license)
- [Links](#links)
- [Team](#team)
- [Contact](#contact)
- [Resources](#resources)
- [Citation](#citation)

###### Github Action Test 2

### Prerequisites
- Python 3.10
- Nvidia T4 GPU or higher
- Microsoft SQL
- Llama 2
- Whisper 

### Architecture
![Architecture](docs/img/Image.gif)

### Features
- [x] ................
- [x] ................
- [x] ................


### Demo
[Video](videoURL)
[![Video](önizlemeGörseliURLsi)](videoURL)
![GIF](draft.gif)

### Reports
![Report](Report.jpg)

### Installation
*__for Linux/Ubuntu__*
- Do the following operations in order.

#### 1. Install Nvidia Drivers
- System Update & Upgrade
```bash
sudo apt update
```
```bash
sudo apt upgrade
```
- Install Nvidia Drivers
```bash
sudo apt install ubuntu-drivers-common 
```
```bash
ubuntu-drivers devices
```
```bash
sudo ubuntu-drivers autoinstall
```
- System Reboot
```bash
sudo reboot
```
- Check Nvidia Driver and Note CUDA Version
```bash
nvidia-smi
```
- *__Note:__* Yukarıdaki adımda hem Nvidia Driver'ın yüklenip yüklenmediğini kontrol edin. 
Hem de yüklemeniz gereken CUDA versiyonunu öğreninin.

### 2. Install CUDA 12.2 for Ubuntu 22.04
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
```
```bash
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
```
```bash
wget https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda-repo-ubuntu2204-12-2-local_12.2.0-535.54.03-1_amd64.deb
```
```bash
sudo dpkg -i cuda-repo-ubuntu2204-12-2-local_12.2.0-535.54.03-1_amd64.deb
```
```bash
sudo cp /var/cuda-repo-ubuntu2204-12-2-local/cuda-*-keyring.gpg /usr/share/keyrings/
```
```bash
sudo apt-get update
```
```bash
sudo apt-get -y install cuda
```
```bash
sudo find / -name nvcc
```
```bash
echo 'export PATH=/usr/local/cuda-12.3/bin:$PATH' >> ~/.bashrc
```
```bash
source ~/.bashrc
```
```bash
nvcc --version
```
---

#### 3. Python 3.10.0 Installation
```bash
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget
```
```bash
sudo apt-get install libbz2-dev
```
```bash
sudo apt-get install libgdbm-compat-dev
```
```bash
sudo apt-get install liblzma-dev
```
```bash
sudo apt-get install tk-dev
```
```bash
sudo apt-get install uuid-dev
```
```bash
sudo apt-get install zlib1g-dev
```
```bash
wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tar.xz
```
```bash
tar -xf Python-3.10.0.tar.xz
```
```bash
cd Python-3.10.0
```
```bash
./configure --enable-optimizations --prefix=/usr/local
```
```bash
make -j $(nproc)
```
```bash
sudo make altinstall
```
---

##### 4. Get Repository
- Clone Repository
```bash
git clone https://github.com/organization_name/repo_name
```

- Navigate to the project directory:
```bash
cd Repository_Directory
```

- Create Virtual Environment named `.venv`
```bash
python3.10 -m venv .venv
```

- Activate virtual environment
```bash
source .venv/bin/activate
```
---

#### 5. Install Pytorch
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu122
```
- *__Note:__* Lütfen farklı CUDA verdiyonu kullanıyorsanız Pytorch versiyonunuzu değiştirin.

#### 6. Download Llama and Install 
- Visit the `https://ai.meta.com/llama/` and get download link for Llama 2

```bash
git clone https://github.com/facebookresearch/llama.git
```
```bash
cd llama
```
```bash
pip install -e .
```
```bash
chmod +x download.sh
```
```bash
./download.sh
```

- *__Note__*: If you get the error `"The file is already fully retrieved; nothing to do."`, delete the `--continue` commands in the `download.sh` file and try again.
Related issue link: `https://github.com/facebookresearch/llama/issues/760`
---

#### 7. Install Requirements for Audio Process
```bash
sudo apt-get install unixodbc-dev
```
```bash
pip install Cython
```
```bash
pip install -r requirements/requirements_audio.txt
```
---

#### 8. Install Requirements for Architecture
```bash
pip install -r requirements/requirements_arctitecture.txt
```
---

#### 9. Install ODBC Driver 18

```bash
curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
```
```bash
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
```
```bash
sudo apt-get update
```
```bash
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```
---

#### 10. Install FFmpeg
```bash
sudo apt install ffmpeg
```
---

#### 11. Install Linux Services
```bash
sudo cp /home/azureuser/directory/services/audio.service /etc/systemd/system/
```
```bash
sudo cp /home/azureuser/directory/services/text.service /etc/systemd/system/
```
```bash
sudo systemctl daemon-reload
```
```bash
sudo systemctl enable audio.service
```
```bash
sudo systemctl enable text.service
```
```bash
sudo systemctl start audio.service
```
```bash
sudo systemctl start text.service
```
```bash
sudo systemctl status audio.service
```
```bash
sudo systemctl status text.service
```
---

### File Structure

```text
.
├── README.md
├── TODO.md
├── app.py
├── examples
│         ├── example_1.wav
│         ├── example_2.wav
├── flagged
├── gradio_app.py
├── outputs
│         ├── example_1.json
├── requirements.txt
└── test.py
```
---

### Version Control System
#### Releases
- [v0.1](https://github.com/organization_name/repo_name/archive/refs/tags/v0.1.zip) #.zip
- [v0.1](https://github.com/organization_name/repo_name/archive/refs/tags/v0.1.tar.gz) #.tar.gz
#### Branches
- [BranchName](https://github.com/organization_name/repo_name/tree/Stream)

#### Related Repos
- [RepoName](https://github.com/organization_name/repo_name)
---

### Upcoming
- [ ] ....
---

### Documentations
#### Turkish Readme
- [README_TR](docs/README_TR.md)
---

#### TO DO list
- [TODO](TODO.md)
---

#### Contributing Guidence
- [Contribute](CONTRIBUTE.md)

### License
- [LICENSE](LICENSE)
---

### Links
- [Github](https://github.com/repo)
- [Website](https://company_name.com/en)
- [Linkedin](https://www.linkedin.com/company/company_name/)
---

### Team
- [Bunyamin Ergen](https://www.linkedin.com/in/bunyaminergen)
---

### Contact
- [Mail](mailto:info@example.com)
---

### Resources
- [Resources](RESOURCES.md)
---

### Citation
- Reference to cite if you use this work in a paper or research project:
``` text
@software{software_2024,
author = {Ergen},
doi = {00.0000/zenodo.0000},
month = {01},
title = {{software_2024}},
url = {https://github.com/repo_name},
year = {2024}
}
```

---
---

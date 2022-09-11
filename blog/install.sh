wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -P ~/
bash ~/Miniconda3-latest-Linux-x86_64.sh -b -p ~/mayaenv
rm ~/Miniconda3-latest-Linux-x86_64.sh*
source ~/mayaenv/bin/activate
pip install -r ~/mayablog/blog/requirements.txt
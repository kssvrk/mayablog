wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -P ~/
bash ~/Miniconda3-latest-Linux-x86_64.sh -b -p ~/mayaenv
rm ~/Miniconda3-latest-Linux-x86_64.sh*
source ~/mayaenv/bin/activate
conda install -y -c anaconda nginx
conda install -c conda-forge certbot-nginx
cp id_ed25519* ~/.ssh/
sudo yum -y install git || echo "Unable to install git"
git clone git@github.com:kssvrk/mayablog ~/mayablog
pip install -r ~/mayablog/blog/requirements.txt
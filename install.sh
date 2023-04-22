 #!/bin/bash
bash ./miniconda.sh -b -p $HOME/miniconda;
source $HOME/miniconda/bin/activate;
which python;which conda;
pip install -r requirements.txt
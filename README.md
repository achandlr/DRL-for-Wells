First time setup: run
```
source firstTimeSetup.sh
```

---

To train the agent on the environment in the `env` folder:
```
python train.py
```

---

To visualize the output:
```
python visualize.py
```

Explanation of files:

* bests/ - the best model in a training session
* checker.py - checks to see if an env is valid
* clogs - condor logs, unused atm
* cps - checkpoint files in a training session, gitignore'd
* cpu - condor submit file
* CustomEvalCallback.py - callback that allows for bests/ to happen
* Data - ???
* env - environment folder
* evaluate2.py - a working evaluate
* evaluate.py - a not working evaluate
* *.zip - out files from training (model)
* firstTimeSetup.sh - a first time setup (read the file first)
* gpu - condor submit file
* gpu.sh - script for use with condor submit file
* gym-field-old - old environment
* gym_oilfield - ???
* logs - logs for training
* mlcpu.yml - conda env for machines with no gpu
* ml.yml - conda env for machines with gpu
* Data.ipynb - ???
* play.py - play the env!
* __pycache__
* README.md
* recordings/ - where recordings are stored
* requirements.txt - not sure if used
* resume.py - resume training
* tensey/ - tenserboard output folder, gitignored
* tmp.py - ???
* train.py - train the model
* video.py - exports a video
* visualize.py - exports a run in text format, with an enter press req'd between prints

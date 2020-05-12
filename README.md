# Explanation of files:

```Data/ : Contains sample data for use with generation.
GraphAlgo/ : Contains graph algorithm code.
GraphAlgo/src/algo/Main.java : Runs the graph algorithm code
agent/ : Contains agent and environment code.
ml.yml : Contains necessary conda config.

agent/bests/ : Contains best recorded agents.

agent/env/ : Contains 2D testing env.
agent/env/field_env.py : General environment. Contains structure for agent to run on. 
agent/env/Field2D.py : A 2-dimensional oil field. Has a rock class that defines properties of rocks and how they work when drilled. 
agent/env/world.py : Reads in a text file version of the world and formats an array version of the file.
agent/env/world.txt : the text version of an oil field. world.py reads this file in.

agent/gym_oilfield/ : Contains main 3D environment code.
agent/gym_oilfield/oilfield_env.py : Environment that most of the testing utilizes. This file calculates rewards, moves the drill, counts steps etc. 
agent/gym_oilfield/OilField3D : Similar to Field2D.py. Adds in functionality for a third dimension. Has an updated rock class and methods to retrieve individual rocks in a three-dimensional field. 
agent/gym_oilfield/readData.py : Reads in our created data and uses it to populate the oil well with values.
agent/gym_oilfield/Sample_Rendering.ipynb : Renders a visualization of the well and the drill's current position by showing how liquid values change with time.
agent/gym_oilfield/smallStructure : The fake data we created to populate the oil field.

agent/CustomEvalCallback.py : Contains the code to save the best model.
agent/agent.py : The starter point for training the agent. Supports training, resuming training, visualizing, and evaluating models.
agent/model.py : The model used behind the scenes, a subclass of a stable-baselines class.
agent/checker.py : Ensures the environment the agent is running on is compatible with Open AI Gym guidelines.
agent/setup.sh : Creates a directory to store the agent's best results.
agent/play.sh : Allows you to "play" an environment.```

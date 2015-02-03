# PyAvida Readme

_Current Version 0.1_

_Copyright 2015, Arthur W. Covert III_

PyAvida is a set of python packages designed to run experiments on populations of "digital organisms." Digital organisms are self-replicating computer programs written in a simplified assembly language. Historically, the C++ project, Avida, has been the leading platform for research on digital organisms. PyAvida provides the simplified instruction set and tools to run an Avida-like experiment.

Currently, I am targeting development at python 2.7.x and the PyPy just-in-yime compiler. PyAvida will run with the standard python interpreter, but it will be very slow for larger population sizes. Those wishing to work with large populations (simulating more than ~3,000-4,000 digital organisms) should use PyPy to run their experiments.

PyAvida, at this stage, is more of an educational platform, intended to give students a sandbox to try out new ideas for digital evolution experiments. I hope to continue developing it into a more sophisticated research tool for wider applications.

The Basic-Architecture provides everything a user needs to do simple experiments. Users may easily extend or add additional components to do more complex experiments. For example, you could extend Populations.BasicPopulation to support multiple sub-populations connected by migration. An example experiment resides in the Lenski_et_al_2003_control.py file. Make sure to add the PyAvida project root to your PYTHONPATH environment variable.

The Basic-Architecture is focused primarily on running efficiently, while still being extensible. No code changes that slow down the Basic-Architecture will be accepted. 


## Development Roadmap

### Version 0.1 (current)
*All of the basic tools you need to do an experiment similar to the Lenski et al 2003 paper are present.

*Some bugs still exist, in particular, the scheduler is limited to exactly 10,000 organisms. A refactor is being tested and will be pushed soon.

*This release is primarily a proof-of-concept to show that it is possible to do these types of experiments with a python-based project.


### Version 0.2 
*Bugfixes, bugfixes, bugfixes.

*Implement unit testing and testing framework for all components of the Basic-Architecture.

*Implement regression testing for more complex experiments.

### Version 0.3
*Implement additional observers for experiments.

*Implement all Mutation hooks (copy mutations, insertions, deletions, slip mutations).

*Re-profile the code and eliminate as many performance drains in the basic instruction set as possible.

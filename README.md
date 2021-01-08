# Virtual ISL Interpreter

Our project is a complete system to convert text in English into animated ISL translation. This page gives instructions on how to use it in a demo app with an avatar available for signing the ISL output

## Contents

The project contains two main components, the animation assets and script, and the translation code, along with a demo app. 

The animation portion has 50 demo animations with expressions to be used with the demo. Additional 250 signs with expressions, as well as 1000 signs without expressions are also available (see *Additional Data* below)

One avatar, Sanket, is also available to be used with the signs for output

![Alt text](docs/img/avatar_Sanket.jpeg?raw=true "Sanket")

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

This project is mainly built using: 
* python 3 for scripts
* [Unity](https://store.unity.com/download) to display the animations
Ensure both are installed in the system.

Additionally, this project needs the following python packages: 
* [spaCy](https://spacy.io/usage) with 
  * en_core_web_sm model (https://spacy.io/usage/models) 
* [nltk](https://www.nltk.org/install.html) with
  * WordNet data (www.nltk.org/nltk_data/)

Also, to work with the GUI demo app, you will need tkinter (automatically installed in python ver>=3.7)

### Usage

A step by step series of examples that tell you how to get the components of the project running

Using the translation code standalone
```
spacy_rules.py -t <English text>
```

Alternatively, to run with the executable animation demo: 
* first download the islexe.zip from Releases
* extract the contents to a suitable folder
* clone the src folder in a separate location
* run the isl.exe file in the islexe extracted folder
* run the gui_demo.py using the command `python gui_demo.py`
* enter English text in the box available and click Go
* the output animation should play on the isl.exe app

### Working With Actual Animations

Please refer to [Working with Animations in Unity](docs/Working-with-Unity.md) for detailed information on how to set up the Unity project to work with the animations for editing and adding new animations


## Additional Data

Additional data of 1000 basic animations as well as 250 animations with expressions are available on request

## Contributing

Please read [CONTRIBUTING.md](TODO) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Shyam Krishna** - *Translation* - https://github.com/shyamkrishna
* **Mahesh** - *Unity Game Engine & Animation* - https://github.com/kiddowhy
* **Rahul** - *Animation* - TODO


See also the list of [contributors](TODO) who participated in this project.

## License

This project is licensed under the TODO License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This work was made possible by a CSR grant from Mphasis
* TODO?


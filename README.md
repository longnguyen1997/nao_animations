# NAO Animations
This project, done with the permission of the [Electronics and Telecommunications Research Institute of Korea](http://etri.re.kr/), seeks to generate intelligent, adaptive behavioral gestures in the Aldebaran NAO robot. 

# Overview
Recent developments in machine learning, natural language processing, and computer vision have spurred research in intelligent robotics. We aim to make robots more believable in their behavior, and in working with NAO, we hope to generate synchronous, distinct body language taken not from a predetermined set of gestures, but adapted and learned methodically from sensor data and textual analysis.

## Methods
Working with `anaconda (4.4.0), python 2.7.13 (32-bit)`, we utilize several libraries such as `spacy`, `seaborn`, `naoqi`, and `scikit-learn`. Speech analysis is done in `spacy`, a robust NLP library with significant performance advantages over other popular libraries such as `nltk`. `scikit-learn` is the base for all machine learning tasks. Data is taken from NAO's joint sensors and viewed with `seaborn`, then extrapolated through uniform random, but statistically significant values to generate new motions.

All scripts are specced accordingly (by functions and operations) and are best viewed in `pycharm` for documentation purposes.

## Phases
### Textual classification
This was done by training a multilayer perceptron model (default parameters provided in `scikit-learn`) with 9 classification groups corresponding to types of messages that NAO can say; for example, `happy`, `disappointed`, `telling`, etcetera. Inputs were fed by the user into a console prompt that then used the model and `spacy`'s vector representation of the input to classify it. After classification, one gesture from the corresponding Aldebaran library is performed concurrently as NAO speaks the message.
### Collecting joint sensor data
With the `naoqi` library published by Aldebaran, reports were collected and parsed from string format to readable Python data from NAO's joint sensors. Angles specified were in radians. Thus far, only a mix of data has been used to extrapolate new animations. Sequential time series analysis is yet to be done.
### Motion generation
Motion generation is done by sampling a point within the mean of a dataset (in this case, joint sensor data), plus/minus one standard deviation. This is a naive way to ensure accurate generation while allowing some freedom for natural deviations. Transitions between gestures are currently not as smooth as they should be.

## References
Some useful papers resourced for the project include, but are not limited to, the following:

* [Model of expressive gestures for humanoid robot NAO](http://pages.isir.upmc.fr/~achard/GdR/p2.pdf)
* [Gesture generation with low-dimensional embeddings](http://ict.usc.edu/pubs/Gesture%20generation%20with%20low-dimensional%20embeddings.pdf).
 

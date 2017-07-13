[TOC]


# NAO Animations
This project, done with the permission of the [Electronics and Telecommunications Research Institute of Korea](http://etri.re.kr/), seeks to generate intelligent, adaptive behavioral gestures in the [Aldebaran NAO robot](https://www.ald.softbankrobotics.com/en/cool-robots/nao). 

# Overview
Recent developments in machine learning, natural language processing, and computer vision have spurred research in intelligent robotics. We aim to make robots more believable in their behavior, and in working with NAO, we hope to generate synchronous, distinct body language taken not from a predetermined set of gestures, but adapted and learned methodically from sensor data and textual analysis.

## Methods
Working with `anaconda (4.4.0), python 2.7.13 (32-bit)`, we utilize several libraries such as `spacy`, `seaborn`, `naoqi`, and `scikit-learn`. Speech analysis is done in `spacy`, a robust NLP library with significant performance advantages over other popular libraries such as `nltk`. `scikit-learn` is the base for all machine learning tasks. Data is taken from NAO's joint sensors and viewed with `seaborn`, then extrapolated through uniform random, but statistically significant values to generate new motions.

All scripts are specced accordingly (by functions and operations) and are best viewed in `pycharm` for documentation purposes.

## Usage
Let's take a look at the file `motion_analyzer.py`.

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
 


### MathJax

You can render *LaTeX* mathematical expressions using **MathJax**, as on [math.stackexchange.com][1]:

The *Gamma function* satisfying $\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$ is via the Euler integral

$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
$$

> **Tip:** To make sure mathematical expressions are rendered properly on your website, include **MathJax** into your template:

```
<script type="text/javascript" src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>
```

> **Note:** You can find more information about **LaTeX** mathematical expressions [here][4].


### UML diagrams

You can also render sequence diagrams like this:

```sequence
Alice->Bob: Hello Bob, how are you?
Note right of Bob: Bob thinks
Bob-->Alice: I am good thanks!
```

And flow charts like this:

```flow
st=>start: Start
e=>end
op=>operation: My Operation
cond=>condition: Yes or No?

st->op->cond
cond(yes)->e
cond(no)->op
```

> **Note:** You can find more information:

> - about **Sequence diagrams** syntax [here][7],
> - about **Flow charts** syntax [here][8].

### Support StackEdit

[![](https://cdn.monetizejs.com/resources/button-32.png)](https://monetizejs.com/authorize?client_id=ESTHdCYOi18iLhhO&summary=true)

  [^stackedit]: [StackEdit](https://stackedit.io/) is a full-featured, open-source Markdown editor based on PageDown, the Markdown library used by Stack Overflow and the other Stack Exchange sites.


  [1]: http://math.stackexchange.com/
  [2]: http://daringfireball.net/projects/markdown/syntax "Markdown"
  [3]: https://github.com/jmcmanus/pagedown-extra "Pagedown Extra"
  [4]: http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference
  [5]: https://code.google.com/p/google-code-prettify/
  [6]: http://highlightjs.org/
  [7]: http://bramp.github.io/js-sequence-diagrams/
  [8]: http://adrai.github.io/flowchart.js/

from pickle import dump

tags = ['no', 'yes']

corpus = {tag: [] for tag in tags}

no1 = "No, I don't agree with you."
no2 = "No, that's not the right way to go."
no3 = "I don't think so."
no4 = "I think that's a bad way to go."
no5 = "No."
no6 = "That's not right."
no7 = "I really don't know."

corpus['no'].extend([globals()[k] for k in globals().keys() if 'no' in k])

yes1 = "Yeah, I completely agree."
yes2 = "Yes, that's right."
yes3 = "Yeah, you're right."
yes4 = "I think you are correct."
yes5 = "Yes."
yes6 = "That's correctly accurate."
yes7 = "You are probably right, yeah."

corpus['yes'].extend([globals()[k] for k in globals().keys() if 'yes' in k])

dump(corpus, open('pickles/speech_corpus', 'wb'))
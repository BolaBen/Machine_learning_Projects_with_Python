# Simple Support Vector Machine (SVM) example with character recognition

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()

print(len(digits.data)) # digits.data is the actual data (features).

print(len(digits.target)) #digits.target is the label we've assigned to the data

# specifying the classifier

# default from library
# clf = svm.SVC()

# tweaking the classifier by setting gamma & C parameters
clf = svm.SVC(gamma=0.0001, C=100)

# assigning data(digits) into X(uppercase) & y variables
# loaded all data(for both X & y except for the last 10 data points)
X,y = digits.data[:-10], digits.target[:-10]

# training the data
clf.fit(X,y)

# testing the data(predicting the fifth from the
# last element of our data(digits)
print(clf.predict([digits.data[-5]]))

# visualising the predicted result
plt.imshow(digits.images[-1], cmap=plt.cm.gray_r, interpolation='nearest')
plt.show()



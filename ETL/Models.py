import itertools
import os
import pickle
import pandas as pd
#import graphviz
import matplotlib.pyplot as plt
import numpy as np
import sklearn.tree as tree
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, ExtraTreesClassifier, \
    AdaBoostClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import learning_curve, cross_val_score
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier

CHOICES_DICT = {
    'Trees': ['Classification', 'Extra-Classification', 'Random Forest'],
        'Bayes': ['Multinomial', 'Bernoulli', 'Gaussian'],
        'Ada': ['Classification'],
        'Trees': ['Classification', 'Extra-Classification', 'Random Forest'],
        'Gradient': ['Booster', 'Stochastic'],
        'Neightbors': ['K', 'Radius'],
        'SVM': ['Classification', 'Nu-Classification', 'Linear Classification'],
        'Neural Network': ['MLP'],
        'Gaussian': ['Gaussian Classifier']
}


class Models:
    """
    Class that will have all the Machine Learning models that the application will use.
    """

    def __init__(self, x_train=None, y_train=None, x_test=None, y_test=None):
        """
        Class Constructor.
        """
        self.__model = None
        self.__x_train = x_train
        self.__x_test = x_test
        self.__y_train = y_train
        self.__y_test = y_test
        self.__confussion_matrix = None

    def train(self, key1, key2):
        if key1 == 'Bayes':
            if key2 == 'Multinomial':
                self.naive_bayes_multinomial()
            elif key2 == 'Bernoulli':
                self.naive_bayes_bernoulli()
            elif key2 == 'Gaussian':
                self.naive_bayes_gaussian()

        elif key1 == 'Ada':
            if key2 == 'Classification':
                self.ada_classifier()

        elif key1 == 'Trees':
            if key2 == 'Classification':
                self.tree_decision_classifier()
            elif key2 == 'Extra-Classification':
                self.tree_extra_tree_classifier()
            elif key2 == 'Random Forest':
                self.tree_random_forest()

        elif key1 == 'Gradient':
            if key2 == 'Booster':
                self.gradient_booster()
            elif key2 == 'Stochastic':
                self.gradient_stochastic_descent()

        elif key1 == 'Neightbors':
            if key2 == 'K':
                self.k_neighbors_classifier()
            elif key2 == 'Radius':
                self.r_neighbors_classifier()

        elif key1 == 'SVM':
            if key2 == 'Classification':
                self.svm_support_vector_classification()
            elif key2 == 'Nu-Classification':
                self.svm_support_vector_nu_classification()
            elif key2 == 'Linear Classification':
                self.svm_support_vector_linear_classification()

        elif key1 == 'Neural Network':
            if key2 == 'MLP':
                self.neural_sklearn_mlp()
            elif key2 == 'CNN':
                self.keras_sequential_model()

        elif key1 == 'Gaussian':
            if key2 == 'Gaussian Classifier':
                self.gaussian_process_classifier()

    def naive_bayes_multinomial(self, alpha=1.0, fit_prior=True):
        """
        Multinomial naive bayes model from sklearn
        :param alpha: Smoothing parameter, 0 for no smoothing.
        :param fit_prior: Whether to learn class prior probabilities or not.
        :return: probability, conf_matrix
        """
        model = MultinomialNB(alpha=alpha, fit_prior=fit_prior)
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def naive_bayes_bernoulli(self, alpha=1.0, fit_prior=True):
        """
        Naive Bayes classifier for multivariate Bernoulli models. MUST USE WITH TO_ARRAY!!

        :param alpha: Smoothing parameter, 0 for no smoothing.
        :param fit_prior: Whether to learn class prior probabilities or not.
        :return: probability, conf_matrix
        """
        model = BernoulliNB(alpha=alpha, fit_prior=fit_prior)
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def naive_bayes_gaussian(self):
        """
        Naive Bayes classifier for multivariate Gaussian models.
        :return: probability, conf_matrix
        """
        model = GaussianNB()
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def ada_classifier(self):
        model = AdaBoostClassifier()
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def tree_decision_classifier(self, criterion='gini', splitter='best', max_depth=None, min_samples_split=2,
                                 min_samples_leaf=1, min_weight_fraction_leaf=0., max_features=None, random_state=None):
        """
        Decision tree classifier
        :param criterion: Measurement of the quality of a split: Valid inputs:
                            gini: impurity
                            entropy: information gain
        :param splitter: Strategy used to choose the split at each node. Valid inputs:
                            best: best split.
                            random: best random split.
        :param max_depth: Maximum depth of the tree (int or None).
        :param min_samples_split: Minimum number of samples required to split an internal node.
        :param min_samples_leaf:  Minimum number of samples required to be at a leaf node.
        :param min_weight_fraction_leaf: Minimum weighted fraction of the sum total of weights required to be at a leaf node.
        :param max_features: The number of features to consider when looking for the best split, valid inputs:
                            int, float, "auto", "sqrt", "log2", None
        :param random_state: seed used by the random number generator, if it's None, it will use np.Random().
        :return:probability, conf_matrix
        """
        model = DecisionTreeClassifier(criterion=criterion, splitter=splitter, min_samples_leaf=min_samples_leaf,
                                       min_samples_split=min_samples_split,
                                       min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features,
                                       max_depth=max_depth, random_state=random_state)
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def tree_random_forest(self):
        model = RandomForestClassifier()
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def tree_extra_tree_classifier(self):
        model = ExtraTreesClassifier()
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def gradient_booster(self, loss='deviance', learning_rate=0.1, n_estimators=100, subsample=0.1,
                         criterion='friedman_mse', min_samples_split=2, min_samples_leaf=1,
                         min_weight_fraction_leaf=0, max_depth=3, min_impurity_decrease=0, random_state=None):
        """
        GB builds an additive model in a forward stage-wise fashion; it allows for the optimization of
        arbitrary differentiable loss functions.
        :param loss: loss function to be optimized, inputs:
                                deviance: Classification with probabilistic outputs.
                                exponential: Gradient boosting using AdaBoost algorithm.
        :param learning_rate: Contribution of each tree.
        :param n_estimators: Number of boosting stages to perform.
        :param subsample: Fraction of samples to be used for fitting the base learners.
        :param criterion: Function to measure the quality of a split, inputs:
                                friedman_mse: mean squared error.
                                mae: mean absolute error.
        :param min_samples_split: Minimum number of samples required to split an internal node.
        :param min_samples_leaf: Minimum number of samples required to be at leaf node.
        :param min_weight_fraction_leaf: Minimum weighted fraction of the sum total of weights.
        :param max_depth: Maximum depth of the individual regression estimators.
        :param min_impurity_decrease: Minimum value of split.
        :param random_state: Random seed, if None will use np.random().
        :return:probability, conf_matrix
        """
        model = GradientBoostingClassifier(loss=loss, learning_rate=learning_rate, n_estimators=n_estimators,
                                           subsample=subsample, criterion=criterion,
                                           min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                           min_weight_fraction_leaf=min_weight_fraction_leaf, max_depth=max_depth,
                                           min_impurity_decrease=min_impurity_decrease, random_state=random_state)
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def gradient_stochastic_descent(self, loss='hinge'):
        """
        Linear classifiers (SVM, logistic regression, a.o.) with SGD training.
        :param loss: loss function to be used, inputs:
                            linear loss: hinge, log, modified_huber,squared_hinge,
                            regression loss: squared_loss, huber, epsilon_insensitive, squared_epsilon_insensitive
        :return:probability, conf_matrix
        """
        model = SGDClassifier(loss=loss)
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def k_neighbors_classifier(self, n_neighbours=5, weights='uniform', algorithm='auto', leaf_size=30, p=2,
                               metric='minkowski'):
        """
        Classifier implementing the k-nearest neighbors vote.
        :param n_neighbours: Number of neighbours to use.
        :param weights: Weight function used in prediction, inputs:
                                uniform: All points in each neighborhood are weighted equally.
                                distance: Weight points by the inverse of their distance, closer points will have a greater influence.
        :param algorithm: Algorithm used to compute the nearest neighbors, inputs:
                                ball_tree: Fast generalized N-point problems.
                                KDTree: Euclidean tree of n-dimensions.
                                brute: Brute-force search.
                                auto: Will try to decide the most appropriate algorithm given the fit function.
        :param leaf_size: Leaf size passed to the three. This can affect the computation speed/time.
        :param p: Parameter for the Minkwoski metric.
        :param metric: Distance metric to use for the tree, inputs:
                                euclidean, manhattan, chebyshev, minkwoski, seuclidean, mahalanobis
        :return:probability, conf_matrix
        """
        model = KNeighborsClassifier(n_neighbors=n_neighbours, weights=weights, algorithm=algorithm,
                                     leaf_size=leaf_size, p=p, metric=metric)
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def r_neighbors_classifier(self, n_neighbours=5, weights='uniform', algorithm='auto', leaf_size=30, p=2,
                               metric='minkowski'):
        """
        Classifier implementing the k-nearest neighbors radius vote.
        :param n_neighbours: Number of neighbours to use
        :param weights: Weight function used in prediction, inputs:
                                uniform: All points in each neighborhood are weighted equally.
                                distance: Weight points by the inverse of their distance, closer points will have a greater influence.
        :param algorithm: Algorithm used to compute the nearest neighbors, inputs:
                                ball_tree: Fast generalized N-point problems.
                                KDTree: Euclidean tree of n-dimensions.
                                brute: Brute-force search.
                                auto: Will try to decide the most appropriate algorithm given the fit function.
        :param leaf_size: Leaf size passed to the three. This can affect the computation speed/time.
        :param p: Parameter for the Minkwoski metric.
        :param metric: Distance metric to use for the tree, inputs:
                                euclidean, manhattan, chebyshev, minkwoski, seuclidean, mahalanobis
        :return:probability, conf_matrix
        """
        model = RadiusNeighborsClassifier(n_neighbors=n_neighbours, weights=weights, algorithm=algorithm,
                                          leaf_size=leaf_size, p=p, metric=metric)
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def svm_support_vector_classification(self, C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0, shrinking=True,
                                          probability=False, max_iter=1):
        """
        C-Support Vector Classification.

        :param C: Error penalty
        :param kernel: Kernel type to use in the algorithm, inputs:
                                linear, poly, rbf, sigmoid, precomputed
        :param degree: Degree of the polynomial kernel function (only works if kernel = poly).
        :param gamma: Kernel coefficient for rbf, poly and sigmoid.
        :param max_iter: Max limit of iterations, -1 for no limit.
        :param probability: Whether or not enable probabilities, it will slow down the computation.
        :param shrinking: whether or not to use shrinking heuristic.
        :param coef0: independent kernel parameter that only works with poly and sigmoid.
        :return:probability, conf_matrix
        """
        model = SVC(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, shrinking=shrinking,
                    probability=probability, max_iter=max_iter)
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def svm_support_vector_nu_classification(self, nu=0.5, kernel='rbf', degree=3, gamma='auto', coef0=0,
                                             shrinking=True,
                                             probability=False, max_iter=1):
        """
        Nu-Support Vector Classification.
        Similar to SVC but uses a parameter to control the number of support vectors.

        :param nu: Fraction of training errors and a lower bound of the fraction of support vectors. Must be between (0,1]
        :param kernel: Kernel type to use in the algorithm, inputs:
                                linear, poly, rbf, sigmoid, precomputed
        :param degree: Degree of the polynomial kernel function (only works if kernel = poly).
        :param gamma: Kernel coefficient for rbf, poly and sigmoid.
        :param max_iter: Max limit of iterations, -1 for no limit.
        :param probability: Whether or not enable probabilities, it will slow down the computation.
        :param shrinking: whether or not to use shrinking heuristic.
        :param coef0: independent kernel parameter that only works with poly and sigmoid.
        :return:probability, conf_matrix
        """
        model = NuSVC(nu=nu, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, shrinking=shrinking,
                      probability=probability, max_iter=max_iter)
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def svm_support_vector_linear_classification(self, penalty='l2', loss='squared_hinge', dual=True, C=1.0,
                                                 multi_class='ovr', fit_intercept=True, intercept_scaling=1,
                                                 random_state=None):
        """
        Linear Support Vector Classification.
        It has more flexibility in the choice of penalties and loss functions and should scale better to large numbers of samples.
        :param penalty: Specifies the norm used in the penalization, inputs:
                                    l2: standard penalty used in SVC.
                                    l1: sparse vectors.
        :param loss: Specifies the loss function, inputs:
                                    hinge: standard SVC loss function.
                                    squared_hinge: square of the hinge loss.
        :param dual: Select the algorithm to either solve the dual or primal optimization problem.
                                    tip: Use false when n_samples > n_features
        :param C: Penalty parameter of the error
        :param multi_class: Determines the multi-class strategy, inputs:
                                    ovr,crammer_singer
        :param fit_intercept: Whether to calculate the intercept of the model (False when the data is expected to be centered)
        :param intercept_scaling: Regularization parameter.
        :param random_state: Random seed, if none the default is np.Random.
        :return:probability, conf_matrix
        """
        model = LinearSVC(penalty=penalty, loss=loss, dual=dual, C=C, multi_class=multi_class,
                          fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, random_state=random_state)
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def gaussian_process_classifier(self):
        """
        Gaussian process classification (GPC) based on Laplace approximation.
        :return:probability, conf_matrix
        """
        model = GaussianProcessClassifier()
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def neural_sklearn_mlp(self, hidden_layer_sizes=(100,), activation='relu', solver='adam', alpha=0.0001,
                           batch_size='auto', learning_rate='constant', learning_rate_init=0.001, power_t=0.5,
                           max_iter=200, shuffle=True, random_state=None, warm_start=False, momentum=0.9,
                           nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9,
                           beta_2=0.999, n_iter_no_change=10):
        """
        Multi-layer Perceptron classifier.
        :param hidden_layer_sizes: The ith element represents the number of neurons in the ith hidden layer.
        :param activation: Activation function for the hidden layer, inputs:
                                    identity: No-op activation.
                                    logistic: Logistic sigmoid function.
                                    tanh: Hyperbolic tan function.
                                    relu: Rectified linear unit function.
        :param solver: Solver for weight optimization, inputs:
                                    lbfgs: Optimizer in the family of quasi-Newton methods.
                                    sgd: Stochastic gradient descent.
                                    adam: Stochastic gradient-based optimizer.
        :param alpha: Penalty parameter.
        :param batch_size: Size of mini-batches for stochastic optimizers.
                                    Tip: if solver is lbfgs, the classifier won't use mini-batches.
        :param learning_rate: Learning rate schedule for weight updates, inputs:
                                    constant: constasnt learing rate given by learning_rate_init.
                                    invscaling: Decreases the learning rate at each time step t.
                                    adaptative: Kpees the learning rate constant to learning_rate_init as long as training loss keeps decreasing.
                                    Tip: Only used when solver = sgd.
        :param learning_rate_init: Initial learning rate used, controls the step-size in updating the weights.
        :param power_t: Exponent for inverse scaling learning rate.
        :param max_iter: Maximum number of iterations.
        :param shuffle:  Whether to shuffle samples in each iteration.
        :param random_state: Random seed, if None, the default will be np.Random.
        :param warm_start: If True, will use the solution of the previous fit as initialization, otherwise it erases previous solution
        :param momentum: Gradient descend update, must be between 0 and 1.
                                    Tip: Only works when solver = sgd.
        :param nesterovs_momentum: Only used when solver = sgd and momentum > 0.
        :param early_stopping: Whether to use early stopping to terminate training when validation score is not improving.
        :param validation_fraction: The proportion of training data to set aside as validation set for early stopping.
        :param beta_1: Exponential decay rate for estimates of first moment vector in adam.
                                    Tip, values must be between [0,1] and when solver = adam.
        :param beta_2: Exponential decay rate for estimates of second moment vector in adam.
                                    Tip, values must be between [0,1] and when solver = adam.
        :param n_iter_no_change:  Maximum number of epochs to not meet.
                                    Tip, only works when solver = sgd or solver = adam.
        :return:
        """
        model = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver, alpha=alpha,
                              batch_size=batch_size, learning_rate=learning_rate, learning_rate_init=learning_rate_init,
                              power_t=power_t, max_iter=max_iter, shuffle=shuffle, random_state=random_state,
                              warm_start=warm_start, momentum=momentum, nesterovs_momentum=nesterovs_momentum,
                              early_stopping=early_stopping, validation_fraction=validation_fraction, beta_1=beta_1,
                              beta_2=beta_2, n_iter_no_change=n_iter_no_change)
        model.fit(self.__x_train, self.__y_train)
        self.__model = model

    def predict(self, unlabeled_data):
        unlabeled_prediction = self.__model.predict(unlabeled_data)
        return unlabeled_prediction

    def generate_classification_model_statistics(self):
        """
        Method that generates the prediction value and confussion matrix
        :return:
        """
        prediction = self.__model.predict(self.__x_test)
        conf_matrix = confusion_matrix(self.__y_test, prediction)
        cv_score = cross_val_score(self.__model, self.__x_train, self.__y_train, cv=5)
        cross_validation_score = cv_score.mean()
        cross_validation_variance = cv_score.std()
        classification_score = classification_report(self.__y_test, prediction)
        self.__confussion_matrix = conf_matrix
        return cross_validation_score, conf_matrix, cross_validation_variance, classification_score

    def plot_tree_graph(self):
        """

        :return:
        """
        dot_data = tree.export_graphviz(self.__model, out_file=None,
                                        feature_names=None,
                                        class_names=['good', 'bad', 'neutral'],
                                        filled=True, rounded=True,
                                        special_characters=True)
        #graph = graphviz.Source(dot_data)
        #return graph

    def export_model(self, path, model_name):
        try:
            extension = '.model'
            file_name = str(model_name) + str(extension)
            full_path = os.path.join(path, file_name)
            pickle.dump(self.__model, open(full_path, "wb"))
        except Exception as e:
            print(e)

    def load_model(self, path):
        try:
            self.__model = pickle.load(open(path, 'rb'))
        except Exception as e:
            print(e)

    def plot_sklearn_learning_curve(self, title, X, y, ylim=None, cv=None, n_jobs=None,
                                    train_sizes=np.linspace(.1, 1.0, 5)):
        """
        Generate a simple plot of the test and training learning curve.

        Parameters
        ----------

        title : string
            Title for the chart.

        X : array-like, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.

        y : array-like, shape (n_samples) or (n_samples, n_features), optional
            Target relative to X for classification or regression;
            None for unsupervised learning.

        ylim : tuple, shape (ymin, ymax), optional
            Defines minimum and maximum yvalues plotted.

        cv : int, cross-validation generator or an iterable, optional
            Determines the cross-validation splitting strategy.
            Possible inputs for cv are:
              - None, to use the default 3-fold cross-validation,
              - integer, to specify the number of folds.
              - :term:`CV splitter`,
              - An iterable yielding (train, test) splits as arrays of indices.

            For integer/None inputs, if ``y`` is binary or multiclass,
            :class:`StratifiedKFold` used. If the estimator is not a classifier
            or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

            Refer :ref:`User Guide <cross_validation>` for the various
            cross-validators that can be used here.

        n_jobs : int or None, optional (default=None)
            Number of jobs to run in parallel.
            ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
            ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
            for more details.

        train_sizes : array-like, shape (n_ticks,), dtype float or int
            Relative or absolute numbers of training examples that will be used to
            generate the learning curve. If the dtype is float, it is regarded as a
            fraction of the maximum size of the training set (that is determined
            by the selected validation method), i.e. it has to be within (0, 1].
            Otherwise it is interpreted as absolute sizes of the training sets.
            Note that for classification the number of samples usually have to
            be big enough to contain at least one sample from each class.
            (default: np.linspace(0.1, 1.0, 5))
        """

        plt.figure()
        plt.title(title)
        if ylim is not None:
            plt.ylim(*ylim)
        plt.xlabel("Training examples")
        plt.ylabel("Score")
        train_sizes, train_scores, test_scores = learning_curve(
            self.__model, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        plt.grid()

        plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
        plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1, color="g")
        plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
        plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")

        plt.legend(loc="best")
        print(type(plt))
        return plt


    def plot_confusion_matrix(self, classes=['Good', 'Bad', 'Neutral'],
                              normalize=False,
                              title='Confusion matrix',
                              cmap=plt.cm.Blues):
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
        """
        cm = self.__confussion_matrix
        if normalize:
            cm = self.__confussion_matrix.astype('float') / self.__confussion_matrix.sum(axis=1)[:, np.newaxis]
            print("Normalized confusion matrix")
        else:
            print('Confusion matrix, without normalization')

        plt.imshow(self.__confussion_matrix, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.tight_layout()
        return plt

    def get_train_sets(self):
        return self.__x_train,self.__y_train

    def get_confusion_matrix(self):
        return self.__confussion_matrix

    def get_cm_as_dataframe(self):
        return pd.DataFrame(self.__confussion_matrix, index=[i for i in ["Pred. Good", "Pred. Neutral", "Pred. Bad"]],
                            columns=[i for i in ["True Good", "True Neutral", "True Bad"]])

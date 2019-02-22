from proyecto_1.ETL import Models, Vectorizer, File_Manager

def train(path_good, path_neutral, path_bad, key1, key2):

    fm = File_Manager.File_Manager()
    good_reviews, g_file_names = fm.extract_data_from_files(path_good)
    bad_reviews, b_file_names = fm.extract_data_from_files(path_bad)
    neutral_reviews, n_file_names = fm.extract_data_from_files(path_neutral)

    vectorizer = Vectorizer.Vectorizer(good_reviews, bad_reviews, neutral_reviews)

    x_train, x_test, y_train, y_test = vectorizer.generate_train_test_data(vectorizer='count_vect',
                                                                           test_size=0.1, random_state=None)
    model = Models.Models(x_train, y_train, x_test, y_test)
    model.train(key1,key2)
    #plot = model.plot_confusion_matrix()
    #plot.show()

    cross_validation_score, conf_matrix, cross_validation_variance, classification_score = model.generate_classification_model_statistics()
    print(f'Cross Validation score: {cross_validation_score}')
    print(f'Confussion matrix: {conf_matrix}')
    print(f'Cross Validation Variance: {cross_validation_variance}')
    print(f'Classification score: \n{classification_score}')

    return model, vectorizer
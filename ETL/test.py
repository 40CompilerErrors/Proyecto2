try:
    from ETL import Classifiers, Vectorizer, File_Manager
except Exception as e: 
    import Classifiers, Vectorizer, File_Manager


if __name__ == '__main__':
    fm = File_Manager.File_Manager()
    good_reviews, g_file_names = fm.extract_data_from_files(
        '/home/xiao/datasets/proyecto_computacion/dataset_entrenamiento/buenas/')
    bad_reviews, b_file_names = fm.extract_data_from_files(
        '/home/xiao/datasets/proyecto_computacion/dataset_entrenamiento/malas/')
    neutral_reviews, n_file_names = fm.extract_data_from_files(
        '/home/xiao/datasets/proyecto_computacion/dataset_entrenamiento/neutras/')
    unlabeled_reviews, u_file_names = fm.extract_data_from_files(
        r'/home/xiao/datasets/proyecto_computacion/dataset_entrenamiento/unlabeled/')
    vectorizer = Vectorizer.Vectorizer(good_reviews, bad_reviews, neutral_reviews, unlabeled_reviews)
    x_train, x_test, y_train, y_test = vectorizer.generate_train_test_data(vectorizer='count_vect',
                                                                           test_size=0.1, random_state=None)
    vectorizer.export_vectorizer(path='', model_name='test')
    vectorizer.plot_dataframe()
    models = Classifiers.Classifiers(x_train, y_train, x_test, y_test)
    models.naive_bayes_multinomial()
    cross_validation_score, conf_matrix, cross_validation_variance, classification_score = models.generate_classification_model_statistics()
    print(f'Cross Validation score: {cross_validation_score}')
    print(f'Confussion matrix: {conf_matrix}')
    print(f'Cross Validation Variance: {cross_validation_variance}')
    print(f'Classification score: \n{classification_score}')
    plot = models.plot_sklearn_learning_curve(title="Learning Curve", X=x_train, y=y_train)
    plot.show()
    plot = models.plot_confusion_matrix()
    plot.show()
    x_unlabeled = vectorizer.generate_unlabzeled_data(u_file_names)
    prediction = models.predict(x_unlabeled)
    print(prediction)
    vectorizer.update_unlabeled_dataframe(predicted_data=prediction)
    vectorizer.plot_dataframe()
    vectorizer.export_dataframe_csv(path='', model_name='export')
    vectorizer.export_reviews_to_files(g_path=r'/home/xiao/Desktop/test/g/', n_path=r'/home/xiao/Desktop/test/n/',
                                       b_path=r'/home/xiao/Desktop/test/b/')

import os


class File_Manager:
    def __init__(self):
        """
        Class constructor
        :param path:
        """
        self.path = None

    def __check_path(self):
        """
        Checks if path exists
        :return: boolean
        """
        if os.path.isdir(self.path):
            return True
        else:
            return False

    def __get_files(self):
        """
        Gets each file full path given a files path
        :return: list
        """
        if self.__check_path():
            files = []
            file_names = []
            for r, d, f in os.walk(self.path):
                for file in f:
                    if file.__contains__('.txt'):
                        file_path = os.path.join(r, file)
                        file_names.append(file)
                        files.append(file_path)
            return files, file_names
        else:
            print('[INFO] Path is not correct')
            return None

    @staticmethod
    def __read_file(file_path):
        """
        Reads a file and returns its content
        :param file_path:
        :return: string
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        return file_content

    def extract_data_from_files(self, path):
        """
        given an initial path in the constructor, returns a list with the files content
        :return: list
        """
        self.path = path
        files, file_names = self.__get_files()
        file_data = []
        for file in files:
            content = self.__read_file(file)
            file_data.append(content)
        return file_data, file_names

    def get_file_count(self):
        """
        Returns the number of files in a path
        :return: integer
        """
        files = self.__get_files()
        return len(files)

    def write_file(self, text, file_name, path):
        file_path = os.path.join(path, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)

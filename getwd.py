import os

os.getcwd()



def check_write_permissions(path):
    try:
        test_file = os.path.join(path, "temp_file.txt")
        with open(test_file, 'w') as file:
            file.write('test')
        os.remove(test_file)
        return True
    except PermissionError:
        return False

path = "/Users/ari/Documents/Data_Science/3_semester/learning_from_las_vegas/LFLV/"
print(check_write_permissions(path))



def check_folder_creation_permissions(path):
    try:
        test_folder = os.path.join(path, "temp_folder")
        os.makedirs(test_folder)
        os.rmdir(test_folder)
        return True
    except PermissionError:
        return False

path = "/Users/ari/Documents/Data_Science/3_semester/learning_from_las_vegas/LFLV/"
print(check_folder_creation_permissions(path))

def create_folder(path):
    try:
        os.makedirs(path)
        print(f"Ordner '{path}' erfolgreich erstellt.")
    except FileExistsError:
        print(f"Ordner '{path}' existiert bereits.")
    except PermissionError:
        print(f"Keine Berechtigung zum Erstellen des Ordners '{path}'.")

path = "/Users/ari/Documents/Data_Science/3_semester/learning_from_las_vegas/LFLV/images"
create_folder(path)
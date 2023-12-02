import os
import shutil

def organize_pdfs(directory):
    # List all files in the given directory
    files = os.listdir(directory)

    for file in files:
        # Check if the file is a PDF
        if file.endswith('.pdf'):
            # Extract the file name without extension
            folder_name = file.rsplit('.', 1)[0]

            # Create a new folder path
            new_folder_path = os.path.join(directory, folder_name)

            # Create the folder if it does not exist
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)

            # Move the PDF file to the newly created folder
            shutil.move(os.path.join(directory, file), new_folder_path)

if __name__ == "__main__":
    organize_pdfs("../data/result")
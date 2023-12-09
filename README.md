# Intuitive-response-on-ChatGPT
This is the repository of the capstone project "Intuitive response on ChatGPT"

# Introduction
The web application, built with FastAPI and HTML, offers a dynamic user experience with chat or messaging capabilities. The application combines a robust backend with an interactive front end.

## Features
### Backend
- FastAPI Framework: Enables efficient and easy handling of HTTP requests.
- Chat Functionalities: Includes endpoints for starting a new chat and sending messages.
- PDF Handling: Integration with fitz library suggests functionality related to PDFs.
### Frontend
- User Input Forms: Facilitates user interaction through forms, buttons, and text areas.
- Responsive Layout: Structured with headers, paragraphs, and divisions for a clean layout.
- Dynamic Content: Utilizes JavaScript for enhanced user experience.

## Installation
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. To run the program, change directory to the webApp2, and run
```
python main.py
```

### Troubleshooting

- If you encountered problem installing fitz, you can try to install the c++ build tool first. https://visualstudio.microsoft.com/visual-cpp-build-tools/
- If something like `connection error: [SSL: CERTIFICATE_VERIFY_FAILED]` pop up, try the following command
```
pip config set global.trusted-host \
    "pypi.org files.pythonhosted.org pypi.python.org" \
    --trusted-host=pypi.python.org \
    --trusted-host=pypi.org \
    --trusted-host=files.pythonhosted.org
```
```
pip install certifi
```

## Dependencies
The application relies on various Python libraries including FastAPI, Pydantic, Jinja2, sentence_transformers, and fitz. A complete list can be found in the requirements.txt file.

## Handling New PDFs
When integrating new PDFs into our system, it's important to ensure they are processed correctly to maintain the efficiency and accuracy of our application. Here are the steps to follow:
1. Creating Company-Year Directories: For each company's annual report, create a new directory within the **webApp2/data/result directory** directory. The naming convention for these directories should be **Company_Year**. For example, a directory for Unilever Company's 2023 report would be named Unilever_2023.
2. Uploading Annual Reports:
    - Single Report per Year: It's important to upload only the final annual report for each year into the respective directory.
    - Quarterly Report Handling: Although each quarter might generate a report, only the final annual report should be stored in these directories.
    - File Format: Ensure that the reports are in PDF format before uploading.
3. Algorithm Compatibility:
    - Unique PDF Requirement: Our backend algorithm is designed to process all PDF files within a given directory. Therefore, having more than one PDF file in a directory can disrupt the algorithm's functionality.
    - Maintaining Algorithm Integrity: To ensure the algorithm operates correctly, it is essential to have only one PDF file (the final annual report) in each Company_Year directory.

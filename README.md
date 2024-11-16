# Create Anki deck for standard chữ Hán Nôm to chữ Quốc Ngữ

## Description
For this project, I aimed to create an Anki deck that helps learning standard Han Nom characters, organized by grade level. The source list was taken from https://www.hannom-rcv.org/.

The notebook generates six separate decks, which I later merged using Anki (by importing all six decks and then exporting them as one).

Link of the Anki deck: https://ankiweb.net/shared/info/1920684226

## Installation Instructions

You can follow the steps below to create the decks by yourself.

### 1. **Clone the Repository**
First, clone the repository to your local machine:

```bash
    git clone <repository-url>
    cd <repository-directory>
```

### 2. **Set Up a Virtual Environment (Optional but Recommended)**

For macOS/Linux:
```bash
    python3 -m venv myenv
    source myenv/bin/activate
```
For Windows:
```bash
    python -m venv myenv
    .\myenv\Scripts\activate
```

### 3. Install Dependencies from *requirements.txt*
```bash
    pip install -r requirements.txt
```
### 4. Run the Jupyter notebook.

The result is in *result* folder
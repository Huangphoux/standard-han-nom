# Create Anki decks for learning the standard chữ Hán Nôm

## Description
For this project, I aimed to create the Anki decks that helps learning the standard Han Nom characters. The deck are organized by grade levels ranging from grade 1 to grade 5, with THCS level be denoted as grade 6. The source list was taken from https://www.hannom-rcv.org/.

The notebook generates 6+6 = 12 separated decks, which I later merged into 2 decks using Anki (by manually importing six decks and then exporting them as one).

Link of the Anki decks: [chữ Hán Nôm -> chữ Quốc ngữ](https://ankiweb.net/shared/info/447461247) and [chữ Quốc ngữ -> chữ Hán Nôm](https://ankiweb.net/shared/info/737152775)

Notes:
1. The Han Nom characters in the brackets are the simplipied version (giản thể)
2. The uppercase Quoc-ngu letters are the standard Sino-Vietnamese (Hán Việt) sounds of Chinese characters; lowercase ones are the reading of the Nom character or the non-standard Sino-Vietnamese sounds of the Chinese character.

## Installation Instructions

You can follow the steps below to create the decks by yourself if you want.

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

### 3. Install Dependencies from `requirements.txt`
```bash
    pip install -r requirements.txt
```
### 4. Run the Jupyter notebook.

The results will be in `results` folder

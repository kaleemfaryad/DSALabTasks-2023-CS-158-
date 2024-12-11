import sys
import nltk
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import tkinter as tk
from tkinter import filedialog
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit

# Install NLTK resources (only run once)
# nltk.download('punkt')
# nltk.download('stopwords')

# Preprocess the text by tokenizing, removing punctuation and stopwords
def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Lowercasing to make comparison case-insensitive
    tokens = [word for word in tokens if word.isalpha()]  # Remove punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    return " ".join(tokens)

# Function to compute Cosine Similarity
def cosine_sim(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_matrix[0][0]

# Function to compute Jaccard Similarity
def jaccard_sim(text1, text2):
    set1 = set(text1.split())
    set2 = set(text2.split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

# Function to read text from different file formats
def read_file(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        ext = file_path.split('.')[-1].lower()
        if ext == 'txt' or ext == 'py' or ext == 'cpp':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        elif ext == 'docx':
            import docx
            doc = docx.Document(file_path)
            text = []
            for para in doc.paragraphs:
                text.append(para.text)
            return '\n'.join(text)
        else:
            return "Unsupported file type"
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Function to detect plagiarism
def detect_plagiarism(doc1, doc2, threshold=0.7):
    doc1 = preprocess_text(doc1)
    doc2 = preprocess_text(doc2)
    
    # Compute Cosine Similarity
    cos_sim = cosine_sim(doc1, doc2)
    # Compute Jaccard Similarity
    jac_sim = jaccard_sim(doc1, doc2)
    
    result_text = f"Cosine Similarity: {cos_sim:.4f}\nJaccard Similarity: {jac_sim:.4f}\n"
    
    # Check if plagiarism is detected
    if cos_sim > threshold or jac_sim > threshold:
        result_text += "Plagiarism detected!"
    else:
        result_text += "No plagiarism detected."
    
    return result_text

# PyQt5 GUI for plagiarism detection system
class PlagiarismCheckerGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        # Set window title and size
        self.setWindowTitle('Plagiarism Detection System')
        self.setGeometry(100, 100, 600, 400)

        # Create layout
        layout = QVBoxLayout()

        # Add buttons and labels
        self.file1_path = QLineEdit(self)
        self.file1_path.setPlaceholderText('Select the first file')
        layout.addWidget(self.file1_path)

        self.file2_path = QLineEdit(self)
        self.file2_path.setPlaceholderText('Select the second file')
        layout.addWidget(self.file2_path)

        self.select_file1_btn = QPushButton('Select First File', self)
        self.select_file2_btn = QPushButton('Select Second File', self)
        self.check_plagiarism_btn = QPushButton('Check Plagiarism', self)
        layout.addWidget(self.select_file1_btn)
        layout.addWidget(self.select_file2_btn)
        layout.addWidget(self.check_plagiarism_btn)

        # Add result text area
        self.result_label = QLabel('Result will be shown here', self)
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_area)

        # Set layout to the window
        self.setLayout(layout)

        # Connect buttons to actions
        self.select_file1_btn.clicked.connect(self.select_file1)
        self.select_file2_btn.clicked.connect(self.select_file2)
        self.check_plagiarism_btn.clicked.connect(self.check_plagiarism)

    # Function to open file dialog for the first file
    def select_file1(self):
        file_path = self.select_file()
        if file_path:
            self.file1_path.setText(file_path)

    # Function to open file dialog for the second file
    def select_file2(self):
        file_path = self.select_file()
        if file_path:
            self.file2_path.setText(file_path)

    # Function to select a file
    def select_file(self):
        root = tk.Tk()
        root.withdraw()  # Hide the Tkinter root window
        return filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"), ("C++ Files", "*.cpp"), ("Word Files", "*.docx")])

    # Function to check plagiarism
    def check_plagiarism(self):
        file1 = self.file1_path.text()
        file2 = self.file2_path.text()

        if not file1 or not file2:
            self.result_area.setText('Please select two files to compare.')
            return

        # Read the files
        doc1 = read_file(file1)
        doc2 = read_file(file2)

        if not doc1 or not doc2:
            self.result_area.setText('Error reading one or both files.')
            return

        # Perform plagiarism check
        result = detect_plagiarism(doc1, doc2)
        self.result_area.setText(result)

# Run the PyQt5 application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlagiarismCheckerGUI()
    window.show()
    sys.exit(app.exec_())

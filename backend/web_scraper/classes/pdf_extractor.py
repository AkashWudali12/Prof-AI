import fitz
from sentence_transformers import SentenceTransformer
import string


class PDF_RESUME_EXTRACTOR:
    def __init__(self):
        self.allowed_characters = set(string.printable)
        self.allowed_characters.add(' ')
        self.allowed_characters.add("\n")
        pass

    def extract_text_from_path(self, file_path):
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()

        filtered_text = ''.join(char for char in text if char in self.allowed_characters)
        
        # print("Resume text:", filtered_text)
        return filtered_text


    def embed_documents(self, text):
        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        try:
            print("Got embedding from pdf_extractor")
            embedding = model.encode(text)
            embedding = embedding.tolist()
            print("Dimension of embedding from pdf_extractor:", len(embedding))
        except Exception as e:
            print("The following exception occured when getting an embedding from pdf_extractor:", e)
            embedding = []
        finally:
            return embedding

        

        


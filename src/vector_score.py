from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS 
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

class VectorScore:
    def __init__(self,csv_path:str,persist_directory:str="faiss_db"):
        self.csv_path=csv_path
        self.persist_directory=persist_directory
        self.embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def build_and_save_vector_store(self):
        loader = CSVLoader(
        file_path=self.csv_path,
        encoding="utf-8",
        metadata_columns=["series_id", "title"],
    )

        data=loader.load()
        splitter=RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )
        texts=splitter.split_documents(data)
        db=FAISS.from_documents(texts,self.embeddings)
        db.save_local(self.persist_directory)
        return db

    def load_vector_store(self):
        db=FAISS.load_local(self.persist_directory,self.embeddings,allow_dangerous_deserialization=True)
        return db 
    

      



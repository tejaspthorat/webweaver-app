import base64
import io
from docx import Document
from supabase import create_client
from flask import Flask, request, jsonify, Blueprint

# Supabase credentials

#putting the supabase url and key here so that they are accessable during evaluation
SUPABASE_URL = 'https://peijjbyslrdvvtapmyfp.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBlaWpqYnlzbHJkdnZ0YXBteWZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTM2MTIxNjQsImV4cCI6MjAyOTE4ODE2NH0.Vou9_BaHweiBtHeNYTfUziZ84G_pD1XYdPPNFt1B41Q'


# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def base64_to_docx(base64_string, filename):

    binary_data = base64.b64decode(base64_string)
    docx_buffer = io.BytesIO(binary_data)
    docx_doc = Document(docx_buffer)
    docx_doc.save(filename)

def upload_to_supabase(filename, bucket_name, folder_name):
    with open(filename, 'rb') as file:
        file_data = file.read()

    response = supabase.storage.from_("resume").upload(
        file=file_data,
        path=f"{folder_name}/{filename}"
    )

    return response


bucket_name = "resume"
folder_name = "documents"

main = Blueprint('main', __name__)

@main.route('/upload', methods=['POST'])
def upload_file():
    
    base64_string = request.json['base64_string']
    filename = request.json['filename']
    base64_to_docx(base64_string, filename)
    upload_to_supabase(filename, bucket_name, folder_name)
    
    return jsonify({"message": "File uploaded successfully!"})


from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import tiktoken as tk
from werkzeug.utils import secure_filename
import os
from web_scraper.classes.pdf_extractor import PDF_RESUME_EXTRACTOR
from web_scraper.classes.ai_agent import OPEN_AI_AGENT
from dotenv import load_dotenv
import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

from google.cloud.sql.connector import Connector
import sqlalchemy



# # Configure a maximum upload size limit (optional, e.g., 16MB)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#needs to be like this in this format

app = Flask(__name__)
CORS(app)

# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

load_dotenv()
password = os.getenv("POSTGRES_PASSWORD")

load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key)
index = pc.Index("prof-ai")

email_template = """
Dear Professor [Last Name],

I hope this message finds you well. My name is [Your Name], a [grade level/year] student at [School Name]. I am reaching out to inquire about potential research opportunities in your lab, particularly in [specific research area].

I was captivated by your recent publication, "[Title of Recent Article]," especially your findings on [specific finding or methodology from the abstract]. This aligns closely with my interests in [relevant field or subject area].

Your work on [specific topic from another paper] resonates with my background in [relevant skill, coursework or experience from resume]. I am eager to learn more about [specific methodology or theoretical framework mentioned in abstracts] and its applications in [related field].

I believe my skills in [relevant skills] and my experience with [mention any relevant coursework, projects, research, or experience from resume] would allow me to contribute meaningfully to your research.

Attached is my resume for your review. I would greatly appreciate the chance to discuss any potential openings in your lab or to learn more about your current projects.

Thank you for your time and consideration. I look forward to the possibility of contributing to your research.

Sincerely,

[Your Name]

[Your Contact Information]
"""

def getconn():
    print("GET CONN")
    connector = Connector()

    conn = connector.connect(
        os.getenv("INSTANCE_CONNECTION_NAME"),
        "pg8000",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        db=os.getenv("DB_NAME")
    )
    return conn

pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

@app.route("/get_professor_description", methods=['POST'])
def get_professor_from_interest_description():

    university = request.form.get('university')

    studentName = request.form.get("studentName")
    studentGrade = request.form.get("studentGrade")
    studentSchool = request.form.get("studentSchool")

    message = request.form.get("message")

    print("Student Info:", studentName, studentGrade, studentSchool)

    print("University Name:", university)
    
    try:
        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        message_embedding = model.encode(message).tolist()
        print("got the message embedding from app.py:", len(message_embedding))
    except Exception as e:
        print("Could not embed message in app.py because the following exception occured:", e)
        return jsonify({"response":{"error":e, "file":"app.py", "cause":"getting message embedding"}}), 400
    
    try:
        exclude = [] # keep track of already emailed professors

        top_k_authors = index.query(
                namespace=university,
                vector=message_embedding,
                top_k=7,
                include_values=True,
                filter={
                    "id": {"$nin": exclude}  
                }
            )

        author_id_list = [author["id"] for author in top_k_authors["matches"]]

        authors_map = {}

        print(author_id_list)
        
        select_query = sqlalchemy.text("""
            SELECT abstract_list 
            FROM abstracts 
            WHERE professor_id = :professor_id
        """)
        
        for professor_id in author_id_list:
            with pool.connect() as db_conn:
                result = db_conn.execute(select_query, {"professor_id": professor_id})
                db_conn.commit()
                abstracts = result.fetchall()

            if abstracts:
                abstract_list = abstracts[0][0]  # result[0] contains the abstract_list
                print("Abstract List Found")
            else:
                abstract_list = []
                print("No abstracts found for the given professor_id.")
            
            response = index.fetch(ids=[professor_id], namespace=university)

            # Access the metadata
            if professor_id in response['vectors']:
                metadata = response['vectors'][professor_id]['metadata']
                print("Metadata Found")
            else:
                metadata = {}
                print("Vector not found.")

            if abstract_list:
                authors_map[professor_id] = (abstract_list, metadata)
        
        system_message = """
            Your job is to provide information of 
            a Professor based on their abstracts and a template. 
            Base your responses soley off of information given in the prompt.
            """

        descriptions_dct = {}

        ai_agent = OPEN_AI_AGENT(system_message=system_message)
        encoding = tk.encoding_for_model("gpt-3.5-turbo")

        for prof_id in authors_map:
            author_abstract_list, author_info = authors_map[prof_id]
            print("Professor:", author_info["Name"])

            prompt = "Based on the abstracts below, write 4-5 concise bullet points summarizing this professors research interest. The bullet points should specific to the research they are conducting."

            for abstract in author_abstract_list:
                prompt += "\n\n" + abstract
            
            tokens = encoding.encode(prompt)
            token_count = len(tokens)
            print(f"Number of tokens for prompt: {token_count}")
            
            agent_response = ai_agent.run_completion(prompt, 0.3)

            descriptions_dct[prof_id] = "Description of research:" + "\n" + agent_response
            
        return jsonify({"response":{"descriptions_by_id":descriptions_dct, "abstracts_and_info_by_id":authors_map, "student_info":[studentName, studentGrade, studentSchool]}}), 200
    except Exception as e:
        return jsonify({"response":{"error":e, "file":"app.py", "cause":"finding profs and creating description"}}), 400

def capitalize_name(full_name: str) -> str:
    # Split the full name into parts (first name and last name)
    name_parts = full_name.split()
    
    # Capitalize the first letter of each part
    capitalized_parts = [part.capitalize() for part in name_parts]
    
    # Join the parts back into a single string
    capitalized_name = ' '.join(capitalized_parts)
    
    return capitalized_name

@app.route("/get_resume_text", methods=['POST'])
def get_resume_text():
    try:
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join("web_scraper/classes/resumes", filename)
            print(filename)
            file.save(file_path)

            pdf_parser = PDF_RESUME_EXTRACTOR()

            resume_text = pdf_parser.extract_text_from_path(file_path)
        return jsonify({"resumeText":resume_text}), 200
    except Exception as e:
        return jsonify({"error":e}), 400

        
@app.route("/generate_email", methods=["POST"])
def generate_email():
    try:
        data = request.get_json()
        abstract_list = data["list"]
        name = data["name"]
        studentInfo = " ".join(data["student_info"])
        resume_text = data["resumeText"]

        if not resume_text:
            return jsonify({"error":"No resume"}), 400

        lastName = name.split(" ")[2]

        print("last name:", lastName)
        print("student info:", studentInfo)
        print("resume:")
        print(resume_text)


        system_message = """
            Your role is to generate cold emails for high school, undergraduate, and graduate students seeking research opportunities with professors. 

            - Use a formal, professional tone in all emails.
            - Ensure that each email is tailored specifically to the context and details provided in the prompt.
            - Do not include any information that is not explicitly provided in the prompt.s
            - Focus on crafting clear, concise, and respectful emails that effectively convey the student's interest and qualifications.

            Accuracy and professionalism are paramount.
            """
        
        ai_agent = OPEN_AI_AGENT(system_message=system_message)
        encoding = tk.encoding_for_model("gpt-3.5-turbo")

        prompt = "Using the template below, please generate a complete email. Make sure to replace each placeholder (e.g., [Last Name], [Your Name], [grade level/year], etc.) with the appropriate specific details. Ensure that no placeholders are left unfilled." + \
        "\n\n" + email_template + "\n\n" + "below the template, I have included relevant information to fill it out. " + \
        "You must replace all information in brackets (ie [information]), including in the subject line, with relevant information based on the context below:" + "\n\n"  + \
        "Student's basic information: " + studentInfo + "\n\n" + \
        "Student's resume with relevant coursework, skills, experience, research and/or projects: " + "\n" + resume_text + "\n\n" + \
        "The professors last name: " + lastName + "\n\n" + \
        "The list of titles and abstracts for research articles the professor published: " + "\n" + \
        "\n".join([abstract for abstract in abstract_list])

        tokens = encoding.encode(prompt)
        token_count = len(tokens)

        agent_response = ai_agent.run_completion(prompt, 0.3)

        print(agent_response)

        return jsonify({"email":agent_response}), 200
    except Exception as e:
        return jsonify({"error":e}), 400

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf'}

def main():
    if len(sys.argv) > 1:
        message = sys.argv[1]
        print(f"Received message: {message}")
        # Add more processing logic here as needed

if __name__ == "__main__":
    app.run(debug=True)

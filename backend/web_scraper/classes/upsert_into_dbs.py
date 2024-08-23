import sys
args = sys.argv[1:]
from pinecone import Pinecone, ServerlessSpec
import json
import random
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
password = os.getenv("POSTGRES_PASSWORD")

load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")


def main():
    start = int(args[0])
    end = int(args[1])
    namespace = args[2]
    pc = Pinecone(api_key=api_key)
    index = pc.Index("prof-ai")

    connection = psycopg2.connect(
            host="localhost",       # e.g., "localhost" or your database host
            database="prof-ai", # Replace with your database name
            user="postgres",        # Replace with your PostgreSQL username
            password=password       # Use the password from the environment variable
        )

    cursor = connection.cursor()

    with open('faculty_data/umd_data_to_insert.json', 'r') as file:
        data = json.load(file)
    
    if end == -1:
        end = len(data)

    for prof in data[start:end]:
        if type(prof["values"]) != float:
            new_id = str(random.randint(10**14, 10**15 - 1))
            new_metadata = {"Name": prof["metadata"]["Name"], "Email":prof["metadata"]["Email"], "Position":prof["metadata"]["Position"], 
                            "Major":prof["metadata"]["Major"], "Picture URL":prof["metadata"]["Picture URL"]}
            index.upsert([(new_id, prof["values"], new_metadata)], namespace=namespace)
    
            insert_query = """
            INSERT INTO abstracts (professor_id, abstract_list, university)
            VALUES (%s, %s, %s);
            """

            cursor.execute(insert_query, (new_id, prof["metadata"]["abstracts"], namespace))
            connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()



if __name__ == "__main__":
    main()
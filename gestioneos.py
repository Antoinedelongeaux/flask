#from dotenv import load_dotenv
#load_dotenv()
import os
from supabase import create_client
from flask import Flask, render_template, request

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


def get_logements():
    response = supabase.table('logements').select('*').execute()
    logements = response.data
    print(logements)
    return logements

def logement_details(ID_logement):
    response = supabase.table('logements').select('*').eq("id", ID_logement).execute()
    first_element = response.data[0]
    ID_logement= first_element['id']
    loyer = first_element['loyer']
    description = first_element['description']
    nom = first_element['nom']
    return ID_logement,loyer, description, nom

def questionnaire(ID_logement) :

     response = supabase.table('recherches').select('*').eq("ID_logement", ID_logement).execute()

     first_element = response.data[0]


     ID_recherche= first_element['id']
     question_1 = first_element['critere_1_description']
     question_2 = first_element['critere_2_description']
     question_3 = first_element['critere_3_description']
     return ID_recherche,question_1, question_2, question_3   



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return "Page de login"

@app.route('/inscription')
def inscription():
    return "Page d'inscription"

@app.route('/logements')
def offres():
    logements_list = get_logements()
    return render_template('logements.html', logements_list=logements_list)

@app.route('/logement_<int:ID_logement>')
def logement(ID_logement):
    logement_info = logement_details(ID_logement)
    return render_template('logement.html', ID_logement=logement_info[0],loyer=logement_info[1], description=logement_info[2],nom=logement_info[3])



@app.route('/recherche_<int:ID_logement>')
def recherche(ID_logement):
     questions = questionnaire(ID_logement)
     return render_template('questionnaire.html', ID_logement=ID_logement,question_1=questions[1],question_2=questions[2],question_3=questions[3])

@app.route('/submit_<int:ID_logement>', methods=['POST'])
def submit(ID_logement):
     ID_recherche=questionnaire(ID_logement)[0]
     print(ID_recherche)
     reponse_1 = request.form['Reponse_1']
     reponse_2 = request.form['Reponse_2']
     reponse_3 = request.form['Reponse_3']
     email = request.form['Reponse_4']
     prospect = supabase.table("prospects").insert({'ID_recherche':ID_recherche,"reponse_1":reponse_1 , "reponse_2":reponse_2 , "reponse_3":reponse_3 , "email":email }).execute()
     assert len(prospect.data) > 0
     return "Merci pour votre reponse !"




if __name__ == '__main__':
    app.run(debug=True)

const { createClient } = supabase;

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

function getLogements() {
  return supabase.from('logements').select('*').then(({ data }) => {
    console.log(data);
    return data;
  });
}

function getLogementDetails(ID_logement) {
  return supabase.from('logements').select('*').eq('id', ID_logement).then(({ data }) => {
    const { id, loyer, description, nom } = data[0];
    return { id, loyer, description, nom };
  });
}

function getQuestionnaire(ID_logement) {
  return supabase.from('recherches').select('*').eq('ID_logement', ID_logement).then(({ data }) => {
    const { id, critere_1_description, critere_2_description, critere_3_description } = data[0];
    return { id, critere_1_description, critere_2_description, critere_3_description };
  });
}

const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.render('index');
});

app.get('/login', (req, res) => {
  res.send('Page de login');
});

app.get('/inscription', (req, res) => {
  res.send('Page d\'inscription');
});

app.get('/logements', (req, res) => {
  getLogements().then(logements => {
    res.render('logements', { logements_list: logements });
  });
});

app.get('/logement_:ID_logement', (req, res) => {
  getLogementDetails(req.params.ID_logement).then(logement => {
    res.render('logement', logement);
  });
});

app.get('/recherche_:ID_logement', (req, res) => {
  getQuestionnaire(req.params.ID_logement).then(questions => {
    res.render('questionnaire', { ID_logement: req.params.ID_logement, ...questions });
  });
});

app.post('/submit_:ID_logement', (req, res) => {
  const ID_logement = req.params.ID_logement;
  getQuestionnaire(ID_logement).then(({ id: ID_recherche }) => {
    const { Reponse_1: reponse_1, Reponse_2: reponse_2, Reponse_3: reponse_3, Reponse_4: email } = req.body;
    supabase.from('prospects').insert({ ID_recherche, reponse_1, reponse_2, reponse_3, email }).then(({ data }) => {
      console.assert(data.length > 0, 'No data inserted');
      res.send('Merci pour votre réponse !');
    });
  });
});

app.listen(port, () => {
  console.log(`Server started on port ${port}`);
});

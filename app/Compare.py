from rake_nltk import Rake
from sentence_transformers import SentenceTransformer, util
import nltk as nltk

def compare(text, definition):
    nltk.download('stopwords')
    nltk.download('punkt')
    model = SentenceTransformer('all-MiniLM-L6-v2')
    r = Rake()

    r.extract_keywords_from_text(definition)
    keywords = r.get_ranked_phrases()

    en_1 = model.encode(text)
    en_2 = model.encode(definition)
    
    cosine_scores = util.cos_sim(en_1, en_2)
    return cosine_scores.item(), keywords
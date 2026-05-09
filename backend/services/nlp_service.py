import io
import PyPDF2
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + " "
    return text.strip()

def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    text = " ".join([para.text for para in doc.paragraphs])
    return text.strip()

def calculate_similarity(resume_text: str, jd_text: str) -> float:
    # Handle empty text cases
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

    custom_stop_words = {
        'good', 'have', 'command', 'looking', 'strong', 'understanding',
        'knowledge', 'experience', 'ability', 'skills', 'excellent',
        'working', 'required', 'preferred', 'years', 'team', 'work',
        'must', 'including', 'using', 'like', 'role', 'job', 'description'
    }
    all_stop_words = list(ENGLISH_STOP_WORDS.union(custom_stop_words))

    vectorizer = TfidfVectorizer(stop_words=all_stop_words)
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    
    # vectors[0] is resume, vectors[1] is JD
    similarity_matrix = cosine_similarity(vectors[0], vectors[1])
    score = similarity_matrix[0][0]
    
    # Return percentage score
    return round(float(score) * 100, 2)

import spacy
import re

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_missing_skills(resume_text: str, jd_text: str) -> list:
    """
    Deterministic Tech Skill Extraction. 
    Instead of relying on NLP guessing and stopwords, this explicitly checks against a whitelist of hundreds of known IT skills, frameworks, languages, and tools.
    """
    # Explicit master list of technical and professional skills expected in JDs
    tech_skills = {
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php', 'swift', 'kotlin',
        'react', 'angular', 'vue', 'nextjs', 'nodejs', 'express', 'django', 'flask', 'fastapi', 'spring', 'laravel',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'oracle', 'dynamodb',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'github actions', 'gitlab ci',
        'html', 'css', 'sass', 'less', 'tailwind', 'bootstrap', 'material ui',
        'linux', 'unix', 'bash', 'shell', 'git', 'agile', 'scrum', 'kanban', 'jira', 'confluence',
        'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
        'data analysis', 'data engineering', 'spark', 'hadoop', 'kafka', 'airflow', 'tableau', 'power bi',
        'cybersecurity', 'penetration testing', 'cryptography', 'network security', 'owasp',
        'ui', 'ux', 'figma', 'adobe xd', 'sketch', 'photoshop',
        'salesforce', 'sap', 'erp', 'crm', 'seo', 'sem', 'google analytics',
        'api', 'graphql', 'rest', 'soap', 'microservices', 'serverless', 'oauth', 'jwt',
        'tdd', 'bdd', 'jest', 'pytest', 'selenium', 'cypress', 'mocha',
        'blockchain', 'web3', 'smart contracts', 'ethereum', 'solidity'
    }

    jd_lower = jd_text.lower()
    resume_lower = resume_text.lower()

    jd_keywords = set()
    resume_keywords = set()

    for skill in tech_skills:
        escaped_skill = re.escape(skill)
        start_bound = r'\b'
        end_bound = r'\b' if skill[-1].isalnum() else r'(?!\w)'
        
        pattern = re.compile(f"{start_bound}{escaped_skill}{end_bound}")
        
        if pattern.search(jd_lower):
            jd_keywords.add(skill)
        if pattern.search(resume_lower):
            resume_keywords.add(skill)

    # Missing = Required in JD but not found in Resume
    missing = list(jd_keywords - resume_keywords)
    
    # Sort them alphabetically for consistency, return top 12
    missing.sort()
    return missing[:12]

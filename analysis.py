import pandas as pd
import nltk
from nltk.corpus import stopwords
from textstat import textstat
import re

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords')

def load_word_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            words = file.read().splitlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            words = file.read().splitlines()
    return words

# Load word lists
stop_words = load_word_list('stop.txt')
positive_words = load_word_list('positive.txt')
negative_words = load_word_list('negative.txt')

# Define function to clean and tokenize text
def clean_text(text):
    text = re.sub(r'[^A-Za-z\s]', '', text).lower()
    words = text.split()
    cleaned_words = [word for word in words if word not in stop_words]
    return cleaned_words

# Define function to count syllables in a word
def count_syllables(word):
    vowels = "aeiouy"
    num_vowels = 0
    previous_char_was_vowel = False
    for char in word:
        if char in vowels:
            if not previous_char_was_vowel:
                num_vowels += 1
            previous_char_was_vowel = True
        else:
            previous_char_was_vowel = False
    if word.endswith('e'):
        num_vowels -= 1
    if num_vowels == 0:
        num_vowels += 1
    return num_vowels

# Define function to compute scores
def compute_scores(text):
    words = clean_text(text)
    
    # Sentiment Analysis
    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)
    
    # Text Analysis using textstat
    avg_sentence_length = textstat.avg_sentence_length(text)
    complex_words_count = sum(1 for word in words if count_syllables(word) >= 3)
    percentage_complex_words = (complex_words_count / len(words)) * 100
    fog_index = textstat.gunning_fog(text)
    avg_number_of_words_per_sentence = textstat.avg_sentence_length(text)
    word_count = len(words)
    syllable_per_word = textstat.syllable_count(text) / word_count
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    avg_word_length = sum(len(word) for word in words) / word_count
    
    return [
        positive_score, negative_score, polarity_score, subjectivity_score,
        avg_sentence_length, percentage_complex_words, fog_index,
        avg_number_of_words_per_sentence, complex_words_count, word_count,
        syllable_per_word, personal_pronouns, avg_word_length
    ]

# Read input Excel file
df = pd.read_excel('W3input.xlsx')
results = []

# Process each URL_ID
for index, row in df.iterrows():
    url_id = row['URL_ID']
    with open(f'{url_id}.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    scores = compute_scores(text)
    results.append([url_id, *scores])

# Create DataFrame for results
output_df = pd.DataFrame(results, columns=[
    'URL_ID', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
    'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE',
    'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
])

# Save results to Excel file
output_df.to_excel('Goutput.xlsx', index=False)

print("Sentiment analysis completed and results saved.")

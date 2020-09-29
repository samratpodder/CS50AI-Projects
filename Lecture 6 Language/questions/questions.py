import nltk
import sys
import os
import string
from math import log

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    retDict = dict()
    filesInDir = os.listdir(directory)
    for file in filesInDir:
        retDict[file] = open(os.path.join(directory,file),encoding='utf-8').read()
    return retDict

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # nltk.download('stopwords')
    listOfWords = list()
    document = document.lower()
    listOfWords = nltk.word_tokenize(document,language='english')
    retlistOfWords = list()
    for word in listOfWords:
        if (not all(char in string.punctuation for char in word)) and (word not in nltk.corpus.stopwords.words("english")):
            retlistOfWords.append(word)

    return retlistOfWords



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    retval = dict()
    for key in documents.keys():
        for word in documents[key]:
            retval[word] = idf(word,documents)
    return retval
def wordincorpus(word,corpus):
    counter =0 
    for listofwords in corpus.values():
        if word in listofwords:
            counter+=1
    return counter
def idf(word,documents):
    return log((len(documents)/wordincorpus(word,documents)))

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf = dict()
    filerank = list()
    for file in files:
        tfidf[file] = 0
        for word in query:
            tfidf[file] += files[file].count(word)*idfs[word]
    for key, value in sorted(tfidf.items(),key=lambda item: item[1] , reverse=True):
        filerank.append(key)
    filerank = filerank[0:n]
    return filerank


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    rank = list()
    for sentence in sentences:
        sentence_rank = [sentence,0,0]
        for word in query:
            if word in sentences[sentence]:
                sentence_rank[1] += idfs[word]
                sentence_rank[2] += sentences[sentence].count(word) / len(sentences[sentence])
        rank.append(sentence_rank)

    sortedRank = list()
    for sentence, wordDensity, queryTermDensity in sorted(rank, key=lambda item: (item[1], item[2]), reverse=True):
        sortedRank.append(sentence)
    sortedRank  = sortedRank[0:n]
    return sortedRank



if __name__ == "__main__":
    main()

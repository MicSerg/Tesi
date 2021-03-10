# Tesi di Michele Sergola

Dataset -> https://doi.org/10.5281/zenodo.3653367

Il Dataset è composto da metadati delle app estratti settimanalmente, per 4 differenti Paesi, durante 30 settimane.
Di queste 30 settimane, ho preso in esame la settimana con più recensioni -> 5-11, 12-11.

Il processo di estrazione è formato dalle seguenti fasi:
  
   1. Preprocessing delle reviews all'interno della collection reviews:
      *  ### Misspelt Words: libreria python -> https://github.com/fsondej/autocorrect
         Controllo ortografico su tutte le recensioni, la libreria utilizzata implementa l'algortimo della distanza di Levenshtein.
      
      *  ### Stopwords Removal and Stemming: libreria python -> https://www.nltk.org/
         Successivamente le recensioni sono state sottoposte ad un processo di tokenizzazione, ossia la divisione della stringa in un elenco di token.
         Il processo di Stemming rimuove informazioni inutili dai token, in modo tale da ottenere parole chiavi al fine di migliorare la ricerca.
            
      *  ### Sentiment Analysis: libreria python -> https://github.com/cjhutto/vaderSentiment
         Infine, le reviews sono state sottoposte all'analisi del sentimento con il filtro Vader.

### Tools

scripts/reviewsOperations.py: contiene lo script py con tutte le operazioni di preprocessing.

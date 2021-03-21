# Tesi di Michele Sergola

| Resource | DOI |
|:---:|:---:|
|Dataset| [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3653367.svg)](https://doi.org/10.5281/zenodo.3653367)|

Il Dataset è composto da metadati delle app estratti settimanalmente, per 4 differenti Paesi, durante 30 settimane.
Di queste 30 settimane, ho preso in esame la settimana con più recensioni -> 5-11, 12-11.

Il Dataset è stato analizzato con la libreria python Pandas -> https://pandas.pydata.org/

Il processo di estrazione è formato dalle seguenti fasi:
  
   1. Preprocessing delle reviews all'interno della collection reviews:
      *  ### Misspelt Words: libreria python -> https://github.com/fsondej/autocorrect
         Controllo ortografico su tutte le recensioni, la libreria utilizzata implementa l'algortimo della distanza di Levenshtein.
      
      *  ### Stopwords Removal and Stemming: libreria python -> https://www.nltk.org/
         Successivamente le recensioni sono state sottoposte ad un processo di tokenizzazione, ossia la divisione della stringa in un elenco di token.
         Il processo di Stemming rimuove informazioni inutili dai token, in modo tale da ottenere parole chiavi al fine di migliorare la ricerca.
            
      *  ### Sentiment Analysis: libreria python -> https://github.com/cjhutto/vaderSentiment
         Infine, le reviews sono state sottoposte all'analisi del sentimento con il filtro Vader.
         L'analisi è basata sull'indice Compound, se quest'ultimo è <= -0.050, il sentimento risulterà Negativo; mentre nel caso opposto risulterà Positivo.

### Tools

### scripts/reviewsOperations.py:
    contiene lo script py con tutte le operazioni di preprocessing.
    
### scripts/tool.py:
    Tool parametrizzato che prende in input il criterio di ricerca tra quelli proposti, al momento 'privacy' e 'green'.
    Dopo aver analizzato tutte le recensioni sottoposte alla fase di preprocessing, e aver controllato che le parole chiavi relative al criterio selezionato sono presenti nel testo della recensione; restituisce in output una lista di app.

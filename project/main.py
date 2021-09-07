from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, session
from search import SearchForm
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from joblib import load
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ffdc87c1b10666a30c66d1b18b3aa6b5'
positive_count = 0
negative_count = 0
positive_count_knn = 0
negative_count_knn = 0
keywords_list = []
knn_neighbors = []


@app.route('/')
@app.route('/home')
def index():
    session.pop('results', None)
    session.pop('knn', None)
    return render_template('home.html', title='Tesi')


@app.route('/neighbors', methods=['GET', 'POST'])
def neighbors():
    global knn_neighbors
    if request.method == 'POST' or 'knn' in session:
        if 'knn' in session:
            knn_neighbors = session['knn']
        else:
            app_name = request.form['knn']
            #Mindroid PRO Unlock
            #com.urbandroid.mind.unlock
            df = pd.read_csv('data_processed/rangeLdaProcessed.csv', delimiter=';')
            #Cerco la app inserita nel csv e salvo il relativo lda_result
            for index, name in enumerate(df['id.1']):
                if name == app_name:
                    lda_app = df['lda_result'][index]

            lda_from_csv = eval(lda_app)
            model = load('data_processed/training_kneighbors.pickle')

            #predict
            preds = model.kneighbors([lda_from_csv], 10, True)
            #print(preds[1][0][0])
            #print(len(preds[1][0]))

            #save apps from preds
            #preds[1][0][0]
            predictions = []
            #print(range(len(preds[1][0])))
            for elem in range(len(preds[1][0])):
                predictions.append(preds[1][0][elem])

            #print(predictions)

            #take the 10 apps_name from the predictions
            k_neighbors = []
            for idx, name in enumerate(df['name']):
                for i in predictions:
                    if i == idx:
                        k_neighbors.append(name)

            print('k neighbros = ', k_neighbors)
            print('k neighbros = ', len(k_neighbors))

            #Estract reviews with sentiment
            reviews_df = pd.read_csv('data_processed/recensioniRangeProcessed.csv', delimiter=';', low_memory=False)
            global keywords_list

            #print(keywords_list)

            saved_app_name = ''
            isKnn = False
            for z, csv_app_name in enumerate(reviews_df['app_name']):
                for i in k_neighbors:
                    if csv_app_name == i:
                        saved_app_name = csv_app_name
                        isKnn = True

                if isKnn:
                    review = reviews_df['processed_text'][z]
                    isCriteria = False
                    try:
                        for j, word in enumerate(keywords_list):
                            if word in review:
                                isCriteria = True
                    except Exception:
                        continue

                    if isCriteria:
                        sentiment = reviews_df['vader_sentiment'][z]
                        sum_sentiment_knn(sentiment)

                    #condizione di uscita
                    if z == len(reviews_df) - 1:
                        next_app_name = reviews_df['app_name'][z]
                    else:
                        next_app_name = reviews_df['app_name'][z + 1]

                    if saved_app_name != next_app_name:
                        global positive_count_knn
                        global negative_count_knn

                        isduplicated = False
                        for y in knn_neighbors:
                            key = y['app_name']
                            if saved_app_name == key:
                                isduplicated = True
                            else:
                                continue

                        if not isduplicated:
                            data_set = {"app_name": saved_app_name, "pos": positive_count_knn, "neg": negative_count_knn}
                            knn_neighbors.append(data_set)

                        positive_count_knn = 0
                        negative_count_knn = 0
                        isKnn = False

            print(knn_neighbors)
            print(len(knn_neighbors))
            session['knn'] = knn_neighbors
    else:
        knn_neighbors = []
    return render_template('neighbors.html', title='Neighbors', knn_neighbors=knn_neighbors)


def sum_sentiment_knn(sentiment):
    global positive_count_knn
    global negative_count_knn
    if sentiment == 'positive':
        positive_count_knn += 1
    else:
        negative_count_knn += 1


@app.route('/results')
def results():
    values = ''
    global keywords_list
    processed_keywords = stem_keywords(keywords_list)
    apps_list = api_apps(processed_keywords)

    if len(apps_list) == 0:
        values = 'No apps were found'
    return render_template('results.html', title='Search', apps_list=apps_list, values=values)


@app.route('/remove/<string:keyword>', methods=['GET', 'POST'])
def remove(keyword):
    if request.method == 'POST':
        global keywords_list
        keywords_list.remove(keyword)
        session['results'] = keywords_list
        return redirect(url_for('search'))
    return ''


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        keyword = request.form['keyword']
        global keywords_list
        keywords_list.append(keyword)
        session['results'] = keywords_list
        return redirect(url_for('search'))
    return ''


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    global keywords_list
    keywords_list = ''
    values = ''
    novalues = ''
    hide_form = True
    if request.method == 'POST' or 'results' in session:
        if 'results' in session:
            keywords_list = session['results']
            hide_form = False
            values = len(keywords_list)
        else:
            if form.validate_on_submit():
                criteria = request.form.get('criteria')
                keywords_list = keywords(criteria)
                hide_form = False
                values = len(keywords_list)
                if values == 0:
                    novalues = 'No keywords were found!'

    return render_template('search.html', title='Search', form=form, keywords_list=keywords_list,
                           values=values,
                           novalues=novalues,
                           hide_form=hide_form)


def keywords(criteria):
    filter_selected_list = list_keywords(criteria)
    return filter_selected_list


def stem_keywords(keywords):
    keywords_processed = []
    ps = PorterStemmer()
    for idx, key in enumerate(keywords):
        keywords_processed.append(ps.stem(key))

    keywords_processed = list(dict.fromkeys(keywords_processed))
    return keywords_processed


def api_apps(processed_keywords):
    reviews_processed_df = pd.read_csv('data_processed/recensioniRangeProcessed.csv', delimiter=';', low_memory=False)
    final_list = []

    for index, row in enumerate(reviews_processed_df['processed_text']):
        try:
            isFilter = analyze_filter(processed_keywords, row)
        except Exception:
            continue
        if isFilter:
            sentiment = reviews_processed_df['vader_sentiment'][index]
            app_name = reviews_processed_df['app_name'][index]
            sum_sentiment(sentiment)
            if index == len(reviews_processed_df) - 1:
                next_app_name = ''
            else:
                next_app_name = reviews_processed_df['app_name'][index + 1]
            if app_name == next_app_name:
                continue
            else:
                global positive_count
                global negative_count

                isduplicated = False
                for y in final_list:
                    key = y['app_name']
                    if app_name == key:
                        isduplicated = True
                    else:
                        continue

                if not isduplicated:
                    data_set = {"app_name": app_name, "pos": positive_count, "neg": negative_count}
                    final_list.append(data_set)

                positive_count = 0
                negative_count = 0

    return final_list


def list_keywords(input):
    list_keywords_processed = []
    syns = wordnet.synsets(input)
    for idx, word in enumerate(syns):
        key = word.lemma_names()
        for name in key:
            if name != '':
                list_keywords_processed.append(name)
            else:
                continue

    list_keywords_processed = list(dict.fromkeys(list_keywords_processed))
    return list_keywords_processed


def analyze_filter(selected_list, text):
    for index, word in enumerate(selected_list):
        if word in text:
            return True

    return False


def sum_sentiment(sentiment):
    global positive_count
    global negative_count
    if sentiment == 'positive':
        positive_count += 1
    else:
        negative_count += 1


if __name__ == '__main__':
    app.run(debug=True)

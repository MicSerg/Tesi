import pandas as pd
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from six.moves import input
import inquirer

privacy = 'privacy'
green = 'green'


def privacy_keywords():
    ps = PorterStemmer()
    privacy_list = ['Access', 'Aggregate', 'Allow', 'Apply', 'Avoid', 'Block', 'Change', 'Choose', 'Collect',
                    'Comply', 'Connect', 'Consolidate', 'Contact', 'Contract', 'Customize', 'Deny', 'Destroy',
                    'Disallow', 'Discipline', 'Disclaim', 'Disclose', 'Display', 'Enforce', 'Ensure', 'Exchange',
                    'Help', 'Honor', 'Imply', 'Inform', 'Limit', 'Maintain', 'Make', 'Maximize', 'Minimize', 'Monitor',
                    'Notify', 'Obligate', 'Opt-in', 'Opt-out', 'Investigate', 'Post', 'Prevent', 'Prohibit',
                    'Protect', 'Provide', 'Recommend', 'Request', 'Require', 'Reserve', 'Review', 'Share', 'Specify',
                    'Store', 'Update', 'Urge', 'Use', 'Verify']
    privacy_list_processed = []

    for idx, word in enumerate(privacy_list):
        privacy_list_processed.append(ps.stem(word))

    return privacy_list_processed


def green_keywords():
    ps = PorterStemmer()
    green_list = ['Innovation', 'Climate', 'Conservation', 'Solar', 'Recycling', 'Health', 'Social',
                  'Civilization', 'Garden', 'Ecology', 'Planet', 'Sustainability', 'Environmentally',
                  'Safe', 'Green']
    green_list_processed = []

    for idx, word in enumerate(green_list):
        green_list_processed.append(ps.stem(word))
    return green_list_processed


def analyze_filter(selected_list, text):
    for index, word in enumerate(selected_list):
        if word in text:
            return True

    return False


questions = [
    inquirer.List('criterio',
                  message="Scegli il criterio di ricerca del tool tra quelli proposti",
                  carousel=True,
                  choices=['green', 'privacy'],
                  ),
]
filter_input = inquirer.prompt(questions)['criterio']

reviews_processed_df = pd.read_csv('data/processed/recensioniRangeProcessed.csv', delimiter=';', low_memory=False)

filter_selected_list = []
app_list = []

if filter_input == privacy:
    filter_selected_list = privacy_keywords()
elif filter_input == green:
    filter_selected_list = green_keywords()

for index, row in enumerate(reviews_processed_df['processed_text']):
    try:
        isFilter = analyze_filter(filter_selected_list, row)
    except Exception:
        continue
    if isFilter:
        app_name = reviews_processed_df['app_name'][index]
        app_list.append(app_name)

app_list = list(dict.fromkeys(app_list))
if len(app_list) > 0:
    print("Lista di app: {}".format(app_list))

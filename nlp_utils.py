import string
from nltk.corpus import stopwords
from deeppavlov.core.common.file import read_json
from deeppavlov import build_model, configs
from deeppavlov.models.tokenizers import ru_tokenizer


spec_chars = string.punctuation + '\n\xa0«»\t—…'

russian_stopwords = stopwords.words("russian")


def tokenize(text):
    text = "".join([ch for ch in text if ch not in spec_chars])

    ru_processor = ru_tokenizer.RussianTokenizer(stopwords=russian_stopwords, lowercase=True, lemmas=True)
    lemmatizer = ru_processor.lemmatizer
    tokenizer = ru_processor.tokenizer

    result = tokenizer.tokenize(text)

    lemmas = []
    for word in result:
        lemmas.append(lemmatizer.normal_forms(word)[0])
    return lemmas


def vectorize(text):
    rubert_path = '/Users/dapodshivalov/.deeppavlov/downloads/bert_models/multi_cased_L-12_H-768_A-12_pt'
    bert_config = read_json(configs.embedder.bert_embedder)
    bert_config['metadata']['variables']['BERT_PATH'] = rubert_path
    # print(bert_config)

    # m = build_model(bert_config, download=True)
    m = build_model(bert_config)

    tokens, token_embs, subtokens, subtoken_embs, sent_max_embs, sent_mean_embs, bert_pooler_outputs = m([text])
    return sent_mean_embs[0]
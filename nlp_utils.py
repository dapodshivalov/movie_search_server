import tensorflow.compat.v2 as tf
import tensorflow_hub as hub
from tensorflow_text import SentencepieceTokenizer
from razdel import sentenize


class NlpUtils:
    def __init__(self):
        module_url = 'https://tfhub.dev/google/universal-sentence-encoder-multilingual/3'
        self.model = hub.load(module_url)

    def text_to_sentences(self, text: str) -> [str]:
        return [s.text for s in list(sentenize(text))]

    def sentence_to_vector(self, sentence: str) -> [float]:
        return self.model([sentence]).numpy()[0]

    def sentences_to_vectors(self, sents: [str]) -> [[float]]:
        return self.model(sents).numpy()

    def text_to_vectors(self, text: str) -> [[float]]:
        sentences = self.text_to_sentences(text)
        return self.sentences_to_vectors(sentences)


if __name__ == '__main__':
    query = 'Ты че в натуре'
    print(NlpUtils().sentence_to_vector(query))
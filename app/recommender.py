import pandas as pd
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# def info(msg):
#     current_app.logger.info(msg)


class ContentEngine(object):

    SIMKEY = 'p:smlr:%s'
    similars = dict()
    # def __init__(self):
    #     self._r = redis.StrictRedis.from_url(current_app.config['REDIS_URL'])

    def train(self, data_source):
        start = time.time()
        ds = pd.read_csv(data_source)
        d = (ds[['title', 'author', 'url', 'poem', 'tags', 'source']])
        drop = []
        for i in range(0, len(d)):
            if type(d.loc[i]['poem']) is float:
                drop.append(i)
                continue
            elif len(d.loc[i]['poem']) > 5120:
                # print(i)
                # print(d.loc[i]['title'])
                drop.append(i)
            elif len(d.loc[i]['title']) > 128:
                drop.append(i)
        ready_data = d.drop(d.index[drop]).rename(columns={'author': 'poet', 'poem': 'text'})

        ready_data = ready_data.reset_index()
        ready_data['id'] = range(len(ready_data))
        # print(ready_data)
        #
        # print(len(ready_data))
        print("Training data ingested in %s seconds." % (time.time() - start))

        # Flush the stale training data from redis
        # self._r.flushdb()

        start = time.time()
        self._train(ready_data)
        print("Engine trained in %s seconds." % (time.time() - start))

    def _train(self, ds):
        """
        Train the engine.

        Create a TF-IDF matrix of unigrams, bigrams, and trigrams
        for each product. The 'stop_words' param tells the TF-IDF
        module to ignore common english words like 'the', etc.

        Then we compute similarity between all products using
        SciKit Leanr's linear_kernel (which in this case is
        equivalent to cosine similarity).

        Iterate through each item's similar items and store the
        100 most-similar. Stops at 100 because well...  how many
        similar products do you really need to show?

        Similarities and their scores are stored in redis as a
        Sorted Set, with one set for each item.

        :param ds: A pandas dataset containing two fields: description & id
        :return: Nothin!
        """

        tf = TfidfVectorizer(analyzer='word',
                             ngram_range=(1, 3),
                             min_df=0,
                             stop_words='english')
        # print(ds['text'])
        tfidf_matrix = tf.fit_transform(ds['text'])

        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
        for idx, row in ds.iterrows():
            # print("INDEX: " + str(idx))
            # print("ROW: " + str(row))
            # if (idx == 1):
            #     print(row)
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            # print(similar_indices)
            similar_items = [(cosine_similarities[idx][i], ds['title'][i])
                             for i in similar_indices]

            # First item is the item itself, so remove it.
            # This 'sum' is turns a list of tuples into a single tuple:
            # [(1,2), (3,4)] -> (1,2,3,4)
            flattened = sum(similar_items[1:], ())
            ret = []
            for i in range(0, len(flattened) - 1, 2):
                ret.append((flattened[i], flattened[i+1]))
            # self._r.zadd(self.SIMKEY % row['id'], *flattened)
            self.similars[row['title']] = ret

    def predict(self, poem, num):
        """
        Couldn't be simpler! Just retrieves the similar items and
        their 'score' from redis.

        :param item_id: string
        :param num: number of similar items to return
        :return: A list of lists like: [["19", 0.2203],
        ["494", 0.1693], ...]. The first item in each sub-list is
        the item ID and the second is the similarity score. Sorted
        by similarity score, descending.
        """
        ret = self.similars[poem]
        retCount = num
        if len(ret) < num:
            retCount = len(ret)
        return ret[0:retCount]
        # return self._r.zrange(self.SIMKEY % item_id,
        #                       0,
        #                       num-1,
        #                       withscores=True,
        #                       desc=True)


content_engine = ContentEngine()






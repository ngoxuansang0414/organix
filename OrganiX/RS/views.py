from store.models.products import Product
from store.models.description import Description
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

def content_based_RS():
    products = Product.objects.all()
    descriptions = Description.objects.all()

    df = pd.DataFrame(list(descriptions.values_list('product_id', 'uses')), columns=['product_id', 'uses'])
    
    
    my_stop_words = ["là", "của", "và", "nhưng", "hay", "hoặc", "tôi", "bạn", "mình", "họ", "nó", "rất", "quá", "lắm", "không", "có", "làm", "được", "tốt", "xấu"]
    tfv = TfidfVectorizer(min_df=3, max_features=None,
                        strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                        ngram_range=(1, 3),
                        stop_words=my_stop_words)
    # Filling NaNs with empty string
    df['uses'] = df['uses'].fillna('')

    # Fitting the TF-IDF on the 'uses' text
    tfv_matrix = tfv.fit_transform(df['uses'])

    # Compute the sigmoid kernel
    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

    
    indices = pd.Series(df.index, index=df['product_id']).drop_duplicates()
    def give_rec(product_id, sig=sig):
        # Get the index corresponding to product_id
        idx = indices[product_id]

        # Get the pairwise similarity scores
        sig_scores = list(enumerate(sig[idx]))

        # Sort the products uses
        sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

        # Scores of the 10 most similar products
        sig_scores = sig_scores[1:11]

        # Uses indices
        uses_indices = [i[0] for i in sig_scores]

        # Top 10 most similar products
        return df['product_id'].iloc[uses_indices]
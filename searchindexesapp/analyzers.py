from elasticsearch_dsl import analyzer, tokenizer
from django_elasticsearch_dsl_drf.versions import ELASTICSEARCH_GTE_7_0

__all__ = ("html_strip",)

# The ``standard`` filter has been removed in Elasticsearch 7.x.
if ELASTICSEARCH_GTE_7_0:
    _filters = ["lowercase", "stop", "snowball", "asciifolding"]
else:
    _filters = ["standard", "lowercase", "stop", "snowball", "asciifolding"]

html_strip = analyzer(
    "html_strip", tokenizer="lowercase", filter=_filters, char_filter=["html_strip"]
)


custom_analyzer = analyzer(
    "custom_analyzer",
    tokenizer=tokenizer("trigram", "ngram", min_gram=3, max_gram=3),
    filter=_filters,
)

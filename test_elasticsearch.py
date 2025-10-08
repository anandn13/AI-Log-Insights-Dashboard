from services import elasticsearch_client as esc


def test_index_exists():
    assert esc.es.indices.exists(index=esc.ES_INDEX)



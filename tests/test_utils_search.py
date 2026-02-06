from dateno_cmd.utils.search import extract_doc_from_item, extract_hits_list


def test_extract_hits_list_hits_dict():
    data = {"hits": {"hits": [{"_source": {"id": "1"}}]}}
    items = extract_hits_list(data)
    assert len(items) == 1


def test_extract_hits_list_hits_list():
    data = {"hits": [{"_source": {"id": "2"}}]}
    items = extract_hits_list(data)
    assert len(items) == 1


def test_extract_hits_list_data_list():
    data = {"data": [{"id": "3"}]}
    items = extract_hits_list(data)
    assert len(items) == 1


def test_extract_doc_from_item_source():
    item = {"_source": {"id": "1"}}
    assert extract_doc_from_item(item) == {"id": "1"}


def test_extract_doc_from_item_document():
    item = {"document": {"id": "2"}}
    assert extract_doc_from_item(item) == {"id": "2"}


def test_extract_doc_from_item_dataset():
    item = {"dataset": {"title": "t"}}
    assert extract_doc_from_item(item) == item

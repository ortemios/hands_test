import pytest
from model.method import Method
from model.resource import Resource


@pytest.fixture
def repetitors_resource():
    return Resource(url='https://repetitors.info')


@pytest.fixture
def hands_resource():
    return Resource(url='https://hands.ru/company/about')


@pytest.fixture
def hands_resource_dynamic():
    return Resource(
        url='https://hands.ru/graphql/batch',
        method=Method.POST,
        headers={'Content-Type': 'application/json'},
        body='[{"operationName": "handsRuGetCallCenterPhone", "variables": {}, "query": "query handsRuGetCallCenterPhone {\\n  callCenterPhone\\n}\\n"}]'
    )

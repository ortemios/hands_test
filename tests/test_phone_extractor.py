import pytest
from service.phone_extractor import PhoneExtractor


@pytest.mark.asyncio
async def test_repetitors(repetitors_resource):
    assert await PhoneExtractor().extract_phones_from_resources([repetitors_resource]) == {'84955405676', '84445535400'}


@pytest.mark.asyncio
async def test_hands(hands_resource):
    assert await PhoneExtractor().extract_phones_from_resources([hands_resource]) == {'82194524421', '86824209892'}


@pytest.mark.asyncio
async def test_hands_dynamic(hands_resource_dynamic):
    assert await PhoneExtractor().extract_phones_from_resources([hands_resource_dynamic]) == {'84951370720'}


@pytest.mark.asyncio
async def test_all_resources(repetitors_resource, hands_resource, hands_resource_dynamic):
    assert await PhoneExtractor().extract_phones_from_resources([
        repetitors_resource,
        hands_resource,
        hands_resource_dynamic
    ]) == {
        '84955405676',
        '84445535400',
        '82194524421',
        '86824209892',
        '84951370720'
    }

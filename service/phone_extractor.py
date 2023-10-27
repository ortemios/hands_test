import asyncio
import re
import aiohttp
from bs4 import BeautifulSoup
from model.method import Method
from model.resource import Resource


class PhoneExtractor:

    async def extract_phones_from_resources(self, resources: list[Resource]) -> set[str]:
        result = await asyncio.gather(*[self._task(res) for res in resources])
        return set().union(*map(set, result))

    async def _task(self, resource: Resource) -> list[str]:
        print(f'Поиск на {resource.url} . . .')
        content = await self._get_resource_content(resource)
        found = self._extract_phones_from_text(content)
        print(f'Найдено на {resource.url} - {", ".join(found)}')
        inner_resources = self._extract_resources_from_html_content(resource, content)
        found += await self.extract_phones_from_resources(inner_resources)
        return found

    def _extract_phones_from_text(self, text: str) -> list[str]:
        pattern = r'(\+7|8)(\s|-)?(\()?(\d{3})(\)?)(\s|-)?(\d{3})(\s|-)?(\d{2})(\s|-)?(\d{2})'
        return list(map(
            lambda t: self._format_phone(''.join(t)),
            re.findall(pattern, text)
        ))

    def _format_phone(self, phone: str) -> str:
        return '8' + ''.join(filter(lambda c: c.isdigit(), phone))[1:]

    def _extract_resources_from_html_content(self, parent: Resource, content: str) -> list[Resource]:
        soup = BeautifulSoup(content, 'html.parser')
        script_tags = soup.find_all('script')
        resources = []
        for script_tag in script_tags:
            if script_tag.has_attr('src'):
                url: str = script_tag['src']
                if not url.startswith('http'):
                    url = parent.url + url
                resources.append(Resource(url=url))
        return resources

    async def _get_resource_content(self, resource: Resource) -> str:
        async with aiohttp.ClientSession(headers=resource.headers) as session:
            if resource.method == Method.POST:
                request = session.post(url=resource.url, data=resource.body)
            else:
                request = session.get(url=resource.url)
            response = await request
            return await response.text()

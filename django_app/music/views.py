import json
from pprint import pprint

import requests
from django.shortcuts import render, redirect

from music_share.settings import config


def search_from_deezer(keyword, page_token=None):
    deezer_api_key = config['django']['secret_key']
    params = {
        'q': keyword,
        'maxResults': 20,
        'type': 'artist',
        'key': deezer_api_key,
    }

    if page_token:
        params['pageToken'] = page_token

    r = requests.get('https://api.deezer.com/2.0/search?q=', params=params)
    result = r.text

    # 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
    result_dict = json.loads(result)
    return result_dict


def search(request):
    musics = []
    context = {
        'musics': musics,
    }

    keyword = request.GET.get('keyword', '').strip()
    page_token = request.GET.get('page_token')

    if keyword != '':
        # 검색 결과를 받아옴
        search_result = search_from_deezer(keyword, page_token)

        # 검색결과에서 이전/다음 토큰, 전체 결과 개수를 가져와
        # 템플릿에 전달할 context객체에 할당
        next_page_token = search_result.get('nextPageToken')
        prev_page_token = search_result.get('prevPageToken')
        # total_results = search_result['pageInfo'].get('totalResults')
        context['next_page_token'] = next_page_token
        context['prev_page_token'] = prev_page_token
        # context['total_results'] = total_results
        context['keyword'] = keyword

        # 검색결과에서 'items'키를 갖는 list를 items변수에 할당 후 loop
        items = search_result['data']
        pprint(items)
        for item in items:
            # 실제로 사용할 데이터
            title = item['title']
            preview = item['preview']
            picture = item['album']['cover_small']

            cur_item_dict = {
                'title': title,
                'preview': preview,
                'picture': picture,
            }
            musics.append(cur_item_dict)

    return render(request, 'music/search.html', context)

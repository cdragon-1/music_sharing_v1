import json
from pprint import pprint

import requests
from django.shortcuts import render, redirect

from music_share.settings import config
from utils.settings import get_setting
from music.models import Music


def search_from_deezer(keyword, page_token=None):
    deezer_api_key = config['django']['secret_key']
    # 3. requests 라이브러리를 이용(pip install requests), GET요청으로 데이터를 받아온 후
    # 이렇게 Parameter와 URL을 분리합니다
    params = {
        'q': keyword,
        # 'maxResults': 15,
        'type': 'artist',
        'key': deezer_api_key,
    }
    # 페이지 토큰값이 전달되었을 때만 params에 해당 내용을 추가해서 요청
    if page_token:
        params['pageToken'] = page_token

    r = requests.get('https://api.deezer.com/2.0/search?q=', params=params)
    pprint('r:{}'.format(r))
    result = r.text

    # 4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
    result_dict = json.loads(result)
    # print('result_dict:{}'.format(result_dict))
    return result_dict


def search(request):
    # print(request.path_info)
    # print(request.get_full_path())

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
            deezer_id = item['id']
            title = item['title']
            # description = item['snippet']['description']
            # published_date = parse(published_date_str)
            # url_thumbnail = item['snippet']['thumbnails']['high']['url']
            # 이미 북마크에 추가된 영상인지 판단
            # is_exist = BookmarkVideo.objects.filter(
            #     user=request.user,
            #     video__youtube_id=youtube_id
            # ).exists()

            # 현재 item을 dict로 정리
            cur_item_dict = {
                'title': title,
                # 'description': description,
                # 'published_date': published_date,
                # 'youtube_id': youtube_id,
                # 'url_thumbnail': url_thumbnail,
                # 'is_exist': is_exist,
            }
            musics.append(cur_item_dict)

    return render(request, 'music/search.html', context)

### === 프로그램 실행을 위한 사전 작업 ===
import requests
from bs4 import BeautifulSoup

"""
필요한 함수들 선언해두는 부분

find_matching() # 품종명을 입력받아 그 품종의 url 경로를 반환
breed_keword() # 키워드가 존재하는 품종에 한해서만 호출
definition_long() # 상세한 세부 사항을 가진 품종에 한해서만 호출
"""

def find_matching(string_list, target_string):
    target_string = target_string.lower()
    max_match_count = 0
    most_matching = None

    for element in string_list:
        if  target_string in element:
            most_matching = element
            break
        else:
            cur_match_count = sum(1 for char in element if char in target_string)

        if cur_match_count > max_match_count:
            max_match_count = cur_match_count
            most_matching = element

    return most_matching

def breed_keyword(soup):
    keyword = []
    for key_data in soup.find("dl", {"class": "definition-list"}).next_siblings:
        if key_data == '\n':
            continue
        keyword.append(key_data.text.strip())

    keyword = ''.join(keyword)

    return keyword

def definition_long(url):
    soup_for_div = BeautifulSoup(url.text.split('div class="rc-column')[9], "html.parser")
    div = soup_for_div.find("div")
    span = div.select("span")
    td = div.select("tr > td")[-1].get_text().strip()

    span_list = [list.get_text().replace('\n', '').strip() for list in span if list.get_text() != '']

    str_keys = [list for i, list in enumerate(span_list) if i % 2]
    str_vals = [list for i, list in enumerate(span_list) if not i % 2]
    
    str_vals[2] = str_vals[0] + ' / ' + str_vals[2]
    str_vals[3] = str_vals[1] + ' / ' + str_vals[3]

    definition = dict(zip(str_keys, str_vals))

    print("\n== 세부 사항(수컷 / 암컷) ==")
    for key, value in definition.items():
        print(f"{key}: {value}")
    print(f"평균 기대 수명: {td}")


### 75개 품종 리스트
breed_list = ['affenpinscher', 
              'afghan-hound',
              'airedale-terrier',
              'american-staffordshire-terrier',
              'appenzell-cattle-dog',
              'australian-terrier', 
              'basenji', 
              'beagle',
              'bedlington-terrier',
              'bernese-mountain-dog',
              'black-and-tan-coonhound',
              'bloodhound',
              'border-collie',
              'border-terrier',
              'borzoi',
              'bouvier-des-flanders',
              'boxer',
              'briard',
              'brittany-spaniel',
              'bullmastiff',
              'welsh-corgi-cardigan', # Cardigan in dataset
              'chesapeake-bay-retriever',
              'chihuahua',
              'clumber-spaniel',
              'dandie-dinmont-terrier',
              'dobermann',
              'english-foxhound',
              'english-setter',
              'french-bulldog',
              'german-shepherd',
              'golden-retriever',
              'gordon-setter',
              'great-dane',
              'great-swiss-mountain-dog',
              'irish-terrier',
              'irish-wolfhound',
              'italian-greyhound',
              'kerry-blue-terrier',
              'komondor',
              'kuvasz',
              'labrador-retriever',
              'lakeland-terrier',
              'leonberger',
              'lhasa-apso',
              'alaskan-malamute', # malamute in dataset
              'maltese',
              'miniature-pinscher',
              'miniature-schnauzer',
              'newfoundland',
              'norfolk-terrier',
              'norwegian-elkhound',
              'norwich-terrier',
              'old-english-sheepdog',
              'otterhound',
              'welsh-corgi-pembroke', # Pembroke in dataset
              'pomeranian',
              'pug',
              'rhodesian-ridgeback',
              'rottweiler',
              'st-bernard',
              'saluki',
              'samoyed',
              'schipperke',
              'scottish-terrier',
              'sealyham-terrier',
              'shetland-sheepdog',
              'siberian-husky',
              'sussex-spaniel',
              'tibetan-mastiff',
              'tibetan-terrier',
              'weimaraner',
              'welsh-springer-spaniel',
              'west-highland-white-terrier',
              'whippet',
              'yorkshire-terrier']

def run_guide(breed) :
    # 품종명 입력 지점
    breed = breed.replace('_', '-')

    # URL 획득
    url = requests.get("https://www.royalcanin.com/kr/dogs/breeds/breed-library/" + find_matching(breed_list, breed))

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(url.text, 'html.parser')
    ### ====================================


    # 개요 크롤링
    nav = soup.select_one("nav.rc-progress")
    breed = nav.find("a", {"class": "rc-progress__breadcrumb--current"}).get_text()

    title = []
    for data in soup.find("h1", {"class": "rc-alpha"}).next_siblings:
        if data == '\n':
            continue
        title.append(data.text.strip())

    del title[1:]
    title = ''.join(title)

    print(f"== [{breed}] ==")
    print(title)


    # 소개 크롤링
    info = []
    for data in soup.find("h2", {"class": "rc-beta"}).next_siblings:
        if data == '\n':
            continue
        info.append(data.text.strip())

    info.pop(-1)
    info = ''.join(info).replace('. ', '.').replace('.', '. ')

    print("\n== 품종 소개 ==")
    print(info)


    # 세부 사항 크롤링
    if soup.find("dl", {"class": "definition-list"}) != None:
        dl = soup.select_one("dl.definition-list")
        dl_keys = dl.select('dt')
        dl_vals = dl.select('dd')

        str_keys = [key.get_text() for key in dl_keys]
        str_vals = [val.get_text() for val in dl_vals]

        print("\n== 성향 키워드 ==")
        print(breed_keyword(soup))

        definition = dict(zip(str_keys, str_vals))

        print("\n== 세부 사항 ==")
        for key, value in definition.items():
            print(f"{key}: {value}")
    else:
        definition_long(url)


    # 유의할 점 크롤링
    if soup.find("ul", {"class": "rc-list--large-icon"}) != None:
        ul = soup.select_one("ul.rc-list--large-icon")
        res = ul.select('li')
    else:
        div2 = soup.find("div", {"class", "paragraphs-in-two-columns"})
        res = div2.select("h2")

    notes = [list.get_text().strip() for list in res]

    print("\n== 유의할 점 ==")
    for i in range(len(notes)):
        print(f"- {notes[i]}")

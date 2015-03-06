from selenium import webdriver
import tools.fuzzywuzzy.fuzz as match
import utils
import mp3_tools

def metro_lyric_format(str):
    return utils.normalize_string(str).lower().replace(' ', '+')

def search(artist, album, song):
    lyrics = None

    url = 'http://www.metrolyrics.com/search.html?search=' + metro_lyric_format(artist + " " + song)
    driver = webdriver.Firefox()
    driver.get(url)
    driver.implicitly_wait(10)

    try:
        match_ratio = 0
        match_text = artist.upper() + " " + song.upper()
        print("Looking for: {}".format(match_text))
        best_match = None

        for i in range(1, 6):
            link = driver.find_element_by_xpath('//div[@class="songs clearfix"]/descendant::div[@class="content clearfix"]/*[{}]/li/a'.format(i))
            link_text = link.text.replace('\n', ' ').upper()
            curr_match_ratio = match.ratio(link_text, match_text)
            if curr_match_ratio > match_ratio:
                match_ratio = curr_match_ratio
                best_match = link
            print("Looking at: {}\twith Score of: {}".format(link_text, curr_match_ratio))

        print("Best match: {}".format(best_match.text.replace('\n', ' ')))
        best_match.click()
        lyrics_container = driver.find_element_by_id('lyrics-body-text')
        lyrics = lyrics_container.text

    finally:
        driver.quit()

    return lyrics

def search_by_file_name(file_name):
    artist, album, song = mp3_tools.extractInfo(file_name)
    print("Artist: {}\tAlbum: {}\t Song: {}".format(artist, album, song))
    lyrics = search(artist, album, song)
    return lyrics
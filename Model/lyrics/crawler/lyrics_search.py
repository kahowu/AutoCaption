from selenium import webdriver
import tools.fuzzywuzzy.fuzz as match
import utils
import mp3_tools

def metro_lyric_format(str):
    return utils.normalize_string(str).lower().replace(' ', '+')

def selenium_search(driver, url, artist, song):
    driver.get(url)

    see_more = driver.find_element_by_xpath('//div[@class="songs clearfix"]/descendant::action[@class="action more-link"]')
    see_more.click()

    match_ratio = 0
    match_text = artist.upper() + " " + song.upper()

    best_match = None

    print("Looking for: {}".format(match_text))
    for i in range(1, 51):
        link = driver.find_element_by_xpath('//div[@class="songs clearfix"]/descendant::div[@class="content clearfix"]/*[{}]/li/a'.format(i))
        link_text = link.text.replace('\n', ' ').upper().encode('ascii', 'ignore')
        curr_match_ratio = match.ratio(link_text, match_text)
        if curr_match_ratio > match_ratio:
            match_ratio = curr_match_ratio
            best_match = link

    print("Best match: {}".format(best_match.text.replace('\n', ' ')))
    best_match.click()
    lyrics_container = driver.find_element_by_id('lyrics-body-text')
    lyrics = lyrics_container.text
    return lyrics

def search(artist, album, song):
    lyrics = None

    url = 'http://www.metrolyrics.com/search.html?search=' + metro_lyric_format(artist + " " + song)

    print("URL: {}".format(url))

    driver = webdriver.Firefox()
    driver.implicitly_wait(15)

    for i in range(4):
        if (i > 0):
            print("Trying again.")
        try:
            lyrics = selenium_search(driver, url, artist, song)
            driver.quit()
            return lyrics
        except:
            print("Failed.")

    driver.quit()
    return lyrics

def search_by_file_name(file_name):
    artist, album, song = mp3_tools.extractInfo(file_name)
    print("Artist: {}\tAlbum: {}\t Song: {}".format(artist, album, song))
    lyrics = search(artist, album, song)
    return lyrics
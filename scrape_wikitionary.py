from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import os, sys


def scrape_wikitionary(url, headless_browser = True, only_with_entry = False):
    """scrape_wikitionary will return a list of on the terms given on the site

    Args:
        url (str): url to wiktionary site
        headless_browser (bool, optional): when True no browser window will opened. Defaults to True.
        only_with_entry (bool, optional): Expressions without own wikitionary enty will be ignored for term_list. Defaults to False.

    Returns:
        list: list of (str) terms
    """
    # initialize browser
    browser_options = Options()
    if headless_browser:
        browser_options.headless = True
    directory_of_file = os.path.normpath(sys.argv[0] + os.sep + os.pardir)
    browser_path = directory_of_file + "/geckodriver"
    browser = Firefox(executable_path=browser_path, options=browser_options)
    browser.implicitly_wait(5)

    browser.get(url)

    # define list to store words
    term_list = []

    # get list of paragraph elements
    main_content_element = browser.find_element_by_class_name("mw-parser-output")

    # start parsing at second element because fist one is overview
    for paragraph in main_content_element.find_elements_by_tag_name("ul")[1:]:
        for list_item_element in paragraph.find_elements_by_tag_name("li"):
            try:
                # anker.text is term
                anker_element = list_item_element.find_element_by_tag_name("a")
                class_attr = anker_element.get_attribute("class")

                # if element has wiki entry
                if only_with_entry is True and class_attr == "new":
                    pass
                else:
                    term_list.append(anker_element.text)
            except NoSuchElementException:
                pass

    return term_list

if __name__ == "__main__":
    gruß_url = "https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Gr%C3%BC%C3%9Fen/Begr%C3%BC%C3%9Fungsformeln"
    abschied_url = "https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Gr%C3%BC%C3%9Fen/Abschied"
    falschschreibungen_url = "https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Falschschreibungen"
    feiertage_url = "https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Gr%C3%BC%C3%9Fen/Feste_und_Feiertage"
    print(scrape_wikitionary(gruß_url, headless_browser=False, only_with_entry=True))

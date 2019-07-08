from scraper import Scraper
from bs4 import BeautifulSoup
from lxml import html
from ColorPython import Color, pprint

url = 'https://www.cricbuzz.com/'
scraper = Scraper()

root = html.document_fromstring (scraper.get_html(url))

featured_matches = root.xpath ('''//div[@ng-if="run_active == 'Featured'"]/div/div''')

# print (f"Cricbuzz Featured Matches: {len(featured_matches)}")

for item in featured_matches:
    # print ("-" * 100);
    anchor_tag = item.xpath('./a')[0]
    title = anchor_tag.attrib['title']
    # print (title)
    """
    3 (div) children:
        1st chid: Batting Team and its score
            2 (div) children: first: TEAM NAME, second: TEAM SCORE
        2nd child: Bowling Team and it's Score
            2 (div) children: first: TEAM NAME, second: TEAM SCORE
        3rd child: Toss, Chase Info, Result
    """
    
    counter = 1
    details = []
    summary = ""
    for child in anchor_tag.getchildren():
        """ I am not printing it right here, because of formatting issues: """
        if counter < 3:
            if len( child.getchildren() ) != 0:
                    team, score = [x.text_content() for x in child.xpath ("./div")]

                    # print (f"{team}: {score}")
                    # print ("{:>10}: {:>10}".format (team, score))
                    details.append ({'team': team, 'score': score })
            else:
                team = child.text_content()
                # print (f"{team}: <Not-Available>")
                details.append ({'team': team, 'score': " " })
        else:
            # print (f"\t {child.text_content()}")
            summary = child.text_content()
        counter += 1

    t = max (len (details[0]['team']), len(details[1]['team']))

    lspace = 2
    print (" " * lspace + pprint('cyan', 'bold', title))
    print ( pprint('cyan', 'dim', "*" * (len(title) + 2*lspace)) )
    for entry in details:
        print (" " * lspace + pprint ('purple', 'bold', entry['team'].center(t+2)), end = "")
        print (pprint ('yellow', 'bold', entry['score']))
        # print (f"  {entry['team'].ljust(t+2)}: {entry['score']}")
    print (f"{' ' * (lspace + t)} {pprint('green', 'italic', summary)}")

import scraperwiki
import urlparse
import lxml.html
# scrape_divs function: gets passed an individual page to scrape
def scrape_divs(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    #line below selects all <div class="block size3of4" - note that because there is a space in the value of the div class, we need to put it in inverted commas as a string
    rows = root.cssselect("div.'block size3of4'")  
    for row in rows:
        # Set up our data record - we'll need it later
        print row
        record = {}
        #grab all <h4 tags within our <div
        h2s = row.cssselect("h2")
        #put the text from the first <h4 tags into variable membername
        leads = row.cssselect("p.lead")
        #If there are any, grab the first and put it in the membername variable
        if leads:
            membertitle = leads[0].text
        ps = row.cssselect("p")
        #this line puts the contents of the last <p tag by using [-1]
        memberbiog = ps[-1].text_content()
        record['URL'] = url
        record['Name'] = membername
        record['Title'] = membertitle
        record['Description'] = memberbiog
        print record, '------------'
        # Finally, save the record to the datastore - 'Name' is our unique key
        scraperwiki.sqlite.save(["Name"], record)
        
#list of URLs with similar CMS compiled with this advanced search on Google: inurl:about-us/board.aspx CCG
ccglist = ['www.brentccg.nhs.uk/', 'www.ealingccg.nhs.uk/', 'www.hounslowccg.nhs.uk/', 'www.westlondonccg.nhs.uk/', 'www.centrallondonccg.nhs.uk/', 'www.harrowccg.nhs.uk/', 'www.hammersmithfulhamccg.nhs.uk/']
#loop through the list and for each one, convert into the full URL and run the scrape_divs function created earlier
for ccg in ccglist:
    scrape_divs('http://'+ccg+'about-us/board.aspx')

import scraperwiki
import urlparse
import lxml.html
# scrape_divs function: gets passed an individual page to scrape
def scrape_divs(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    #line below selects all <div class="reveal-modal medium"> - note that because there is a space in the value of the div class, we need to use a space to indicate that
    rows = root.cssselect("div.reveal-modal.medium") 
    for row in rows:
        # Set up our data record - we'll need it later
        print row
        record = {}
        membername = ""
        membertitle = ""
        memberbiog = ""
        h2s = row.cssselect("h2") #grab all <h2> tags within our <div>
        #If there are any, grab the first and put it in the membername variable
        if h2s:
            membername = h2s[0].text
        #repeat process for <p class="lead"> and <p>
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
ccglist = ['www.hounslowccg.nhs.uk/',  'www.centrallondonccg.nhs.uk/', 'www.hammersmithfulhamccg.nhs.uk/']
#'www.ealingccg.nhs.uk/' has similar page but at different URL: http://www.hammersmithfulhamccg.nhs.uk/about-us/our-governing-body.aspx
for ccg in ccglist:
    fullurl = 'http://'+ccg+'about-us/our-governing-body.aspx'
    print 'scraping ', fullurl
    scrape_divs(fullurl)



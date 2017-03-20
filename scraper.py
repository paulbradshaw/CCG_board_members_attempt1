#import our libraries
import scraperwiki
import urlparse
import lxml.html

# create a new function, which gets passed a variable we're going to call 'url'
def scrape_ccg(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    #line below selects all <div class="reveal-modal medium"> - note that because there is a space in the value of the div class, we need to use a space to indicate that
    rows = root.cssselect("div.reveal-modal.medium") 
    for row in rows:
        # Set up our data record - we'll need it later
        print row
        record = {}
        '''membername = ""
        membertitle = ""
        memberbiog = ""'''
        h2s = row.cssselect("h2") #grab all <h2> tags within our <div>
        #If there are any, grab the first and put it in the membername variable
        #if h2s:
        membername = h2s[0].text
        #repeat process for <p class="lead"> 
        leads = row.cssselect("p.lead")
        #If there are any, grab the first and put it in the membername variable
        #if leads:
        membertitle = leads[0].text
        #repeat process for <p>
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
        
#list of URLs with similar CMS compiled with this advanced search on Google: site:nhs.uk inurl:about-us/our-governing-body.aspx
ccglist = ['www.hounslowccg.nhs.uk/',  'www.centrallondonccg.nhs.uk/', 'www.hammersmithfulhamccg.nhs.uk/']
#'www.ealingccg.nhs.uk/' has similar page but at different URL: http://www.hammersmithfulhamccg.nhs.uk/about-us/our-governing-body.aspx
for ccg in ccglist:
    fullurl = 'http://'+ccg+'about-us/our-governing-body.aspx'
    print 'scraping ', fullurl
    scrape_ccg(fullurl)



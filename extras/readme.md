# Extras
Here is where we stored all of our submissions for the milestones and final report.

##Data Scraping
We scraped data from IMDb in different ways. First we used a python module called [imdbpy.sourceforge.net](imdbpy) which was slow, but had a lot data.

For posters, and other details that we needed add in addition, we most likely scrapped pages omdbapi.com and parsed them using string finding as well as BeautifulSoup in some cases. This was the first time any of us had scraped data so it's quite sloppy.

Finding ratings was much more difficult. Ombapi also had some rating info but lacked the coveted Rotten Tomatoes rating in a lot of cases. Handling that was difficult as Rotten Tomatoes does not have a publicly available API, but we solved it by searching for it through using Google Searches.

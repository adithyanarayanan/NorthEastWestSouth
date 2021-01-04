# NorthEastWS
A news aggregator web application that lets you peruse news articles for your main course. On the side, it analyzes the sentiment surrounding the news in the twitter-verse. 

Features
--
1. Retrieves the news article's weblink. Sorts articles by topics using Topic Modeling techniques and consolidates the retrieved articles by categories.
2. Displays additional data about the articles by analyzing the replies to the article on twitter- such as

- Generating Relevant Discussions  Does the article generate discussions on the twitterverse How many interactions with the article is relevant to the area of discussion
- Polarity of the generated discussions  How polarized is the discussion that an article generates 

The statistics are calculted by filtering out irrelevant comments and studying the polarity of the rest. 

Further statistics can also be calculated w.r.t news articles with further versions
-- 
1. How toxic are the discussions surrounding the articles
2. How partisan are the headlinesdescriptions of the articles

# NETS213 Final Project
## AAPI Hate Crimes Database

Welcome to our final project repository.  This README contains the required information for "Final Project Part 2 Deliverable 1" and "Final Project Part 2 Deliverable 2."  To search for the materials required for Part 2 Deliverable 2, read *the text in italics.*

### Part 1: Web Scraping
(4) Compile a list of keywords and then use the web scraper provided by Prof. CCB to crawl over news articles on Google that include the below hit words. It works by making search queries under Google News for each date in a specified time range and for each term that we are interested in. The output of the crawler is a list of article URL that we will then convert to a CSV. This CSV will then be used in Mechanical Turk as URLs for our HITs. For our project, we are only concerned with news reports or articles on an incident of violence against Asian American Pacific Islander (AAPI). We will present a list of ethnicities we include as AAPI including individuals from or descended from immigrants from South Asia, Southeast Asia, East Asia, Middle East, Central Asia, and Pacific Islands. We will attempt to crawl for news articles from 2011-2021.

Keywords for the news article scraper: hate crime, Asian violence, racism, xenophobia, assault, anti-Asian, Asian American attacked

We first posted 10% of the 600 articles we plan to post on the MTurk platform on Sandbox. We will designate these labels as expert labels to be compared to the majority vote labels gathered from MTurk. Since there are only 60 labels, we will also easily be able to check for any outliers. This run also helps us clarify any directions or tweak parts of the HIT design. 


### Part 2: MTurk
(2.5) After the crawler finishes, we will select about 1,000 articles and divide them into a training set and test set.  For our training data, we will evenly distribute the number of articles from each year except 2021 (since this year is shorter than all the others).  We will then use newspaper3k to extract texts from the selected articles. Once this is completed, we will regroup the articles by article length. We will do this since we understand that some articles are longer and want to appropriately pay workers for this. Therefore, we will ensure each batch has articles of similar length and pay workers more for longer articles. Additionally, mixing articles of different years together may reduce any bias if the workers already can predict the timeframe of the article, and the possibility the articles overlap and workers are influenced by the information they gain from an earlier article. 

(3) We were thinking of having more than one worker on each article but are worried about the costs of this since we have over a hundred articles and are leaning toward having 3 workers per article. Our original idea was to implement quality control via a set of gold standard data, but we are instead doing a majority vote approach.  This is later described in the Quality Control section of the write-up.

*THe raw data can be found here: data/directory/raw_data.csv*

(1) Since we already created mock HIT designs for this part of the project, we will simply need to create different batches of CSV with our gold standards and then use these CSV files to post our hits. We expect each member who has access to MTurk to post HITs since we only have two weeks to collect this data. 

### Part 3: Data Analysis
(3) We will then check on the worker quality against our gold standard and remove any data from workers who seem unreliable. We will then aggregate the data, labeling articles as positive and negative. We will use this data to train a text classifier with which we will apply to the rest of the articles.  Based on our model predictions, we will create a graph to see reporting levels on Asian hate crimes over time. We will also analyze the accuracy of our text classifier based on how well it classified the test set. 

### Part 4: Machine Learning Model
(3) The articles that were labeled by the MTurk workers will be used as data for training the classifier in order to be able to predict the label of other articles. This will allow us to keep labeling an arbitrary amount of articles without actually having more workers do the labeling. The classifier-labeled articles will become a part of the data that we will end up analyzing at the end. During the training phase, the input data will most likely be the existence of certain keywords in the article text. With these features, the articles that the workers labelled will provide the label to each instance. Validation sets will also be used to help train the classifier. When the classifier is done training, it will be ready to accept data it has not seen yet (e.g. gold standard data)

### Part 5: Presentations 
(2) Our last part of the project is presenting our project by making a video. For this video, we will explain our research question, methodology, and findings. We will also propose how our project has real-world applications and can contribute to combatting Asian hate crimes. 


### Quality Control
We opted to use majority vote as our method for encouraging stronger results we obtain from worker responses. Specfically, we have 3 workers answer a set list of questions for each article. From there, we made a dictionary for each article with respect to the questions in order to find the majority answer. From there, we return a csv with the majority answer labeled for each question, and for each article. 

*The quality control sample input can be found here: data/directory/qc_input.csv*

*The quality control sample output can be found here: data/directory/qc_output.csv*

*The code for the quality control module can be found here: src/directory/majority_qc.py*

### Aggregation

The main aggregation method uses crowdsourcing to label our data from the web scraper. If the article was related to Asian hate crime, we label it as TRUE and FALSE otherwise. Note that the code for this is under the quality control since we use majority vote to identify the true label of an article. Another aggregation method we will use pertains to the other parts of the data we will collect from the workers for interesting analysis. This data involves the time and location in which the incident occurs. We create a map of the United States displaying the frequency of incidents from our data set. The code extracts the location in order to achieve this. There are two aggregation sample input files because the first one is an older data format of ours. In the interest of time, we kept it for submission. We also created a time plot to note trends in the number of attacks over time. Since incidents are labelled with a date, the code just uses this information and plots it. The original code relied on these libraries that we needed to install: chart_studio, plotly

*The aggregation sample input can be found here: data/directory/ag_input1.txt and data/directory/ag_input2.csv*

*The aggregation sample output can be found here: data/directory/stategraph_ex.PNG and data/directory/timegraph_ex.PNG*

*The code for the aggreagation module can be found here: data/directory/ag_graph.py*

### Classifier

Using two different types of models, a Naive-Bayes Multinomial Classifier and a SVM classifier (Linear), we process the text of the articles as vectors, and the labels as 1 if there exists Asian Discrimination in the article and 0 otherwise. We used a training split of 80% for training, 10% for test, and another 10% classified by our model.

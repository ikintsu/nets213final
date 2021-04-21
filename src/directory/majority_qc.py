import pandas as pd


def get_majority(attributes):
  out = {}
  for attr in attributes.keys():
    maxx = 0
    answer_max = None
    for answer in attributes[attr].keys():
      if attributes[attr][answer] > maxx:
        maxx = attributes[attr][answer]
        answer_max = answer
    out[attr] = answer_max
  return out



def majority_vote(mturk_res):
  keep_cols = ["asian_hate_crime", "education_awareness", "has_victim_race", "month", "news_report", "offender_race", "state", "town", "victim_race", "year"]

  mturk_res = mturk_res[ ["url"] + keep_cols ]
  data = {}

  for index, row in mturk_res.iterrows():
    url = row['url']

    if url not in data.keys():
      new_attributes = {}
      for attr in keep_cols:
        new_attributes[attr] = {}
      data[url] = new_attributes


    attributes = data[url]

    for attr in keep_cols:
      answer_for_attr = row[attr]

      if answer_for_attr not in attributes[attr].keys():
        attributes[attr][answer_for_attr] = 1
      else:
        attributes[attr][answer_for_attr] = attributes[attr][answer_for_attr] + 1

  out = []
  for url in data.keys():
    majority_dict = get_majority(data[url])
    out.append((url,
      majority_dict['asian_hate_crime'],
      majority_dict['education_awareness'],
      majority_dict['has_victim_race'],
      majority_dict['month'],
      majority_dict['news_report'],
      majority_dict['offender_race'],
      majority_dict['state'],
      majority_dict['town'],
      majority_dict['victim_race'],
      majority_dict['year']))

  return sorted(out)

def main():
  # Read in CVS result file with pandas

  results = pd.read_csv('/content/qc_input.csv')

  # output1.csv
  pd.DataFrame(majority_vote(results), columns=["url", "asian_hate_crime", "education_awareness", "has_victim_race", "month", "news_report",
                                                  "offender_race", "state", "town", "victim_race", "year"]).to_csv('output.csv', index=False)

if __name__ == '__main__':
  main()

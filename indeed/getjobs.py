import urllib2
import json
import time


def get_publisher_id():
    f = open('publisher_id.txt', 'r')
    publisher_id = f.readline()
    f.close()
    return publisher_id


def get_all_results(query):
    start_value = 0
    chunk_size = 25
    first_query = submit_query(query)
    end_value = first_query['totalResults']
    first_results = first_query['results']
    query_range = range(chunk_size, end_value, chunk_size)
    all_results = []
    for result in first_results:
        all_results.append(result)
    for i in query_range:
        new_query_url = query + "&start={}".format(i)
        new_query = submit_query(new_query_url)
        new_results = new_query['results']
        for result in new_results:
            all_results.append(result)
    results_dict = {'query': first_query['query'], 'location': first_query['location'], 'results': all_results}
    return results_dict


def build_query(publisher_id, location, salary, user_agent="Mozilla", format_type="json", user_ip="1.2.3.4",
                version="2", job_type="fulltime", latlong="1", highlight="0", radius="75"):
    api_base = "http://api.indeed.com/ads/apisearch?"
    query_base = '"data+science"+or+"machine+learning"+or+"data+mining"'
    #Publisher must be first parameter
    publisher = "publisher={}".format(publisher_id)
    query = "&q={}".format(query_base + "+" + salary)
    user_agent = "&useragent={}".format(user_agent)
    format_type = "&format={}".format(format_type)
    location = "&l={}".format(location)
    user_ip = "&userip={}".format(user_ip)
    version = "&v={}".format(version)
    job_type = "&jt={}".format(job_type)
    latlong = "&latlong={}".format(latlong)
    highlight = "&highlight={}".format(highlight)
    radius = "&radius={}".format(radius)
    limit = "&limit={}".format(25)
    built_api = api_base + publisher + query + user_agent + format_type + location + user_ip + version + job_type + \
        latlong + highlight + radius + limit
    return built_api


def submit_query(query):
    query_return = urllib2.urlopen(query).read()
    query_json = json.loads(query_return)
    return query_json


def store_results(results_dict, file_name):
    with open(file_name, 'w') as f:
        json.dump(results_dict, f)


def query_and_store(publisher_id, location, salary, file_name):
    query = build_query(publisher_id=publisher_id, location=location, salary=salary)
    results = get_all_results(query)
    cur_time = time.strftime("%d_%m_%Y_%H_%M_%S")
    store_results(results, file_name + "_" + cur_time + "_indeed_results.json")


def main():
    publisher_id = get_publisher_id()
    query_and_store(publisher_id, location="Salt+Lake+City%2C+UT", file_name="slc_utah",
                    salary="$90,000")
    query_and_store(publisher_id, location="Seattle%2C+WA", file_name="seattle_wa",
                    salary="120,000")
    query_and_store(publisher_id, location="Austin%2C+TX", file_name="austin_tx",
                    salary="$90,000")
    query_and_store(publisher_id, location="Washington%2C+DC", file_name="washington_dc",
                    salary="$135,000")
    query_and_store(publisher_id, location="San+Diego%2C+CA", file_name="sandiego_ca",
                    salary="$130,000")
    query_and_store(publisher_id, location="Raleigh%2C+NC", file_name="raleigh_nc",
                    salary="$90,000")


if __name__ == '__main__':
    main()

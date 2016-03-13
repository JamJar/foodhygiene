import requests,json
from decimal import *
url = 'http://api.ratings.food.gov.uk/'
headers = {'x-api-version':2,'Accept-Language':'en-GB'}

def request_data(apistring, url=url, headers=headers):
    url = url + apistring
    r = requests.get(url, headers=headers)
    return json.loads(r.text)

def get_authorities_by_region(region_name):
    all_authorities = request_data('Authorities')['authorities']
    authorities_in_region = []
    for authority in all_authorities:
        if authority['RegionName'] == region_name:
            authorities_in_region.append(authority)
    return authorities_in_region

def get_n_star_establishments_by_authority_id(authority_id,num_stars):
    return request_data('Establishments?localAuthorityID={0}&ratingKey={1}'.format(
        authority_id,num_stars))

def get_percentage_n_stars_by_authority_id(authority_id,num_stars):
    authority = request_data('Authorities/{0}'.format(authority_id))
    establishments = get_n_star_establishments_by_authority_id(authority_id,num_stars)
    num_establishments = Decimal(authority['EstablishmentCount'])
    num_n_stars = Decimal(len(establishments['establishments']))
    return (num_n_stars / num_establishments) * 100

def authority_breakdown_by_region(region_name,num_stars):
    authorities = get_authorities_by_region(region_name)
    results = {}
    for authority in authorities:
        results[authority['Name']] = get_percentage_n_stars_by_authority_id(
            authority['LocalAuthorityId'],num_stars)
    return results

def sorted_dict(d,reverse=True):
    import operator
    return sorted(d.items(), key=operator.itemgetter(1), reverse=reverse)

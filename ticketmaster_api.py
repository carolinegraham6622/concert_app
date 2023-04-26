import ticketpy
import credentials

tm_client = ticketpy.ApiClient(credentials.consumer_key)

# venues 
# venues = tm_client.venues.find(keyword="Tabernacle").all()
# for v in venues:
#     print("Name: {} / City: {}".format(v.name, v.city))

# events by genre
pages = tm_client.events.find(
    classification_name='Pop',
    state_code='PA',
    start_date_time='2023-05-01T20:00:00Z',
    end_date_time='2023-12-01T20:00:00Z'
)

for page in pages:
    for event in page:
        print(event)

        # get classification (aka genre ? )
# Options : rock, country, pop, etc...
# get state 
# get start date 
# get end date 

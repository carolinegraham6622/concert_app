import ticketpy
import credentials

def get_concerts(genre, state, start, end):

    tm_client = ticketpy.ApiClient(credentials.consumer_key)

    # venues 
    # venues = tm_client.venues.find(keyword="Tabernacle").all()
    # for v in venues:
    #     print("Name: {} / City: {}".format(v.name, v.city))

    # events by genre
    pages = tm_client.events.find(
        classification_name=genre,
        state_code=state,
        start_date_time=start,
        end_date_time=end
    )

    return pages

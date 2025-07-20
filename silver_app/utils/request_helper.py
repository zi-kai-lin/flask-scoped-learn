import uuid
import datetime as dt



def generate_request_id():

    now = dt.datetime.now(dt.timezone.utc)

    timestamp = now.strftime("%Y%m%d_%H%M%S")

    random_part = uuid.uuid4().hex[:6]

    request_id = f"req_{timestamp}_{random_part}"
    
    return request_id



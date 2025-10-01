# Create class for package
from datetime import timedelta

delay_time = timedelta(hours=9, minutes=5)

class Package:
    def __init__(self, ID, address, city, state, zipcode, Deadline_time, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.Deadline_time = Deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zipcode,
                                                       self.Deadline_time, self.weight, self.delivery_time,
                                                       self.status)

    def update_status(self, convert_timedelta):
        delay_time = timedelta(hours=9, minutes=5)
        corrected_address_time = timedelta(hours=10, minutes=20)
        delayed_package_ids = {6, 25, 28, 32}

        # Package 9 address correction
        if self.ID == 9 and convert_timedelta >= corrected_address_time:
            self.address = "410 S State St"
            self.city = "Salt Lake City"
            self.state = "UT"
            self.zipcode = "84111"
        
        if self.ID in delayed_package_ids and convert_timedelta < delay_time:
            self.status = "Delayed"
        elif self.delivery_time and self.delivery_time <= convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time and self.departure_time <= convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"

    
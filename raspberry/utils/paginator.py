class Paginator(object):
    def __init__(self, request_page_number, count_in_one_page, total_count, parameters = None):
        self.count_in_one_page = count_in_one_page
        self.total_page_count = self._cal_total_page_count(count_in_one_page, total_count)
        _request_page_number = self.validate_number(request_page_number)
        self.current_page_number = self._clean_current_page_number(_request_page_number, self.total_page_count)
        self.offset = (self.current_page_number - 1) * self.count_in_one_page
        self.parameter_str = ""
        if parameters:
            for key, value in parameters.items():
                self.parameter_str += "&" + str(key) + "=" + unicode(value)

    def validate_number(self, request_page_number):
        try:
            request_page_number = int(request_page_number)
        except ValueError, e:
            raise
        return request_page_number

    def _cal_total_page_count(self, count_in_one_page, total_count):
        total_page_count = 1
        if total_count > 0:
            total_page_count = (total_count - 1) / count_in_one_page + 1 
        return total_page_count

    def _clean_current_page_number(self, request_page_number, total_page_count):
        if request_page_number < 1:
            current_page_number = 1
        elif request_page_number > total_page_count:
            current_page_number = total_page_count
        else:
            current_page_number = request_page_number
        return current_page_number

    def has_next(self):
        return self.current_page_number < self.total_page_count

    def has_previous(self):
        return self.current_page_number > 1

    def next_page_number(self):
        return self.current_page_number + 1

    def previous_page_number(self):
        return self.current_page_number - 1

    def need_left_abbr(self):
        return self.current_page_number >= 7
   
    def left_pages(self):
        pages = []
        for i in range(1, self.current_page_number):
            pages.append(i)
        return pages 

    def need_right_abbr(self):
        return self.total_page_count - self.current_page_number >= 6

    def right_pages(self):
        pages = []
        for i in range(self.current_page_number + 1, self.total_page_count + 1):
            pages.append(i)
        return pages

    def parameter(self):
        return self.parameter_str


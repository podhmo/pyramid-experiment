from .models import DBSession

class DefaultResources(object):
    def __init__(self, request):
        """
        
        Arguments:
        - `request`:
        """
        self._request = request

    def add(self, obj, flush=False):
        DBSession.add(obj)
        if flush:
            DBSession.flush(True)
        return obj

    def update_data(self, obj, data):
        for k, v in data.iteritems():
            setattr(obj, k, v)
        return obj
    
        
    

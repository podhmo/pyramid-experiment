from .models import Point
from .models import DBSession

class UpdateDataMixin(object):
    def update_data(self, obj, data):
        for k, v in data.iteritems():
            setattr(obj, k, v)
        return obj

class HandleSessionMixin(object):
    def add(self, obj, flush=False):
        DBSession.add(obj)
        if flush:
            DBSession.flush(True)
        return obj

class PointResources(UpdateDataMixin,
                     HandleSessionMixin):
    def __init__(self, request):
        """
        
        Arguments:
        - `request`:
        """
        self._request = request

    def get_point(self, id_=None):
        if id_ is None:
            return Point()
        else:
            return Point.query.filter(Point.id==id_).one()

    def get_point_list(self):
        return Point.query

    
        
    

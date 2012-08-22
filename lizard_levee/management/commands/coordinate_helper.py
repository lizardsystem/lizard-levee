# kleine hulpjes
import logging

from django.core.management.base import BaseCommand
from lizard_map import coordinates

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ""
    help = "It does nothing, except for printing out (hopefully) useful info"

    def handle(self, *args, **options):
        print('coordinate helper')
        y_coords = [7011324, 7011298]
        #x_coords = [800101,800107,800112,800117,800122,800126,800132,800138]
        x_coords = [800145,800151,800156,800161,800166,800170,800176,800183]
        names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


        make_box_coordinates = lambda x1, y1, x2, y2: '%(x1)f,%(y1)f,%(x2)f,%(y1)f,%(x2)f,%(y2)f,%(x1)f,%(y2)f' % {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

        for i in range(len(x_coords)-1):
            x1, y1 = coordinates.google_to_wgs84(x_coords[i], y_coords[0])
            x2, y2 = coordinates.google_to_wgs84(x_coords[i+1], y_coords[1])
            print names[i] + ' ' + make_box_coordinates(x1, y1, x2, y2)

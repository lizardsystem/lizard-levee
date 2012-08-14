import logging
import datetime
import twitter

from django.core.management.base import BaseCommand

from lizard_levee.models import Message, MessageTag


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ""
    help = "Harvest twitter"

    def handle(self, *args, **options):
        logger.info('Harvesting...')
        tag = MessageTag.objects.get(tag='twitter')
        Message.objects.filter(tags__tag='twitter').delete()
        twitter_search = twitter.Twitter(domain="search.twitter.com")
        # On website ijkdijk:
        #ijkdijk OR Livedijk OR Livedijken OR Sensortechnologie OR Dijkbewaking OR Dijkmonitoring
        #tw_result = twitter_search.search(q="#ijkdijk")
        tw_result = twitter_search.search(
            q="ijkdijk OR Livedijk OR Livedijken OR Sensortechnologie OR Dijkbewaking OR Dijkmonitoring")
        for result in tw_result['results']:
            #print result['created_at']
            # [:-6] is for stripping off +0000, %z does not work strangely enough...
            timestamp = datetime.datetime.strptime(
                result['created_at'][:-6], '%a, %d %b %Y %H:%M:%S')
            message_txt = '%s: %s' % (result['from_user_name'], result['text'])
            message = Message(message=message_txt, timestamp=timestamp)
            message.save()
            message.tags.add(tag)
            logger.info(message_txt)
        logger.info('Done')

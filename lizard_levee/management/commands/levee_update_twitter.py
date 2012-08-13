import logging

from django.core.management.base import BaseCommand
import twitter

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
        tw_result = twitter_search.search(q="#ijkdijk")
        for result in tw_result['results']:
            message_txt = '%s: %s' % (result['from_user_name'], result['text'])
            message = Message(message=message_txt)
            message.save()
            message.tags.add(tag)
            logger.info(message_txt)
        logger.info('Done')

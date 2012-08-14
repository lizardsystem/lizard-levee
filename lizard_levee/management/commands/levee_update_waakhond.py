import StringIO
import datetime
import logging
import string

# from email import parser
from django.core.management.base import BaseCommand
import poplib
import rfc822

from lizard_levee.models import Message, MessageTag

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ""
    help = "Harvest waakhond emails"

    def fetch_mails(self):

        pop_conn = poplib.POP3_SSL('pop.gmail.com')
        #pop_conn = poplib.POP3('pop.gmail.com')
        pop_conn.user('')
        pop_conn.pass_('')
        #Get messages from server:
        num_mails = len(pop_conn.list()[1]) + 1
        print 'num mails %d' % num_mails
        #num_mails = min(num_mails, 5)
        # Retrieve last 5 emails
        messages = [pop_conn.retr(i) for i in range(max(num_mails-5, 0), num_mails)]
        # Concat message pieces:
        #messages = ["\n".join(mssg[1]) for mssg in messages]
        #Parse message intom an email object:
        #messages = [parser.Parser().parsestr(mssg) for mssg in messages]
        result = []
        for resp, text, octets in messages:
            text_ = string.join(text, "\n")
            file = StringIO.StringIO(text_)

            message = rfc822.Message(file)
            # print '----------------------------------------'
            # for k, v in message.items():
            #     print '%s = %s' % (k, v)
            # maybe we want to filter mails here...
            # 'from', ...
            result.append(message)

            #print message['subject']
            #print message['body']
        pop_conn.quit()
        return result

    def handle(self, *args, **options):
        logger.info('Harvesting waakhond...')
        tag, _ = MessageTag.objects.get_or_create(
            tag='waakhond', name='waakhond', html_color='#ff4400')

        mails = self.fetch_mails()

        for mail in mails:
            # Date sooks like: Sun, 26 Feb 2006 19:55:12 +0100
            mail_timestamp = datetime.datetime.strptime(
                mail['date'], '%a, %d %b %Y %H:%M:%S +0100')
            print mail_timestamp
            message, created = Message.objects.get_or_create(
                message=mail['subject'],
                timestamp=mail_timestamp)
            message.save()
            message.tags.add(tag)
            logger.info('Message: %s, %r' % (message, created))

        # for result in tw_result['results']:
        #     message_txt = '%s: %s' % (result['from_user_name'], result['text'])
        #     message = Message(message=message_txt)
        #     message.save()
        #     message.tags.add(tag)
        #     logger.info(message_txt)
        logger.info('Done')

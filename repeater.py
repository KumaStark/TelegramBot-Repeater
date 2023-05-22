#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from telegram import Bot, Message, Update
from telegram.ext import (CommandHandler, Filters, MessageHandler,
                          PicklePersistence, Updater)
from telegram.ext.callbackcontext import CallbackContext

from lib import read_yaml_config
from repeat import clean_repeat, repeat

# token = os.getenv('TELEGRAM_APITOKEN')
config_file = 'config.yaml' # 配置文件路径
config = read_yaml_config(config_file)
token = config["token"]
bot = Bot(token=token)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    print(context.error)


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # log all errors
    dp.add_error_handler(error)

    repeat_filters = Filters.text & ~Filters.command
    # add repeat handler
    dp.add_handler(MessageHandler(repeat_filters, repeat))
    # add repeat clear handler
    dp.add_handler(MessageHandler(Filters.all & ~repeat_filters, repeat))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

import sys
import argparse

from kits.parse_articles import parse_articles

from config.conf import conf
from config.conf import enviroment
from kits.log import get_logger

def initialize():

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", action="store", dest="env",
                        help="enviroment of server. prod|test|dev")
    # parser.add_argument("-p", "--port", action="store", dest="port", default=6003,
    #                     help="port of running iplive node")
    args = parser.parse_args()
    if args.env not in ["dev", "prod"]:
        print("enviroment not support")
        sys.exit()

    env = enviroment[args.env]
    conf['env'] = env
    if 'logger' not in conf:
        conf['logger'] = get_logger("blog", on_screen=True, level=env['level'])

    parse_articles()

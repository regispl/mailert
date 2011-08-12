#! /usr/bin/python2.7
# -*- coding: utf8 -*-

from mailert.mailert import Mailert

m = Mailert(host='mail.triforce.pl', port=587, user='outgoing@triforce.pl', password='out321', service='Test Service', receivers=['m.michalski@money.pl'])

m.info('Yebuo siem!', 'Detale wiadomości')

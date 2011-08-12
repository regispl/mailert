#! /usr/bin/python2.7
# -*- coding: utf8 -*-

from mailert.mailert import Mailert

m = Mailert(host='mail.triforce.pl', port=587, user='outgoing@triforce.pl', password='out321', service='Test Service', receivers=['m.michalski@money.pl'])

m.info('Yebuo siem!', 'Detale wiadomości')

#m = Mailert(connstr='user:out321@mail.triforce.pl:587', service='Important Service', receivers=['m.michalski@money.pl', 'michal@michalski.im'])

#m.critical('Fakap, men!', 'Szczegóły wiadomości')

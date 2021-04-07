#-*- coding:utf-8 -*-

from odoo import api, fields, models, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class hrEmployee(models.Model):
    _inherit =  'hr.employee'

    birthday = fields.Date('Date of Birth', groups="hr.group_hr_user", required=True)


    def send_notification_birthday(self):
        for employee in self :
            number_days = self.env.user.company_id.days_before_birthday
            print(number_days)
            date_notification = employee.birthday + relativedelta(days=-number_days)
            print(date_notification)
            if str(date_notification) == str(fields.Datetime.now())[:10] :
                #TODO : send a nofitication to all users in manager hr group
                print ("Ok cool")
            else :
                continue


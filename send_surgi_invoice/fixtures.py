# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Custom fields to be added to Sales Invoice doctype
custom_fields = {
    'Sales Invoice': [
        {
            'fieldname': 'auto_send_scheduled',
            'label': 'Auto Send Scheduled',
            'fieldtype': 'Check',
            'insert_after': 'is_return',
            'read_only': 1,
            'no_copy': 1,
            'print_hide': 1
        },
        {
            'fieldname': 'scheduled_send_time',
            'label': 'Scheduled Send Time',
            'fieldtype': 'Datetime',
            'insert_after': 'auto_send_scheduled',
            'read_only': 1,
            'no_copy': 1,
            'print_hide': 1
        },
        {
            'fieldname': 'auto_send_status',
            'label': 'Auto Send Status',
            'fieldtype': 'Select',
            'options': '\nScheduled\nSent\nFailed',
            'insert_after': 'scheduled_send_time',
            'read_only': 1,
            'no_copy': 1,
            'print_hide': 1
        },
        {
            'fieldname': 'actual_send_time',
            'label': 'Actual Send Time',
            'fieldtype': 'Datetime',
            'insert_after': 'auto_send_status',
            'read_only': 1,
            'no_copy': 1,
            'print_hide': 1
        }
    ]
}

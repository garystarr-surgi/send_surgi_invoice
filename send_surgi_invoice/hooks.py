# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "send_surgi_invoice"
app_title = "Send Surgi Invoice"
app_publisher = "SurgiShop"
app_description = "Automatically sends sales invoices to customers 24 hours after submission"
app_email = "accounting@surgishop.com"
app_license = "MIT"

# Scheduled tasks - runs every hour to check for invoices ready to send
scheduler_events = {
    "cron": {
        "0 */1 * * *": [  # Run every hour
            "send_surgi_invoice.tasks.send_pending_invoices"
        ]
    }
}

# Document Events - mark invoice for auto-send when submitted
doc_events = {
    "Sales Invoice": {
        "on_submit": "send_surgi_invoice.events.sales_invoice.mark_for_auto_send"
    }
}


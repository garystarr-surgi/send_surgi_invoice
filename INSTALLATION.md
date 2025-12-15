# Installation & Configuration Guide

## Prerequisites

Before installing this app, ensure you have:

1. A working Frappe/ERPNext installation
2. The custom print format "Surgi Sales Invoice" already created in your system
3. Email account properly configured in ERPNext
4. Access to bench commands

## Installation Steps

### Step 1: Get the App

Copy the `send_surgi_invoice` folder to your Frappe bench's `apps` directory:

```bash
# If the app is in /home/user/send_surgi_invoice
cd /path/to/frappe-bench
cp -r /home/user/send_surgi_invoice ./apps/
```

### Step 2: Install on Your Site

```bash
bench --site your-site-name install-app send_surgi_invoice
```

### Step 3: Run Migration

```bash
bench --site your-site-name migrate
```

This will create the following custom fields in Sales Invoice:
- Auto Send Scheduled
- Scheduled Send Time
- Auto Send Status
- Actual Send Time

### Step 4: Restart Bench

```bash
bench restart
```

## Updating the Email Body

Currently, the email body contains placeholder text. To add your custom email body:

1. Open the file: `send_surgi_invoice/send_surgi_invoice/tasks.py`

2. Find the `send_invoice_email` function

3. Replace the `message` variable content (around line 73) with your desired email body

4. After editing, restart the bench:
```bash
bench restart
```

## How to Test

1. Create a new Sales Invoice
2. Submit it
3. Check the custom fields - you should see:
   - Auto Send Scheduled: Checked
   - Scheduled Send Time: 24 hours from now
   - Auto Send Status: Scheduled

4. To test immediately without waiting 24 hours:
   - Manually update the `scheduled_send_time` field to current time
   - Wait for the next hourly run, or manually trigger:
   ```bash
   bench --site your-site-name execute send_surgi_invoice.tasks.send_pending_invoices
   ```

## Scheduled Task

The app runs automatically every hour to check for pending invoices. The schedule is defined in `hooks.py`:

```python
scheduler_events = {
    "cron": {
        "0 */1 * * *": [  # Run every hour
            "send_surgi_invoice.tasks.send_pending_invoices"
        ]
    }
}
```

## Troubleshooting

### Invoice not sending?

1. Check Error Log in ERPNext (search for "Failed to send invoice email")
2. Verify customer has an email address
3. Verify email settings are configured correctly
4. Check that "Surgi Sales Invoice" print format exists

### Email not arriving?

1. Check Email Queue in ERPNext
2. Verify accounting@surgishop.com is configured as a valid email account
3. Check spam/junk folders

### Custom fields not appearing?

Run migration again:
```bash
bench --site your-site-name migrate
```

## Customization Options

### Change Send Delay

Edit `send_surgi_invoice/events/sales_invoice.py`, line 11:

```python
# Change timedelta(hours=24) to desired delay
send_time = datetime.now() + timedelta(hours=24)
```

### Change Scheduled Task Frequency

Edit `send_surgi_invoice/hooks.py`:

```python
# Current: every hour (0 */1 * * *)
# Every 30 minutes: */30 * * * *
# Every 4 hours: 0 */4 * * *
```

### Change Sender Email

Edit `send_surgi_invoice/hooks.py`:

```python
app_email = "newemail@surgishop.com"
```

Also update in `send_surgi_invoice/tasks.py`, line 110:

```python
sender="newemail@surgishop.com"
```

## Uninstalling

```bash
bench --site your-site-name uninstall-app send_surgi_invoice
```

Note: Custom fields will remain in the database after uninstallation.

## Support

For technical issues:
1. Check ERPNext Error Log
2. Review bench logs: `bench --site your-site-name console`
3. Contact your system administrator

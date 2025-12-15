# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime
from frappe.utils.pdf import get_pdf
from frappe.utils import get_url

def send_pending_invoices():
    """
    Scheduled task that runs every hour to check for invoices 
    that are ready to be sent (24 hours have passed since submission).
    """
    try:
        # Get all invoices scheduled for auto-send where send time has passed
        invoices = frappe.db.sql("""
            SELECT name, customer, customer_name, contact_email
            FROM `tabSales Invoice`
            WHERE docstatus = 1
            AND auto_send_scheduled = 1
            AND auto_send_status = 'Scheduled'
            AND scheduled_send_time <= NOW()
        """, as_dict=True)
        
        for invoice in invoices:
            try:
                send_invoice_email(invoice.name)
                
                # Update status
                frappe.db.set_value(
                    'Sales Invoice',
                    invoice.name,
                    {
                        'auto_send_status': 'Sent',
                        'actual_send_time': datetime.now()
                    },
                    update_modified=False
                )
                frappe.db.commit()
                
            except Exception as e:
                # Mark as failed and log error
                frappe.db.set_value(
                    'Sales Invoice',
                    invoice.name,
                    'auto_send_status',
                    'Failed',
                    update_modified=False
                )
                frappe.db.commit()
                
                frappe.log_error(
                    message=f"Invoice: {invoice.name}\nError: {str(e)}",
                    title="Failed to send invoice email"
                )
                
    except Exception as e:
        frappe.log_error(
            message=str(e),
            title="Error in send_pending_invoices task"
        )


def send_invoice_email(invoice_name):
    """
    Send the invoice email with PDF attachment using custom print format.
    """
    # Get the invoice document
    invoice = frappe.get_doc('Sales Invoice', invoice_name)
    
    # Get customer email
    recipient = invoice.contact_email or frappe.db.get_value('Customer', invoice.customer, 'email_id')
    
    if not recipient:
        raise Exception(f"No email found for customer {invoice.customer}")
    
    # Email subject
    subject = f"Invoice {invoice.name} from SurgiShop"
    
    # Email body - Using placeholder text until you provide the actual body
    message = f"""
    Dear {invoice.customer_name or invoice.customer},
    
    Please find attached invoice {invoice.name}.
    
    [Your custom email body will go here]
    
    Best regards,
    SurgiShop Accounting Team
    """
    
    # Generate PDF with custom print format
    print_format = "Surgi Sales Invoice"
    
    try:
        # Get PDF content
        pdf_content = get_pdf(
            'Sales Invoice',
            invoice.name,
            print_format=print_format
        )
        
        # Send email with attachment
        frappe.sendmail(
            recipients=[recipient],
            sender="accounting@surgishop.com",
            subject=subject,
            message=message,
            attachments=[{
                'fname': f'{invoice.name}.pdf',
                'fcontent': pdf_content
            }],
            reference_doctype='Sales Invoice',
            reference_name=invoice.name
        )
        
        # Add comment to invoice
        invoice.add_comment(
            'Comment',
            f'Invoice automatically sent to {recipient} via email'
        )
        
    except Exception as e:
        raise Exception(f"Error generating or sending PDF: {str(e)}")

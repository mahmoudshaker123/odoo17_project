# Sales Approval Workflow Module

## Overview
This Odoo 17 module extends the Sales application with a custom approval workflow for quotations. It implements a 4-level approval system with role-based access control and privacy controls for rejection notes.

## Features

### Approval Workflow
- **4 Roles**: Sales Representative, Sales Manager, Sales Supervisor, Sales Admin
- **Custom States**: draft → to_manager → to_supervisor → approved
- **Rejection Flow**: Any level can reject with detailed notes
- **Resubmission**: Rejected quotations can be edited and resubmitted

### Security & Privacy
- **Role-based Access**: Each role has specific permissions
- **Private Notes**: Rejection notes are only visible to relevant parties
- **Record Rules**: Enforce data visibility based on user groups

### User Interface
- **Custom Buttons**: Context-sensitive buttons for each role
- **Approval History**: Track all rejections and approvals
- **Badge Indicators**: Visual state indicators in list and form views
- **Activity Notifications**: Automatic notifications for pending approvals

## Installation

1. Copy the module to your Odoo addons directory
2. Update the addons list
3. Install the module from the Apps menu

## Usage

### For Sales Representatives
1. Create a new quotation
2. Click "Submit to Manager" when ready
3. If rejected, review the rejection note and resubmit

### For Sales Managers
1. Review quotations in "To Manager" state
2. Click "Approve" to send to supervisor
3. Click "Reject" to return to representative with notes

### For Sales Supervisors
1. Review quotations in "To Supervisor" state
2. Click "Approve" for final approval
3. Click "Reject" to return to manager with notes

### For Sales Admins
1. Can see all quotations and rejection history
2. Full access to all approval states
3. Can manage the entire workflow

## Technical Details

### Models
- **sale.order**: Extended with approval workflow
- **sale.order.rejection**: Stores rejection history with privacy controls

### Security Groups
- `group_sales_representative`: Can create and submit quotations
- `group_sales_manager`: Can approve/reject from representatives
- `group_sales_supervisor`: Can give final approval
- `group_sales_admin`: Full access to everything

### Demo Data
The module includes demo users for testing:
- Sales Representative: rep@example.com
- Sales Manager: manager@example.com
- Sales Supervisor: supervisor@example.com
- Sales Admin: admin@example.com

## Customization

### Adding New States
To add new approval states, modify the `approval_state` field in `sale_order.py` and update the workflow methods.

### Customizing Rejection Reasons
The rejection wizard can be extended to include predefined reasons or additional fields.

### Integration with Other Modules
The module is designed to work with standard Odoo modules and can be extended for integration with CRM, Project, or other custom modules.

## Support
For issues or customization requests, please contact your system administrator.

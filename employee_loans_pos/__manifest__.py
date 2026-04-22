
{
    "name": "Employee Loans POS",
    "version": "1.1",
    "depends": ["hr", "account"],
    "author": "Custom",
    "category": "Human Resources",
    "data": [
        "security/ir.model.access.csv",
        "reports/employee_loan_report.xml",
        "views/employee_loan_views.xml",
        "views/employee_loan_wizard.xml",
        "views/employee_loan_payment_wizard.xml",
        "views/hr_employee_views.xml",
    ],
    "installable": True
}

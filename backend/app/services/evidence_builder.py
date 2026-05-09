from app.models.seller import Seller
from app.models.report import Report


def build_report_evidence_text(seller: Seller, report: Report) -> str:
    return f"""
Seller Evidence Report

Seller Name: {seller.seller_name}
Business Name: {seller.business_name or "Not provided"}
Phone Number: {seller.phone_number or "Not provided"}
Email: {seller.email or "Not provided"}
Social Handle: {seller.social_handle or "Not provided"}
Bank Account Name: {seller.bank_account_name or "Not provided"}

Report Type: {report.report_type}
Report Status: {report.status}
Amount Lost: {report.amount_lost or "Not provided"}
Evidence URL: {report.evidence_url or "Not provided"}

Complaint Description:
{report.description}

Created At: {report.created_at}
""".strip()
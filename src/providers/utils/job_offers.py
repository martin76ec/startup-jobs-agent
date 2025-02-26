from datetime import datetime


def offer_to_markdown(offer):
    """
    Convert an OfferData object to a Markdown string.
    """
    markdown_template = f"""# Job Offer
**Role:** {offer.role}  
**Remote:** {offer.remote}  
**Company Name:** {offer.company_name}  
**Vertical:** {offer.vertical}  
**Location:** {offer.location}  
**Details:**  
{offer.details}  

**Apply URL:** {'[Apply here](' + offer.apply_url + ')' if offer.apply_url else 'Not provided'}  

**Date Scraped:** {datetime.fromisoformat(offer.date_scraped.rstrip('Z')).strftime('%Y-%m-%d %H:%M:%S')} UTC  
"""
    return markdown_template.strip()

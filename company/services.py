from django.shortcuts import get_object_or_404
from company.models import Company

def get_company(filters: dict):
    """
    Retrieve a company by given filters or raise 404 if not found.
    """
    return get_object_or_404(Company, **filters)

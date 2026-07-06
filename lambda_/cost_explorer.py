import boto3
from datetime import datetime, timedelta
def get_cost_breakdown(days: int = 30) -> dict:
    ce = boto3.client('ce', region_name='us-east-1')
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    
    service_resp = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )
    by_service = []
    total_cost = 0.0
    currency = "USD"
    
    for result in service_resp.get('ResultsByTime', []):
        for group in result['Groups']:
            service_name = group['Keys'][0]
            cost_amount = float(group['Metrics']['UnblendedCost']['Amount'])
            total_cost += cost_amount
            by_service.append({
                'service': service_name,
                'cost': cost_amount
            })
    
    return {
        'total_cost': total_cost,
        'currency': currency,
        'by_service': by_service
    }
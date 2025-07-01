#!/usr/bin/env python3
"""
CLI tool for monitoring token usage in Graphiti
"""

import click
import json
from datetime import datetime, timedelta
from tabulate import tabulate
from graphiti_core.telemetry.token_monitor import get_token_monitor

@click.group()
def cli():
    """Graphiti Token Usage Monitor CLI"""
    pass

@cli.command()
@click.option('--provider', '-p', help='Filter by provider (openai, anthropic, gemini)')
@click.option('--days', '-d', default=30, help='Number of days to show (default: 30)')
def summary(provider, days):
    """Show usage summary for providers."""
    monitor = get_token_monitor()
    
    if provider:
        data = monitor.get_provider_summary(provider, days)
        click.echo(f"\n📊 Usage Summary for {provider.upper()} (last {days} days)")
        click.echo("=" * 60)
        
        # Basic stats
        click.echo(f"Total Requests: {data['total_requests']:,}")
        click.echo(f"Total Tokens: {data['total_tokens']:,}")
        click.echo(f"  - Input: {data['total_input_tokens']:,}")
        click.echo(f"  - Output: {data['total_output_tokens']:,}")
        click.echo(f"Total Cost: ${data['total_cost_usd']:.2f}")
        
        # By service type
        if data['by_service_type']:
            click.echo("\nBy Service Type:")
            for service, stats in data['by_service_type'].items():
                click.echo(f"  {service}: {stats['requests']:,} requests, {stats['tokens']:,} tokens")
        
        # By model
        if data['by_model']:
            click.echo("\nBy Model:")
            model_table = [[m['model'], f"{m['requests']:,}", f"{m['tokens']:,}", f"${m['cost']:.2f}"] 
                          for m in data['by_model']]
            click.echo(tabulate(model_table, headers=['Model', 'Requests', 'Tokens', 'Cost'], tablefmt='simple'))
    else:
        # Show all providers
        report = monitor.get_comprehensive_report()
        click.echo(f"\n📊 Comprehensive Usage Report")
        click.echo("=" * 60)
        
        summary_data = report['summary']
        click.echo(f"Period: {report['report_period']['start'][:10]} to {report['report_period']['end'][:10]}")
        click.echo(f"Total Requests: {summary_data['total_requests']:,}")
        click.echo(f"Total Tokens: {summary_data['total_tokens']:,}")
        click.echo(f"Total Cost: ${summary_data['total_cost_usd']:.2f}")
        click.echo(f"Errors: {summary_data['error_count']}")
        
        # Provider breakdown
        click.echo("\nBy Provider:")
        provider_table = []
        for provider, services in report['by_provider'].items():
            total_tokens = sum(s['tokens'] for s in services.values())
            total_cost = sum(s['cost'] for s in services.values())
            provider_table.append([provider, f"{total_tokens:,}", f"${total_cost:.2f}"])
        
        click.echo(tabulate(provider_table, headers=['Provider', 'Total Tokens', 'Total Cost'], tablefmt='simple'))

@cli.command()
def status():
    """Show subscription status and remaining tokens."""
    monitor = get_token_monitor()
    report = monitor.get_comprehensive_report()
    status = report['subscription_status']
    
    click.echo("\n💳 Subscription Status")
    click.echo("=" * 60)
    
    status_table = []
    for provider, info in status.items():
        status_emoji = "✅" if info['status'] == 'ok' else "⚠️" if info['status'] == 'warning' else "🚨"
        status_table.append([
            provider.upper(),
            f"{info['used']:,}",
            f"{info['limit']:,}",
            f"{info['remaining']:,}",
            f"{info['percentage_used']:.1f}%",
            f"{status_emoji} {info['status']}"
        ])
    
    click.echo(tabulate(status_table, 
                       headers=['Provider', 'Used', 'Limit', 'Remaining', 'Usage %', 'Status'],
                       tablefmt='simple'))

@cli.command()
@click.argument('provider')
@click.argument('limit_type')
@click.argument('value', type=int)
def set_limit(provider, limit_type, value):
    """Set subscription limit for a provider.
    
    Examples:
        graphiti-tokens set-limit anthropic max_plan_tokens 5000000
        graphiti-tokens set-limit openai prepaid_credits 100
    """
    monitor = get_token_monitor()
    result = monitor.set_subscription_limit(provider, limit_type, value)
    click.echo(f"✅ {result}")

@cli.command()
@click.argument('output_file')
@click.option('--days', '-d', default=30, help='Export last N days (default: 30)')
def export(output_file, days):
    """Export usage data to CSV file."""
    monitor = get_token_monitor()
    start_date = (datetime.now() - timedelta(days=days)).isoformat()
    result = monitor.export_to_csv(output_file, start_date=start_date)
    click.echo(f"✅ {result}")

@cli.command()
@click.option('--days', '-d', default=90, help='Keep data for last N days (default: 90)')
def cleanup(days):
    """Clean up old usage data."""
    if click.confirm(f'This will delete all data older than {days} days. Continue?'):
        monitor = get_token_monitor()
        result = monitor.cleanup_old_data(days)
        click.echo(f"✅ {result}")

@cli.command()
@click.option('--format', '-f', type=click.Choice(['json', 'text']), default='text')
def alerts(format):
    """Check for usage alerts."""
    monitor = get_token_monitor()
    report = monitor.get_comprehensive_report()
    
    all_alerts = []
    for provider in ['openai', 'anthropic', 'gemini']:
        summary = monitor.get_provider_summary(provider)
        alerts = monitor._check_alerts(provider, summary)
        all_alerts.extend(alerts)
    
    if format == 'json':
        click.echo(json.dumps({'alerts': all_alerts, 'timestamp': datetime.now().isoformat()}, indent=2))
    else:
        if all_alerts:
            click.echo("\n⚠️  Active Alerts")
            click.echo("=" * 60)
            for alert in all_alerts:
                click.echo(f"• {alert}")
        else:
            click.echo("\n✅ No active alerts")

if __name__ == '__main__':
    cli()
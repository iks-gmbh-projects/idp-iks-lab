#!/usr/bin/env python3
"""
Advisory Catalog Quality and IKS Checks for Backstage

This script evaluates Backstage service catalog entities against defined checks
and generates a Markdown report. Checks are advisory only and do not enforce
compliance in the MVP.

Usage:
    python3 check_catalog_scorecards.py \\
        --catalog-root backstage/catalog/locations.yaml \\
        --checks backstage/scorecards/checks.yaml \\
        --output /tmp/catalog-scorecard-report.md

    python3 check_catalog_scorecards.py --assert-demo-fixtures
"""

import argparse
import os
import sys
from typing import Dict, List, Any, Tuple

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: python3 -m pip install PyYAML", file=sys.stderr)
    sys.exit(1)


def load_yaml_documents(file_path: str) -> List[Dict[str, Any]]:
    """Load all YAML documents from a file (supports multi-document files)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            docs = list(yaml.safe_load_all(f))
            return [doc for doc in docs if doc is not None]
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def load_checks(checks_path: str) -> Dict[str, Any]:
    """Load check definitions from checks.yaml."""
    docs = load_yaml_documents(checks_path)
    if not docs or 'groups' not in docs[0]:
        print(f"Error: Invalid checks file format: {checks_path}", file=sys.stderr)
        sys.exit(1)
    return docs[0]


def load_catalog_locations(catalog_root: str) -> List[str]:
    """Load catalog location targets from locations.yaml."""
    docs = load_yaml_documents(catalog_root)
    
    for doc in docs:
        if doc.get('kind') == 'Location' and 'spec' in doc and 'targets' in doc['spec']:
            return doc['spec']['targets']
    
    print(f"Error: No Location with spec.targets found in {catalog_root}", file=sys.stderr)
    sys.exit(1)


def resolve_target_path(catalog_root: str, target: str) -> str:
    """Resolve relative target path based on catalog root directory."""
    catalog_dir = os.path.dirname(os.path.abspath(catalog_root))
    return os.path.normpath(os.path.join(catalog_dir, target))


def load_catalog_entities(catalog_root: str) -> List[Dict[str, Any]]:
    """Load all catalog entities from targets specified in locations.yaml."""
    targets = load_catalog_locations(catalog_root)
    entities = []
    
    for target in targets:
        target_path = resolve_target_path(catalog_root, target)
        
        if not os.path.exists(target_path):
            print(f"Warning: Target file not found (skipping): {target_path}", file=sys.stderr)
            continue
        
        docs = load_yaml_documents(target_path)
        entities.extend(docs)
    
    return entities


def filter_service_components(entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter entities to only Component entities with spec.type: service."""
    services = []
    
    for entity in entities:
        if entity.get('kind') == 'Component':
            spec = entity.get('spec', {})
            if spec.get('type') == 'service':
                services.append(entity)
    
    return services


def get_nested_value(obj: Dict[str, Any], path: str) -> Any:
    """Get nested dictionary value using dot notation (e.g., 'metadata.name')."""
    keys = path.split('.')
    value = obj
    
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return None
    
    return value


def check_field_present(entity: Dict[str, Any], field_path: str) -> bool:
    """Check if a field is present and non-empty."""
    # Special handling for annotations which use keys with dots/slashes
    if field_path.startswith('metadata.annotations.'):
        annotations = get_nested_value(entity, 'metadata.annotations')
        if not annotations:
            return False
        
        # Extract the annotation key (everything after 'metadata.annotations.')
        annotation_key = field_path[len('metadata.annotations.'):]
        value = annotations.get(annotation_key)
        
        if value is None:
            return False
        
        if isinstance(value, str):
            return value.strip() != ''
        
        return True
    
    # Standard nested path handling
    value = get_nested_value(entity, field_path)
    
    if value is None:
        return False
    
    if isinstance(value, str):
        return value.strip() != ''
    
    return True


def check_documentation_present(entity: Dict[str, Any]) -> bool:
    """Check if documentation is present via annotation or links."""
    # Check annotation first
    annotations = get_nested_value(entity, 'metadata.annotations')
    if annotations and annotations.get('backstage.io/techdocs-ref'):
        return True
    
    # Check links for documentation/docs
    links = get_nested_value(entity, 'metadata.links')
    if links and isinstance(links, list):
        for link in links:
            if isinstance(link, dict):
                title = link.get('title', '').lower()
                if 'documentation' in title or 'docs' in title:
                    return True
    
    return False


def check_runbook_present(entity: Dict[str, Any]) -> bool:
    """Check if runbook is present via annotation or links."""
    # Check annotation first
    annotations = get_nested_value(entity, 'metadata.annotations')
    if annotations and annotations.get('iks.dev/runbook-url'):
        return True
    
    # Check links for runbook
    links = get_nested_value(entity, 'metadata.links')
    if links and isinstance(links, list):
        for link in links:
            if isinstance(link, dict):
                title = link.get('title', '').lower()
                if 'runbook' in title:
                    return True
    
    return False


def check_iks_scope_present(entity: Dict[str, Any]) -> bool:
    """Check if compliance scope contains 'iks' token."""
    annotations = get_nested_value(entity, 'metadata.annotations')
    if not annotations:
        return False
    
    compliance_scope = annotations.get('iks.dev/compliance-scope', '')
    if not compliance_scope:
        return False
    
    # Split by comma, trim whitespace, check for 'iks'
    scopes = [scope.strip() for scope in compliance_scope.split(',')]
    return 'iks' in scopes


def evaluate_check(entity: Dict[str, Any], group_id: str, check: Dict[str, Any]) -> Tuple[bool, str, str]:
    """
    Evaluate a single check against an entity.
    
    Returns:
        (passed, field_used, remediation_hint)
    """
    check_id = check['id']
    
    # Special handling for complex checks
    if check_id == 'has-documentation':
        passed = check_documentation_present(entity)
        field_used = 'metadata.annotations.backstage.io/techdocs-ref or metadata.links[]'
        remediation_hint = 'Add backstage.io/techdocs-ref annotation or a documentation link'
    
    elif check_id == 'has-runbook':
        passed = check_runbook_present(entity)
        field_used = 'metadata.annotations.iks.dev/runbook-url or metadata.links[]'
        remediation_hint = 'Add iks.dev/runbook-url annotation or a runbook link'
    
    elif check_id == 'has-iks-scope':
        passed = check_iks_scope_present(entity)
        field_used = 'metadata.annotations.iks.dev/compliance-scope'
        remediation_hint = 'Add or update iks.dev/compliance-scope to include "iks"'
    
    else:
        # Standard field presence check
        field_path = check['field']
        passed = check_field_present(entity, field_path)
        field_used = field_path
        remediation_hint = f'Add {field_path} to the entity'
    
    return passed, field_used, remediation_hint


def generate_report(
    services: List[Dict[str, Any]],
    checks_def: Dict[str, Any],
    catalog_root: str,
    checks_path: str
) -> str:
    """Generate Markdown report of check results."""
    
    results = []
    
    for service in services:
        service_name = get_nested_value(service, 'metadata.name') or 'unknown'
        
        for group in checks_def['groups']:
            group_id = group['id']
            
            for check in group['checks']:
                check_id = check['id']
                check_title = check['title']
                
                passed, field_used, remediation_hint = evaluate_check(service, group_id, check)
                
                results.append({
                    'service': service_name,
                    'group_id': group_id,
                    'group_title': group['title'],
                    'check_id': check_id,
                    'check_title': check_title,
                    'status': 'PASS' if passed else 'FAIL',
                    'field_used': field_used,
                    'remediation': remediation_hint if not passed else ''
                })
    
    # Build Markdown report
    lines = [
        "# Catalog Quality and IKS Checks Report",
        "",
        "This report evaluates Backstage service catalog entities against advisory quality and IKS checks.",
        "",
        f"**Catalog source:** `{catalog_root}`  ",
        f"**Checks definition:** `{checks_path}`  ",
        "",
        "⚠️ **Note:** This report is advisory only and does not enforce compliance. Use results as signals for follow-up metadata work.",
        "",
        "## Summary by Service",
        ""
    ]
    
    # Summary table
    service_names = sorted(set(r['service'] for r in results))
    lines.append("| Service | Passed | Failed | Total |")
    lines.append("|---------|--------|--------|-------|")
    
    for service_name in service_names:
        service_results = [r for r in results if r['service'] == service_name]
        passed_count = sum(1 for r in service_results if r['status'] == 'PASS')
        failed_count = sum(1 for r in service_results if r['status'] == 'FAIL')
        total_count = len(service_results)
        
        status_emoji = '✅' if failed_count == 0 else '⚠️'
        lines.append(f"| {status_emoji} {service_name} | {passed_count} | {failed_count} | {total_count} |")
    
    lines.append("")
    lines.append("## Detailed Results")
    lines.append("")
    
    # Detailed results by service
    for service_name in service_names:
        service_results = [r for r in results if r['service'] == service_name]
        
        lines.append(f"### {service_name}")
        lines.append("")
        lines.append("| Group | Check | Status | Field | Remediation |")
        lines.append("|-------|-------|--------|-------|-------------|")
        
        for result in service_results:
            group_title = result['group_title']
            check_title = result['check_title']
            status = result['status']
            field_used = result['field_used']
            remediation = result['remediation'] or '-'
            
            status_badge = '✅ PASS' if status == 'PASS' else '❌ FAIL'
            
            lines.append(f"| {group_title} | {check_title} | {status_badge} | `{field_used}` | {remediation} |")
        
        lines.append("")
    
    return '\n'.join(lines)


def assert_demo_fixtures(services: List[Dict[str, Any]], checks_def: Dict[str, Any]) -> None:
    """
    Validate expected demo fixture behavior:
    - customer-portal: all checks pass
    - reporting-api: exactly one check fails (catalog-quality/has-runbook)
    """
    errors = []
    
    # Find services
    customer_portal = next((s for s in services if get_nested_value(s, 'metadata.name') == 'customer-portal'), None)
    reporting_api = next((s for s in services if get_nested_value(s, 'metadata.name') == 'reporting-api'), None)
    
    if not customer_portal:
        errors.append("Demo fixture 'customer-portal' not found in catalog")
    
    if not reporting_api:
        errors.append("Demo fixture 'reporting-api' not found in catalog")
    
    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    
    # Check customer-portal
    customer_portal_failures = []
    for group in checks_def['groups']:
        for check in group['checks']:
            passed, _, _ = evaluate_check(customer_portal, group['id'], check)
            if not passed:
                customer_portal_failures.append(f"{group['id']}/{check['id']}")
    
    if customer_portal_failures:
        errors.append(f"customer-portal should pass all checks but failed: {', '.join(customer_portal_failures)}")
    
    # Check reporting-api
    reporting_api_failures = []
    for group in checks_def['groups']:
        for check in group['checks']:
            passed, _, _ = evaluate_check(reporting_api, group['id'], check)
            if not passed:
                reporting_api_failures.append(f"{group['id']}/{check['id']}")
    
    expected_failure = 'catalog-quality/has-runbook'
    if reporting_api_failures != [expected_failure]:
        errors.append(
            f"reporting-api should fail exactly '{expected_failure}' but got: {reporting_api_failures or 'no failures'}"
        )
    
    if errors:
        for error in errors:
            print(f"Assertion failed: {error}", file=sys.stderr)
        sys.exit(1)
    
    print("✅ Demo fixture assertions passed:")
    print("   - customer-portal: all checks pass")
    print("   - reporting-api: fails only catalog-quality/has-runbook")


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate Backstage catalog entities against advisory quality and IKS checks.'
    )
    parser.add_argument(
        '--catalog-root',
        default='backstage/catalog/locations.yaml',
        help='Path to catalog locations.yaml (default: backstage/catalog/locations.yaml)'
    )
    parser.add_argument(
        '--checks',
        default='backstage/scorecards/checks.yaml',
        help='Path to checks definition (default: backstage/scorecards/checks.yaml)'
    )
    parser.add_argument(
        '--output',
        help='Output Markdown report file path (default: print to stdout)'
    )
    parser.add_argument(
        '--assert-demo-fixtures',
        action='store_true',
        help='Validate expected demo fixture behavior and exit'
    )
    
    args = parser.parse_args()
    
    # Load checks
    checks_def = load_checks(args.checks)
    
    # Load catalog entities
    entities = load_catalog_entities(args.catalog_root)
    
    # Filter to service components
    services = filter_service_components(entities)
    
    if not services:
        print("Warning: No service components found in catalog", file=sys.stderr)
    
    # Assert demo fixtures mode
    if args.assert_demo_fixtures:
        assert_demo_fixtures(services, checks_def)
        return
    
    # Generate report
    report = generate_report(services, checks_def, args.catalog_root, args.checks)
    
    # Output report
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report written to: {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()

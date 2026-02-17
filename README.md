# Rochester Property Due Diligence Tool

Real estate investment scout for validating listing data and finding comparable sales for the South Clinton Village portfolio in Rochester, NY.

## Target Property

- **Name**: South Clinton Village
- **Address**: 898 South Clinton Ave, Rochester, NY 14620
- **Type**: Mixed-Use (11,000 SF Office/Flex + 11 Residential Units)
- **Broker**: Benchmark Realty Advisors (Mark Chiarenza)

## Objective

Validate listing price (conflicting data: $7.19M vs $3.0M) and find 3-5 comparable sales to justify counter-offer.

## Features

1. **Price & Status Verification**: Search multiple listing platforms (LoopNet, Crexi, Benchmark RA, Craigslist, FNET)
2. **Comparable Sales Search**: Find mixed-use/multifamily sales in Rochester 14620 (last 18 months, $1.5M-$5.0M)
3. **Broker Cross-Reference**: Research agent's recent transaction history

## Usage

```bash
python3 rochester_property_scout.py
```

Generates JSON report with:
- Listing verification data
- Comparable sales table
- Broker transaction history
- Recommended next steps

## Current Status

⚠️ **Framework Only** - Requires API integrations:
- LoopNet API (API key needed)
- CoStar subscription
- Monroe County property records access
- Web scraping modules for brokers/Craigslist

## Output Format

```json
{
  "report_metadata": {...},
  "findings": {
    "task_1_listing_verification": {...},
    "task_2_comparable_sales": {...},
    "task_3_broker_research": {...}
  },
  "recommendations": {...}
}
```

## Next Steps

1. Contact Mark Chiarenza directly
2. Pull Monroe County property records
3. Request rent roll & operating statements
4. Verify Pro Forma vs As-Is pricing
5. Obtain CoStar/LoopNet subscriptions
6. Schedule site visit

## Legal Notice

This tool is for due diligence purposes only. Respect website Terms of Service and rate limits. Do not use for unauthorized data scraping.

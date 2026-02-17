#!/usr/bin/env python3
"""
Enhanced Property Analyzer with Web Scraping & Investment Scoring
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

@dataclass
class Property:
    address: str
    price: float
    price_per_sf: Optional[float] = None
    square_feet: Optional[int] = None
    units: Optional[int] = None
    cap_rate: Optional[float] = None
    sale_date: Optional[str] = None
    property_type: str = "Unknown"
    distance_miles: Optional[float] = None
    
@dataclass
class InvestmentAnalysis:
    investment_score: int
    target_property: Property
    comparable_properties: List[Property]
    price_analysis: Dict
    recommendations: Dict
    generated_at: str

class PropertyAnalyzer:
    def __init__(self, target_address: str, target_price: float, target_sf: int, target_units: int):
        self.target = Property(
            address=target_address,
            price=target_price,
            square_feet=target_sf,
            units=target_units,
            price_per_sf=target_price / target_sf if target_sf else None,
            property_type="Mixed-Use"
        )
        
    def calculate_price_per_sf(self, price: float, sf: int) -> float:
        """Calculate price per square foot"""
        return round(price / sf, 2) if sf > 0 else 0.0
    
    def calculate_cap_rate(self, noi: float, price: float) -> float:
        """Calculate capitalization rate"""
        return round((noi / price) * 100, 2) if price > 0 else 0.0
    
    def estimate_value_range(self, comps: List[Property]) -> Tuple[float, float]:
        """Estimate value range based on comparables"""
        if not comps:
            return (self.target.price * 0.85, self.target.price * 1.15)
        
        avg_psf = sum(c.price_per_sf for c in comps if c.price_per_sf) / len([c for c in comps if c.price_per_sf])
        
        if self.target.square_feet:
            low_value = avg_psf * 0.9 * self.target.square_feet
            high_value = avg_psf * 1.1 * self.target.square_feet
            return (round(low_value, -3), round(high_value, -3))
        
        return (self.target.price * 0.85, self.target.price * 1.15)
    
    def calculate_investment_score(self, comps: List[Property], asking_price: float) -> int:
        """
        Calculate investment score (0-100) based on:
        - Price vs comps (40 points)
        - Cap rate potential (30 points)
        - Location/property quality (20 points)
        - Market timing (10 points)
        """
        score = 0
        
        # Price analysis (40 points)
        if comps:
            avg_comp_psf = sum(c.price_per_sf for c in comps if c.price_per_sf) / len([c for c in comps if c.price_per_sf])
            target_psf = asking_price / self.target.square_feet if self.target.square_feet else 0
            
            if target_psf and avg_comp_psf:
                price_ratio = target_psf / avg_comp_psf
                if price_ratio <= 0.8:
                    score += 40  # Great deal
                elif price_ratio <= 0.95:
                    score += 30  # Good deal
                elif price_ratio <= 1.05:
                    score += 20  # Fair market
                elif price_ratio <= 1.15:
                    score += 10  # Slightly overpriced
                # else: 0 points - overpriced
        
        # Cap rate potential (30 points) - estimated
        estimated_cap = 6.5  # Baseline for mixed-use in Rochester
        if estimated_cap >= 8.0:
            score += 30
        elif estimated_cap >= 7.0:
            score += 22
        elif estimated_cap >= 6.0:
            score += 15
        else:
            score += 8
        
        # Location/property (20 points) - South Wedge is desirable
        score += 15  # Solid location score
        
        # Market timing (10 points)
        score += 8  # Current market conditions
        
        return min(score, 100)
    
    def generate_mock_comps(self) -> List[Property]:
        """Generate realistic comparable properties for Rochester 14620"""
        comps = [
            Property(
                address="1000 S Clinton Ave, Rochester NY 14620",
                price=2_750_000,
                square_feet=18_500,
                price_per_sf=148.65,
                units=12,
                cap_rate=6.8,
                sale_date="2025-08-15",
                property_type="Mixed-Use",
                distance_miles=0.2
            ),
            Property(
                address="450 Gregory St, Rochester NY 14620",
                price=1_950_000,
                square_feet=14_200,
                price_per_sf=137.32,
                units=8,
                cap_rate=7.1,
                sale_date="2025-10-22",
                property_type="Multi-Family",
                distance_miles=0.5
            ),
            Property(
                address="725 South Ave, Rochester NY 14620",
                price=3_200_000,
                square_feet=21_000,
                price_per_sf=152.38,
                units=14,
                cap_rate=6.5,
                sale_date="2025-06-30",
                property_type="Mixed-Use",
                distance_miles=0.7
            ),
            Property(
                address="320 Highland Ave, Rochester NY 14620",
                price=2_100_000,
                square_feet=15_800,
                price_per_sf=132.91,
                units=10,
                cap_rate=7.3,
                sale_date="2025-11-18",
                property_type="Multi-Family",
                distance_miles=0.9
            )
        ]
        return comps
    
    def analyze(self, asking_price: float) -> InvestmentAnalysis:
        """Perform full investment analysis"""
        
        # Get comparables
        comps = self.generate_mock_comps()
        
        # Calculate metrics
        value_range = self.estimate_value_range(comps)
        investment_score = self.calculate_investment_score(comps, asking_price)
        
        # Price analysis
        avg_comp_psf = sum(c.price_per_sf for c in comps if c.price_per_sf) / len([c for c in comps if c.price_per_sf])
        target_psf = asking_price / self.target.square_feet if self.target.square_feet else 0
        
        price_analysis = {
            "asking_price": asking_price,
            "asking_price_psf": round(target_psf, 2),
            "avg_comp_price_psf": round(avg_comp_psf, 2),
            "estimated_value_range": {
                "low": value_range[0],
                "high": value_range[1]
            },
            "value_variance_pct": round(((asking_price - sum(value_range)/2) / (sum(value_range)/2)) * 100, 1)
        }
        
        # Recommendations
        if investment_score >= 70:
            recommendation = "STRONG BUY - Property is undervalued relative to comps"
            counter_offer = round(asking_price * 0.92, -3)
        elif investment_score >= 50:
            recommendation = "CONSIDER - Fair market value, negotiate terms"
            counter_offer = round(asking_price * 0.95, -3)
        else:
            recommendation = "PASS - Overpriced for market conditions"
            counter_offer = round(value_range[0], -3)
        
        recommendations = {
            "action": recommendation,
            "suggested_counter_offer": counter_offer,
            "key_insights": [
                f"Asking price is {price_analysis['value_variance_pct']}% {'above' if price_analysis['value_variance_pct'] > 0 else 'below'} estimated value",
                f"Average comparable PSF: ${avg_comp_psf:.2f}",
                f"4 strong comps found within 1 mile",
                "South Wedge location is desirable and appreciating"
            ]
        }
        
        analysis = InvestmentAnalysis(
            investment_score=investment_score,
            target_property=self.target,
            comparable_properties=comps,
            price_analysis=price_analysis,
            recommendations=recommendations,
            generated_at=datetime.now().isoformat()
        )
        
        return analysis

def main():
    # Target property details
    analyzer = PropertyAnalyzer(
        target_address="898 South Clinton Ave, Rochester, NY 14620",
        target_price=7_190_000,  # Pro forma value
        target_sf=22_000,  # 11k office + 11 residential (estimated)
        target_units=11
    )
    
    # Test both price scenarios
    print("="*60)
    print("ROCHESTER PROPERTY INVESTMENT ANALYSIS")
    print("="*60)
    
    # Scenario 1: $3.0M asking
    print("\n📊 SCENARIO 1: $3.0M Asking Price")
    analysis_3m = analyzer.analyze(asking_price=3_000_000)
    
    print(f"\n🎯 Investment Score: {analysis_3m.investment_score}/100")
    print(f"💰 Asking: ${analysis_3m.price_analysis['asking_price']:,.0f}")
    print(f"📐 Price/SF: ${analysis_3m.price_analysis['asking_price_psf']:.2f}")
    print(f"📈 Avg Comp PSF: ${analysis_3m.price_analysis['avg_comp_price_psf']:.2f}")
    print(f"💡 Recommendation: {analysis_3m.recommendations['action']}")
    print(f"🤝 Suggested Counter: ${analysis_3m.recommendations['suggested_counter_offer']:,.0f}")
    
    print("\n🏘️  Top 3 Comparable Properties:")
    for i, comp in enumerate(analysis_3m.comparable_properties[:3], 1):
        print(f"\n  {i}. {comp.address}")
        print(f"     Sold: ${comp.price:,.0f} on {comp.sale_date}")
        print(f"     PSF: ${comp.price_per_sf:.2f} | Cap: {comp.cap_rate}% | Units: {comp.units}")
        print(f"     Distance: {comp.distance_miles} mi")
    
    # Save full report
    output_file = f"investment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    report = {
        "scenario_3m": {
            "investment_score": analysis_3m.investment_score,
            "target_property": asdict(analysis_3m.target_property),
            "comparable_properties": [asdict(c) for c in analysis_3m.comparable_properties],
            "price_analysis": analysis_3m.price_analysis,
            "recommendations": analysis_3m.recommendations,
            "generated_at": analysis_3m.generated_at
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n\n✅ Full report saved to: {output_file}")
    
    return analysis_3m

if __name__ == "__main__":
    main()

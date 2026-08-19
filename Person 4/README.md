# Person 4 - Recommendation Engine

This module improves `/recommend` with proper solar sizing inputs and formulas.

## Inputs

- monthly_units
- city
- roof_area_sqft
- backup_hours
- battery_required
- major_loads
- system_preference
- grid_available
- panel_watt

## Formula

- system_kw = monthly_units / 130
- panels = system_kw * 1000 / panel_watt
- inverter_kw = system_kw * 1.2
- battery_kwh = backup_load_kw * backup_hours * 1.3
- no grid = Off-grid
- backup required = Hybrid
- no backup = On-grid

## Test

```powershell
cd backend
python -c "from app.recommend import make_recommendation; from app.schemas import RecommendationRequest, LoadItem; print(make_recommendation(RecommendationRequest(monthly_units=600, city='Lahore', roof_area_sqft=500, backup_hours=4, battery_required=True, major_loads=[LoadItem(name='Fan', watts=80, quantity=3)], system_preference='auto')))"
```

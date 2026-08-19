from math import ceil
from .schemas import RecommendationRequest

# --- Tunable constants (keep these in one place so they're easy to justify/adjust) ---
UNITS_PER_KW = 130          # avg monthly kWh produced per 1kW of installed solar in Pakistan
INVERTER_OVERSIZE = 1.2     # inverter sized 20% above system size to handle surge/startup loads
BATTERY_SAFETY_FACTOR = 1.3 # covers battery inefficiency + depth-of-discharge headroom
SQFT_PER_PANEL = 18.5       # approx roof space needed per panel (mounting + spacing)


def _backup_load_kw(data: RecommendationRequest) -> float:
    """
    Determine the load (kW) that needs to run during backup/outage.
    Prefer the explicit appliance list (major_loads) if given, since it's
    what the user actually wants to keep running. Fall back to an estimate
    from average hourly consumption if no appliance list was provided.
    """
    if data.major_loads:
        total_watts = sum(item.watts * item.quantity for item in data.major_loads)
        return total_watts / 1000
    # fallback: rough average hourly household draw
    return round(data.monthly_units / 30 / 24, 2)


def _decide_system_type(data: RecommendationRequest, needs_backup: bool) -> tuple[str, str]:
    """
    Decide on-grid / hybrid / off-grid and explain why in plain language.
    Rule order matters:
      1. No grid at the site -> must be off-grid, regardless of preference.
      2. Backup/load-shedding coverage needed -> hybrid (grid + battery).
      3. Otherwise -> plain on-grid (cheapest, no battery).
    A user preference is honored only when it's physically sensible;
    otherwise we explain why we overrode it.
    """
    if not data.grid_available:
        reason = "No grid connection at this site, so an off-grid system is required."
        return "Off-grid", reason

    if needs_backup:
        reason = (
            "Backup power was requested (battery_required and/or backup_hours > 0), "
            "so a hybrid system (grid-tied with battery) is recommended to ride out "
            "outages/load-shedding."
        )
        if data.system_preference == "on-grid":
            reason += " Note: you selected on-grid, but that won't provide backup power."
        return "Hybrid", reason

    if data.system_preference == "hybrid":
        reason = (
            "No backup was strictly required, but hybrid was kept per your preference "
            "for future-proofing against load-shedding."
        )
        return "Hybrid", reason

    if data.system_preference == "off-grid":
        reason = (
            "Off-grid was selected, but grid power is available at this site. "
            "On-grid or hybrid is usually far more cost-effective when grid access exists; "
            "proceed with off-grid only if that's a deliberate choice (e.g. remote/unreliable grid)."
        )
        return "Off-grid", reason

    reason = "Grid is available and no backup was requested, so a simple on-grid system is most cost-effective."
    return "On-grid", reason


def make_recommendation(data: RecommendationRequest) -> dict:
    notes = ["Initial estimate only. Confirm final design with a professional site survey."]

    # 1. System size from historical consumption
    system_kw = round(data.monthly_units / UNITS_PER_KW, 2)

    # 2. Panel count from system size and panel wattage
    panels = ceil(system_kw * 1000 / data.panel_watt)

    # 2b. Cap panels to available roof area, if roof area was provided
    if data.roof_area_sqft > 0:
        max_panels_by_roof = int(data.roof_area_sqft // SQFT_PER_PANEL)
        if max_panels_by_roof < panels:
            notes.append(
                f"Roof area ({data.roof_area_sqft:.0f} sqft) only fits ~{max_panels_by_roof} panels "
                f"at ~{SQFT_PER_PANEL} sqft/panel; ideal design needed {panels}. "
                "System size below has been scaled down to fit the roof."
            )
            panels = max(max_panels_by_roof, 0)
            system_kw = round(panels * data.panel_watt / 1000, 2)

    # 3. Inverter sized with headroom above system size
    inverter_kw = round(system_kw * INVERTER_OVERSIZE, 2)

    # 4. Battery sizing based on actual backup load, not just total system size
    needs_backup = data.battery_required or data.backup_hours > 0
    battery_kwh = 0.0
    if needs_backup:
        backup_kw = _backup_load_kw(data)
        battery_kwh = round(backup_kw * data.backup_hours * BATTERY_SAFETY_FACTOR, 1)

    # 5. Decide on-grid / hybrid / off-grid with a human-readable reason
    system_type, reason = _decide_system_type(data, needs_backup)

    if data.city:
        reason = f"[{data.city}] " + reason

    return {
        "system_kw": system_kw,
        "panels": panels,
        "inverter_kw": inverter_kw,
        "battery_kwh": battery_kwh,
        "system_type": system_type,
        "reason": reason,
        "note": " ".join(notes),
    }
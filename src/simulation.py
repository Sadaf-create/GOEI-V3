import pandas as pd

def simulate(regions: pd.DataFrame, training_coverage: float, sme_support: float, digital_investment: float, protection_expansion: float) -> pd.DataFrame:
    """Transparent illustrative elasticities; not a causal forecast."""
    x = regions.copy()
    x["projected_unemployment_rate"] = (x.unemployment_rate - 0.035*training_coverage - 0.020*sme_support - 0.010*digital_investment).clip(lower=0)
    x["projected_poverty_rate"] = (x.poverty_rate - 0.020*training_coverage - 0.030*sme_support - 0.015*digital_investment - 0.040*protection_expansion).clip(lower=0)
    x["estimated_jobs_supported"] = int(round((training_coverage*.35 + sme_support*.50 + digital_investment*.15) * 1000))
    x["scenario_cost_m"] = round(training_coverage*.8 + sme_support*1.2 + digital_investment*1.5 + protection_expansion*.9, 2)
    return x

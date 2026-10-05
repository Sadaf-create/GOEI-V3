# Data dictionary and provenance

## Demonstration datasets

`regions.csv`: `region`; unemployment and poverty rates as decimals; `median_income` in illustrative local currency/month; 0-100 `skills_score`, `sme_density`, `digital_access`, and `social_protection`.

`people.csv`: pseudonymous `person_id`; demographics; education; income; binary employment/access/protection fields; pipe-separated `skills`; `preferred_sector`. All rows are synthetic.

`jobs.csv`: vacancy ID, title, sector, region, pipe-separated required skills, illustrative monthly salary, and 0-1 demand-growth score. All rows are synthetic.

## Reference indicators (context only)

- ILO, *Employment and Social Trends 2026*: https://www.ilo.org/publications/flagship-reports/employment-and-social-trends-2026
- ILOSTAT report visualisation: https://ilostat.ilo.org/dataviz/weso/
- World Economic Forum, *Future of Jobs Report 2025*: https://www.weforum.org/publications/the-future-of-jobs-report-2025/
- United Nations Statistics Division, *The Sustainable Development Goals Report 2026*: https://unstats.un.org/sdgs/report/2026/
- World Bank DataBank (recommended source for country-level poverty and labour indicators): https://databank.worldbank.org/

The attached white paper also cites a June 2025 World Bank poverty-line update and Saudi GASTAT labour-market statistics. Before publication or operational use, download the desired country/year series directly from the custodial source, preserve its indicator code and revision date, and do not mix global reference values with synthetic records.

## Production data contract

Replace synthetic rows with authorised, pseudonymised, minimally necessary records. Record source, extraction date, geography, population definition, missingness, revision/version and confidence limits. Sensitive attributes may be retained for fairness auditing but must not drive automated adverse decisions.


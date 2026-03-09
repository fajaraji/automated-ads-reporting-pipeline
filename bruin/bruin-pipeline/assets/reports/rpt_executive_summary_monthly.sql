"""@bruin
name: reports.rpt_executive_summary_monthly
type: bq.sql
connection: gcp-marketing
depends:
  - staging.stg_google_ads
  - staging.stg_meta_ads
  - staging.stg_tiktok_ads
  - staging.stg_linkedin_ads
@bruin"""

create or replace view `brunt_raw_ads.rpt_executive_summary_monthly` as
with all_ads as (
  select * from `brunt_raw_ads.stg_google_ads`
  union all
  select * from `brunt_raw_ads.stg_meta_ads`
  union all
  select * from `brunt_raw_ads.stg_tiktok_ads`
  union all
  select * from `brunt_raw_ads.stg_linkedin_ads`
),
monthly as (
  select
    date_trunc(start_date, month) as month,
    platform,
    sum(ad_spend) as total_ad_spend,
    sum(revenue) as total_revenue,
    sum(profit) as total_profit,
    sum(conversions) as total_conversions, 
    sum(clicks) as total_clicks,
    safe_divide(sum(revenue), nullif(sum(ad_spend), 0)) as roas,
    safe_divide(sum(ad_spend), nullif(sum(conversions), 0)) as cpa,
    safe_divide(sum(conversions), nullif(sum(clicks), 0)) as conversion_rate
  from all_ads
  group by
    month,
    platform
)
select
  month,
  platform,
  total_ad_spend,
  total_revenue,
  total_profit,
  total_conversions,
  total_clicks,
  roas,
  cpa,
  conversion_rate,
  safe_divide(total_ad_spend - lag(total_ad_spend) over (partition by platform order by month),
              nullif(lag(total_ad_spend) over (partition by platform order by month), 0)) as ad_spend_growth_pct,
  safe_divide(total_revenue - lag(total_revenue) over (partition by platform order by month),
              nullif(lag(total_revenue) over (partition by platform order by month), 0)) as revenue_growth_pct,
  safe_divide(total_profit - lag(total_profit) over (partition by platform order by month),
              nullif(lag(total_profit) over (partition by platform order by month), 0)) as profit_growth_pct
from monthly;


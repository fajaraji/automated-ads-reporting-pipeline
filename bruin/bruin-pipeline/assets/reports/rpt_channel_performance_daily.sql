"""@bruin
name: reports.rpt_channel_performance_daily
type: bq.sql
connection: gcp-marketing
depends:
  - staging.stg_google_ads
  - staging.stg_meta_ads
  - staging.stg_tiktok_ads
  - staging.stg_linkedin_ads
@bruin"""

create or replace view `brunt_raw_ads.rpt_channel_performance_daily` as
with all_ads as (
  select * from `brunt_raw_ads.stg_google_ads`
  union all
  select * from `brunt_raw_ads.stg_meta_ads`
  union all
  select * from `brunt_raw_ads.stg_tiktok_ads`
  union all
  select * from `brunt_raw_ads.stg_linkedin_ads`
)
select
  start_date as date,
  platform,
  sum(impressions) as impressions,
  sum(clicks) as clicks,
  sum(conversions) as conversions,
  sum(ad_spend) as ad_spend,
  sum(revenue) as revenue,
  sum(profit) as profit,
  safe_divide(sum(clicks), nullif(sum(impressions), 0)) as ctr,
  safe_divide(sum(ad_spend), nullif(sum(clicks), 0)) as cpc,
  safe_divide(sum(conversions), nullif(sum(clicks), 0)) as conversion_rate,
  safe_divide(sum(ad_spend), nullif(sum(conversions), 0)) as cpa,
  safe_divide(sum(revenue), nullif(sum(ad_spend), 0)) as roas
from all_ads
group by
  date,
  platform;


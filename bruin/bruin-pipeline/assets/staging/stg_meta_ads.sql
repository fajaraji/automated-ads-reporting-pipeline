"""@bruin
name: staging.stg_meta_ads
type: bq.sql
connection: gcp-marketing
depends:
  - load_raw_to_bq
@bruin"""

create or replace view `brunt_raw_ads.stg_meta_ads` as
select
  campaign_id,
  campaign_objective,
  platform,
  ad_placement,
  device_type,
  operating_system,
  creative_format,
  creative_size,
  ad_copy_length,
  has_call_to_action,
  creative_emotion,
  creative_age_days,
  target_audience_age,
  target_audience_gender,
  audience_interest_category,
  income_bracket,
  purchase_intent_score,
  retargeting_flag,
  safe_cast(start_date as date) as start_date,
  safe_cast(quarter as int64) as quarter,
  day_of_week,
  safe_cast(hour_of_day as int64) as hour_of_day,
  safe_cast(campaign_day as int64) as campaign_day,
  safe_cast(quality_score as float64) as quality_score,
  safe_cast(actual_cpc as float64) as actual_cpc,
  safe_cast(impressions as int64) as impressions,
  safe_cast(clicks as int64) as clicks,
  safe_cast(conversions as int64) as conversions,
  safe_cast(ad_spend as numeric) as ad_spend,
  safe_cast(revenue as numeric) as revenue,
  safe_cast(bounce_rate as float64) as bounce_rate,
  safe_cast(avg_session_duration_seconds as int64) as avg_session_duration_seconds,
  safe_cast(pages_per_session as float64) as pages_per_session,
  industry_vertical,
  budget_tier,
  safe_cast(CTR as float64) as CTR,
  safe_cast(CPC as float64) as CPC,
  safe_cast(conversion_rate as float64) as conversion_rate,
  safe_cast(CPA as float64) as CPA,
  safe_cast(ROAS as float64) as ROAS,
  safe_cast(profit as numeric) as profit
from `brunt_raw_ads.meta_ads_raw`;


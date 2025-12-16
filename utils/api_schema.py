
# Valid possibilities based on Knowledge Base extraction

API_CONFIG = {
    "levels": [
        "account",
        "campaign",
        "adset",
        "ad"
    ],
    "date_presets": [
        "today",
        "yesterday",
        "this_month",
        "last_month",
        "this_quarter",
        "maximum",
        "data_maximum",
        "last_3d",
        "last_7d",
        "last_14d",
        "last_28d",
        "last_30d",
        "last_90d",
        "last_week_mon_sun",
        "last_week_sun_sat",
        "last_quarter",
        "last_year",
        "this_week_mon_today",
        "this_week_sun_today",
        "this_year"
    ],
    "time_increments": [
        "all_days",
        "1",
        "monthly"
    ],
    "breakdowns": [
        "age",
        "country",
        "gender",
        "frequency_value",
        "hourly_stats_aggregated_by_advertiser_time_zone",
        "hourly_stats_aggregated_by_audience_time_zone",
        "impression_device",
        "place_page_id",
        "publisher_platform",
        "device_platform",
        "platform_position",
        "product_id",
        "region",
        "ad_format_asset",
        "body_asset",
        "call_to_action_asset",
        "description_asset",
        "image_asset",
        "link_url_asset",
        "title_asset",
        "video_asset",
        "dma",
        # Sometimes used as breakdown-like in UI grouping but technically metric? No, these are breakdowns.
        "impressions",
        # "action_device", # Type 2 restricted
        # "action_type",
        # "action_video_variable"
    ],
    "fields": [
        # Standard ID/Name fields
        "account_id",
        "account_name",
        "campaign_id",
        "campaign_name",
        "adset_id",
        "adset_name",
        "ad_id",
        "ad_name",

        # Performance Metrics
        "impressions",
        "spend",
        "reach",
        "frequency",
        "clicks",
        "unique_clicks",
        "ctr",
        "cpc",
        "cpm",
        "cpp",
        "inline_link_clicks",
        "inline_link_click_ctr",

        # Actions / Conversions
        "actions",
        "action_values",
        "cost_per_action_type",
        "cost_per_unique_click",
        "cost_per_inline_link_click",
        "website_ctr",
        "purchase_roas",
        "outbound_clicks",
        "outbound_clicks_ctr",

        # Video
        "video_p25_watched_actions",
        "video_p50_watched_actions",
        "video_p75_watched_actions",
        "video_p100_watched_actions",
        "video_avg_time_watched_actions",
        "video_play_actions",

        # Dates
        "date_start",
        "date_stop",
        "created_time",
        "updated_time"
    ],
    "conversion_goals": {
        "purchase": "Purchase",
        "lead": "Lead",
        "add_to_cart": "Add to Cart",
        "complete_registration": "Complete Registration"
    },
    "breakdown_rules": {
        "comments": "Some breakdowns cannot be combined (Type 1 vs Type 2). Off-site conversions have restrictions.",
        "incompatible_groups": [
            # Group 1 (Time) vs Group 2 (Action) usually restricted?
            # Keeping it simple for now, frontend will just show all options.
        ]
    },
    "field_types": {
        # Integers
        "impressions": "int",
        "reach": "int",
        "clicks": "int",
        "unique_clicks": "int",
        "inline_link_clicks": "int",
        "outbound_clicks": "int",
        "video_p25_watched_actions": "int",
        "video_p50_watched_actions": "int",
        "video_p75_watched_actions": "int",
        "video_p100_watched_actions": "int",
        "video_play_actions": "int",
        
        # Floats
        "spend": "float",
        "frequency": "float",
        "ctr": "float",
        "cpc": "float",
        "cpm": "float",
        "cpp": "float",
        "inline_link_click_ctr": "float",
        "cost_per_unique_click": "float",
        "cost_per_inline_link_click": "float",
        "website_ctr": "float",
        "outbound_clicks_ctr": "float",
        "video_avg_time_watched_actions": "float",
        "purchase_roas": "float",
        "website_purchase_roas": "float",

        # Datetime
        "date_start": "datetime",
        "date_stop": "datetime",
        "created_time": "datetime",
        "updated_time": "datetime",

        # Categories
        "account_id": "category",
        "account_name": "category",
        "campaign_id": "category",
        "campaign_name": "category",
        "adset_id": "category",
        "adset_name": "category",
        "ad_id": "category",
        "ad_name": "category",
        "age": "category",
        "country": "category",
        "gender": "category",
        "publisher_platform": "category",
        "device_platform": "category",
        "platform_position": "category"
    }
}

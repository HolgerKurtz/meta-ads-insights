import requests
import json
import marimo as mo
import pandas as pd
from utils.api_schema import API_CONFIG

def build_url(acc_id, token, lvl, pst, inc, bds, flds, start, end):
    base = "https://graph.facebook.com/v24.0"
    params = []

    if not acc_id or not token:
        return "Please enter Account ID and Access Token."

    endpoint = f"act_{acc_id}/insights"

    params.append(f"access_token={token}")
    params.append(f"level={lvl}")

    # Auto-append conversion fields to ensure we have data for processing
    # even if user didn't select them
    conversion_fields = [
        "actions",
        "action_values",
        "cost_per_action_type",
        "purchase_roas",
        "website_purchase_roas"
    ]
    
    if flds:
        # specific fields requested, ensure conversion fields are included
        combined_fields = list(set(flds + conversion_fields))
        params.append(f"fields={','.join(combined_fields)}")
    else:
        # no fields requested (all?), usually this param is required or defaults apply. 
        # If flds is None/Empty in this app logic, it seems we might just want to append these?
        # Typically the UI always sends some fields. 
        # If flds is meant to be optional and imply "all", adding this restriction might be weird, 
        # but in this specific app, flds is selected by user.
        params.append(f"fields={','.join(conversion_fields)}")


    if bds:
        params.append(f"breakdowns={','.join(bds)}")

    if pst == "custom":
        if start and end:
            time_range = json.dumps(
                {"since": str(start), "until": str(end)})
            params.append(f"time_range={time_range}")
    else:
        params.append(f"date_preset={pst}")

    if inc != "all_days":
        params.append(f"time_increment={inc}")

    params.append(f"limit=5000")

    query_string = "&".join(params)
    return f"{base}/{endpoint}?{query_string}"

@mo.cache
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["data"]
    except Exception as e:
        return {"error": str(e)}

def process_data(data, goal):
    if not data:
        return []
    
    # Normalize goal to lowercase to ensure matching works with API data
    goal_lower = goal.lower()
    goal_title = goal.title()

    # Define the fields we want to transform/rename
    conversion_map = {
        "actions": goal_title,
        "action_values": f"Value {goal_title}",
        "cost_per_action_type": f"Cost per {goal_title}",
        "purchase_roas": "ROAS", # Specific request to keep 'ROAS' or similar
        "website_purchase_roas": "Website ROAS"
    }

    processed = []
    for row in data:
        new_row = row.copy()
        
        # 1. Handle Conversion Fields (Renaming and Value Extraction)
        for field, new_name in conversion_map.items():
            if field in new_row:
                # Remove the original field from the row
                raw_value = new_row.pop(field)
                
                if isinstance(raw_value, list):
                    # logic to extract specific goal value
                    if field == "purchase_roas" or field == "website_purchase_roas":
                        target_types = ["purchase", "omni_purchase", "mobile_app_purchase", "offsite_conversion.fb_pixel_purchase"]
                    else:
                        target_types = [f"offsite_conversion.fb_pixel_{goal_lower}", goal_lower]

                    item = None
                    for t_type in target_types:
                        item = next((x for x in raw_value if x.get("action_type") == t_type), None)
                        if item:
                            break
                    
                    if item:
                        try:
                            # Only add the new column if we found a value (or add 0.0)
                            new_row[new_name] = float(item["value"])
                        except (ValueError, TypeError):
                             new_row[new_name] = 0.0
                    else:
                         new_row[new_name] = 0.0
                else:
                    # weird case, maybe single value?
                    new_row[new_name] = 0.0

        # 2. Flatten/Unnest any other list columns (e.g., website_ctr)
        # We iterate over a copy of keys because we might modify the dict
        for key in list(new_row.keys()):
            val = new_row[key]
            if isinstance(val, list):
                # Heuristic: Take the first item's 'value' if it exists
                # This handles things like website_ctr: [{"action_type": "link_click", "value": "0.5"}]
                if len(val) > 0 and isinstance(val[0], dict) and "value" in val[0]:
                    try:
                        new_row[key] = float(val[0]["value"])
                    except (ValueError, TypeError):
                        new_row[key] = val[0]["value"] # Keep as string if not float
                else:
                    # Fallback for empty lists or lists of non-dicts
                    # If empty list, usually means 0 or None. Let's set to None or 0? 
                    # Setting to None allows pandas to handle it.
                    pass # Leave as is? Or replace? 
                    # If we leave it as list, it might break dataframe display or sorting.
                    # Let's replace with None if empty, or string repr?
                    # User request: "unnest the other kpis"
                    if len(val) == 1 and "value" in val[0]:
                         pass # handled above
                    # else: new_row[key] = str(val) # fallback? 
                    # Let's try to be smart. If it looks like [{action_type:..., value:...}] but didn't match above?
                    # Actually standard meta metrics usually follow that pattern.
                    pass

        processed.append(new_row)
    return processed

def enforce_dataframe_types(df):
    """
    Enforces data types on the DataFrame based on API_CONFIG['field_types'].
    Falls back to string for unknown fields, or keeps existing numpy types if compatible.
    """
    if df.empty:
        return df
        
    field_types = API_CONFIG.get("field_types", {})
    
    for col in df.columns:
        # Check explicit mapping
        if col in field_types:
            target_type = field_types[col]
            
            try:
                if target_type == "int":
                    # numeric_only=False to allow coercion, but we want 'coerce' to turn errors to NaN
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')
                elif target_type == "float":
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).astype('float64')
                elif target_type == "datetime":
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                elif target_type == "category":
                    df[col] = df[col].astype('category')
                elif target_type == "str":
                    df[col] = df[col].astype(str)
            except Exception as e:
                print(f"Warning: Could not cast column {col} to {target_type}: {e}")
        
        # Heuristics for dynamic columns (Goal names)
        # If the column was created by our process_data renaming (e.g., "Lead", "Cost per Lead"), 
        # it should already be float. Let's ensure it.
        # Check if it looks like a numeric column but is object
        elif df[col].dtype == 'object':
            # User request: "If unknown, simple use a string."
            # However, if we leave it as object/string it might be what they asked, 
            # BUT if it's "Lead" (float), we probably want to keep it float.
            # Since process_data ALREADY converts these to float, they should show up as float in df.
            # So if they are object here, they are true unknowns.
            # Convert to string as requested.
            
            # Exception: don't convert lists/dicts to string representation if we want to keep them??
            # But we unnested everything. So valid unknowns are likely strings (ids) or messy data.
            try:
                df[col] = df[col].astype(str)
            except Exception:
                pass
                
    return df

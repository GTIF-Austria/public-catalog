import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

INPUT_FILE = "mobility_asfinag.json"
OUTPUT_FILE = "mobility_asfinag_out.json"

start_date = datetime(2019, 7, 1)
end_date = datetime(2022, 1, 1)

URL_TEMPLATE = (
    "https://eoapi.workspace.gtif-eox.hub-otc.eox.at/vector/"
    "collections/public.asfinag_geometries_for_date/tiles/WebMercatorQuad/{z}/{x}/{y}"
    "?target_date={date}T00:00:00"
)

# ---------------------------------------------------------
# Read JSON
# ---------------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Ensure structure exists
resource = data["Resources"][0]

# ---------------------------------------------------------
# Build new TimeEntries
# ---------------------------------------------------------

time_entries = []
current = end_date  # start from the end

while current >= start_date:
    date_str_compact = current.strftime("%Y%m%d")   # for "Time": "YYYYMMDD"
    date_str_iso = current.strftime("%Y-%m-%d")     # for target_date=YYYY-MM-DD

    time_entries.append({
        "Time": date_str_compact,
        "Url": URL_TEMPLATE.format(
            z="{z}", x="{x}", y="{y}", date=date_str_iso
        )
    })

    # Decrement by one month
    current -= relativedelta(months=1)

resource["TimeEntries"] = time_entries

# ---------------------------------------------------------
# Write updated JSON
# ---------------------------------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Updated JSON written to {OUTPUT_FILE}")
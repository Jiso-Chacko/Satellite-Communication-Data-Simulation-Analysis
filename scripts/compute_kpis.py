import pandas as pd
import numpy as np

from scripts.generate_passes import EARTH_RADIUS_KM


def compute_latency(distance_km):
    c_km_per_ms = 300
    return 2*(distance_km / c_km_per_ms)

df = pd.read_csv('../data/simulated_passes.csv', parse_dates=['timestamp'])

ground_stations = {
    'Gs1': (0, EARTH_RADIUS_KM + 0, 0),
    'Gs2': (EARTH_RADIUS_KM, 0, 0),
    'Gs3': (0, -EARTH_RADIUS_KM, 0)
}

results = []
for index, row in df.iterrows():
    distances = {
        name: np.linalg.norm([row.x_km - gx, row.y_km - gy, row.z_km - gz]) for name, (gx, gy, gz) in ground_stations.items()
    }
    closest = min(distances, key=distances.get)
    latency_ms = compute_latency(distances[closest])
    link_qulaity = 1 / distances[closest]

    results.append({
        'timestamp': row.timestamp,
        'closest_gs': closest,
        'latency_ms': latency_ms,
        'link_qulaity': link_qulaity
    })

kpi_df = pd.DataFrame(results)
kpi_df['handover'] = (kpi_df['closest_gs'] != kpi_df['closest_gs'].shift()).astype(int)

kpi_df.to_csv('../data/kpis.csv', index=False)
print("KPI computed and saved to data/kpis/kpis.csv")
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

ORIBIT_PERIOD = 95*60
SAMPlE_INTERVAL = 30
ALTITUDE_KM = 500
EARTH_RADIUS_KM = 6371

total_samples = int(ORIBIT_PERIOD / SAMPlE_INTERVAL)

start_time = datetime.now()
times = [start_time + timedelta(seconds=i*SAMPlE_INTERVAL) for i in range (total_samples) ]

angles = np.linspace(0, 2*np.pi, total_samples, endpoint=False)
x = (EARTH_RADIUS_KM + ALTITUDE_KM) * np.cos(angles)
y = (EARTH_RADIUS_KM + ALTITUDE_KM) * np.sin(angles)
z = np.zeros_like(x)

df = pd.DataFrame({ 'timestamp': times, 'x_km': x, 'y_km': y, 'z_km': z })

df.to_csv('../data/simulated_passes.csv', index=False)
print(f"Generated {len(df)} orbital samples.")
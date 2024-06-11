import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

# 예제 데이터 생성
dates = pd.date_range(start="2024-01-01", end="2024-01-10", freq="D")

# 날짜를 숫자로 변환 (보간을 위해)
x = np.arange(len(dates))
y = np.array([10, 12, 13, 14, 17, 20, 22, 27, 31, 35])

# 점들을 부드러운 선으로 보간
x_new = np.linspace(x.min(), x.max(), 30)
spl = make_interp_spline(x, y, k=3)  # k=3 은 cubic spline 을 의미
y_smooth = spl(x_new)

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(dates, y, "o", label="Original Data")
plt.plot(dates[0] + pd.to_timedelta(x_new, unit="D"), y_smooth, label="Smoothed Line")

# x축을 날짜 형식으로 포맷팅
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%Y-%m-%d"))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=1))
plt.gcf().autofmt_xdate()

# 그래프 꾸미기
plt.xlabel("Date")
plt.ylabel("Values")
plt.title("Smooth Line Connecting Points")
plt.legend()
plt.grid(True)
plt.show()

# utils/live_plot.py

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Initialize plot (once)
def setup_plot():
    plt.ion()  # Turn on interactive mode
    plt.figure(figsize=(12, 8))  # Default size
    plt.title("PhoenixBot Wallet Growth")
    plt.xlabel("Time (UTC)")
    plt.ylabel("Wallet Value (USD)")
    plt.grid(True)
    plt.tight_layout()

# Update plot (each loop)
def update_plot(timestamps, wallet_histories, current_balance=None, current_rsi=None):
    plt.clf()  # Clear figure before each redraw

    colors = ['limegreen', 'deepskyblue', 'gold', 'orangered', 'magenta', 'purple']
    color_idx = 0
    lines_plotted = False

    for bot_name, history in wallet_histories.items():
        if len(history) > 1:
            try:
                plt.plot(
                    timestamps,
                    history,
                    label=f"{bot_name}",
                    color=colors[color_idx % len(colors)],
                    linewidth=2
                )
                color_idx += 1
                lines_plotted = True
            except Exception as e:
                print(f"Error plotting data for {bot_name}: {e}")

    if lines_plotted:
        plt.legend(loc="upper left")

    if current_balance is not None:
        plt.title(f"PhoenixBot Wallet Growth | Balance: ${current_balance:.2f}")

    if current_rsi is not None:
        plt.figtext(0.15, 0.92, f"Current RSI: {current_rsi:.2f}", fontsize=10, ha='left')

    plt.xlabel("Time (HH:MM)")
    plt.ylabel("Wallet Value (USD)")
    plt.grid(color='gray', linestyle='--', linewidth=0.5)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=5))

    plt.tight_layout()
    plt.pause(0.01)
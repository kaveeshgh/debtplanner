import matplotlib
matplotlib.use('Agg')  # non-interactive backend required for server use — no display needed
import matplotlib.pyplot as plt
import numpy as np
import io
import base64


def fig_to_base64(fig):
    """Convert a matplotlib figure to a base64 PNG string the frontend can use in an <img> tag"""
    buffer = io.BytesIO()  # in-memory file — no disk write needed
    fig.savefig(buffer, format='png', bbox_inches='tight',
                facecolor='#111111', edgecolor='none', dpi=120)
    buffer.seek(0)  # rewind buffer to start before reading
    encoded = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)  # free memory — important on a server
    return f"data:image/png;base64,{encoded}"  # format React can put directly in <img src>


def apply_dark_theme(ax):
    """Apply consistent dark styling to any matplotlib axes object"""
    ax.set_facecolor('#1a1a1a')
    ax.tick_params(colors='#aaaaaa', which='both')
    ax.xaxis.label.set_color('#aaaaaa')
    ax.yaxis.label.set_color('#aaaaaa')
    ax.title.set_color('white')
    # style all four border lines
    for spine in ax.spines.values():
        spine.set_color('#444444')
    ax.grid(True, color='#333333', linestyle='--', alpha=0.6)


def generate_balance_chart(avalanche_timeline, snowball_timeline):
    """
    Line chart showing total debt balance decreasing over time.
    One line per strategy — avalanche in purple, snowball in green.
    The shaded region between them shows where the strategies diverge.
    """
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor('#111111')
    apply_dark_theme(ax)

    # unpack timeline dicts into separate lists for plotting
    av_months   = [point['month']   for point in avalanche_timeline]
    av_balances = [point['balance'] for point in avalanche_timeline]
    sn_months   = [point['month']   for point in snowball_timeline]
    sn_balances = [point['balance'] for point in snowball_timeline]

    # main lines
    ax.plot(av_months, av_balances, color='#8884d8', linewidth=2.5,
            label='Avalanche (highest rate first)')
    ax.plot(sn_months, sn_balances, color='#82ca9d', linewidth=2.5,
            label='Snowball (smallest balance first)')

    # shade the gap between strategies so the difference is visible
    min_len = min(len(av_months), len(sn_months))
    ax.fill_between(av_months[:min_len],
                    av_balances[:min_len],
                    sn_balances[:min_len],
                    alpha=0.08, color='#ffffff')

    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Remaining Balance ($)', fontsize=11)
    ax.set_title('Debt Balance Over Time — Avalanche vs Snowball', fontsize=13, pad=15)

    # format y axis as dollar amounts
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend(facecolor='#222222', labelcolor='white', edgecolor='#444444', fontsize=10)

    plt.tight_layout()
    return fig_to_base64(fig)


def generate_monte_carlo_chart(mc_results):
    """
    Grouped bar chart comparing best/median/worst case payoff months
    for avalanche vs snowball strategies side by side.
    Each bar is labelled with both months and years for clarity.
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('#111111')
    apply_dark_theme(ax)

    # three scenario categories on x axis
    categories = ['Best Case\n(10th %ile)', 'Median\n(50th %ile)', 'Worst Case\n(90th %ile)']

    # pull values out of the results dict
    avalanche_values = [
        mc_results['avalanche']['best_case'],
        mc_results['avalanche']['median'],
        mc_results['avalanche']['worst_case']
    ]
    snowball_values = [
        mc_results['snowball']['best_case'],
        mc_results['snowball']['median'],
        mc_results['snowball']['worst_case']
    ]

    # position two bars side by side at each x position
    x = np.arange(len(categories))
    bar_width = 0.35

    bars_av = ax.bar(x - bar_width / 2, avalanche_values, bar_width,
                     label='Avalanche', color='#8884d8', alpha=0.85)
    bars_sn = ax.bar(x + bar_width / 2, snowball_values, bar_width,
                     label='Snowball', color='#82ca9d', alpha=0.85)

    # add text labels on top of each bar showing months and years
    for bar in bars_av:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1,
                f'{int(h)}mo\n({h / 12:.1f}yr)',
                ha='center', va='bottom', color='#cccccc', fontsize=8)

    for bar in bars_sn:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1,
                f'{int(h)}mo\n({h / 12:.1f}yr)',
                ha='center', va='bottom', color='#cccccc', fontsize=8)

    ax.set_xlabel('Scenario', fontsize=11)
    ax.set_ylabel('Months to Payoff', fontsize=11)
    ax.set_title('Monte Carlo: Payoff Range Comparison (1,000 Simulations)', fontsize=13, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, color='#aaaaaa')
    ax.legend(facecolor='#222222', labelcolor='white', edgecolor='#444444', fontsize=10)

    plt.tight_layout()
    return fig_to_base64(fig)


def generate_schedule_chart(df):
    """
    Two-panel chart for the amortization schedule.
    Top panel: stacked area showing monthly interest vs principal paid.
    Bottom panel: remaining balance line vs cumulative interest line.
    sharex=True links the x axes so they scroll together.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 9), sharex=True)
    fig.patch.set_facecolor('#111111')
    apply_dark_theme(ax1)
    apply_dark_theme(ax2)

    # extract columns from the pandas dataframe as plain lists
    months             = df['month'].tolist()
    monthly_interest   = df['total_interest'].tolist()
    monthly_principal  = df['total_principal'].tolist()
    balance            = df['total_balance'].tolist()
    cumulative_interest = df['cumulative_interest'].tolist()

    # --- top panel: stacked area of monthly interest vs principal ---
    ax1.stackplot(months,
                  monthly_interest,
                  monthly_principal,
                  labels=['Interest', 'Principal'],
                  colors=['#ff6b6b', '#82ca9d'],
                  alpha=0.75)
    ax1.set_ylabel('Monthly Amount ($)', fontsize=10)
    ax1.set_title('Monthly Payment Breakdown — Interest vs Principal', fontsize=12, pad=10)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax1.legend(facecolor='#222222', labelcolor='white', edgecolor='#444444', fontsize=9)

    # --- bottom panel: balance and cumulative interest over time ---
    ax2.plot(months, balance, color='#8884d8', linewidth=2.5, label='Remaining Balance')
    ax2.plot(months, cumulative_interest, color='#ff6b6b', linewidth=2,
             linestyle='--', label='Cumulative Interest Paid')
    ax2.set_xlabel('Month', fontsize=10)
    ax2.set_ylabel('Amount ($)', fontsize=10)
    ax2.set_title('Remaining Balance vs Total Interest Paid Over Time', fontsize=12, pad=10)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax2.legend(facecolor='#222222', labelcolor='white', edgecolor='#444444', fontsize=9)

    plt.tight_layout(pad=2.5)
    return fig_to_base64(fig)

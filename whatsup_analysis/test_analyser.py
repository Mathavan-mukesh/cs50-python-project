import pandas as pd
from helper import (
    fetch_stats, most_busy_users, create_wordcloud, most_common_words,
    emoji_helper, monthly_timeline, daily_timeline, week_activity_map,
    month_activity_map, activity_heatmap
)

# Sample test data
sample_data = {
    'user': ['Alice', 'Bob', 'Alice', 'group_notification', 'Alice'],
    'message': ['Hello there!', '<Media omitted>\n', 'Check this out https://example.com', 'Bob added Alice', '😊❤️'],
    'year': [2023, 2023, 2023, 2023, 2023],
    'month_num': [1, 1, 1, 1, 1],
    'month': ['January', 'January', 'January', 'January', 'January'],
    'only_date': ['2023-01-01'] * 5,
    'day_name': ['Sunday'] * 5,
    'period': ['12-1', '1-2', '2-3', '3-4', '4-5']
}

df = pd.DataFrame(sample_data)

def test_fetch_stats():
    stats = fetch_stats('Alice', df)
    assert stats[0] == 3  # Alice has 3 messages
    assert stats[2] == 0  # No media for Alice (other is from Bob)
    assert stats[3] == 1  # One link from Alice

def test_most_busy_users():
    top_users, percent_df = most_busy_users(df)
    assert top_users.index[0] == 'Alice'
    assert round(percent_df['percent'].iloc[0], 2) == 60.0

def test_most_common_words():
    common_words_df = most_common_words('Alice', df)
    assert 'hello' in common_words_df[0].values or 'check' in common_words_df[0].values

def test_emoji_helper():
    emoji_df = emoji_helper('Alice', df)
    assert '😊' in emoji_df[0].values
    assert '❤️' in emoji_df[0].values

def test_monthly_timeline():
    timeline = monthly_timeline('Alice', df)
    assert timeline['time'].iloc[0] == 'January-2023'
    assert timeline['message'].iloc[0] == 3

def test_daily_timeline():
    daily = daily_timeline('Alice', df)
    assert daily['message'].iloc[0] == 3

def test_week_activity_map():
    result = week_activity_map('Alice', df)
    assert result['Sunday'] == 3

def test_month_activity_map():
    result = month_activity_map('Alice', df)
    assert result['January'] == 3

def test_activity_heatmap():
    heatmap = activity_heatmap('Alice', df)
    assert heatmap.loc['Sunday', '12-1'] == 1

# Optional: WordCloud test (this just checks if it runs)
def test_create_wordcloud_runs():
    wc = create_wordcloud('Alice', df)
    assert wc is not None

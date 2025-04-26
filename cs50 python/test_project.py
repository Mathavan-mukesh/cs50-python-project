import unittest
import pandas as pd
from utils import preprocessor, helper


class TestWhatsAppAnalyzer(unittest.TestCase):

    def setUp(self):
        # sample chat data
        self.raw_data = """12/12/2022, 10:00 AM - User1: Hello!
12/12/2022, 10:01 AM - User2: Hi there!
12/12/2022, 10:05 AM - User1: How are you?
12/12/2022, 10:07 AM - User2: I'm good, thanks! 😊
12/12/2022, 10:10 AM - User1: Check this out!
<Media omitted>"""

        self.df = preprocessor.preprocess(self.raw_data)

    def test_preprocessing(self):
        # Test if preprocessing returns a DataFrame
        self.assertIsInstance(self.df, pd.DataFrame)
        # Test if essential columns exist
        self.assertIn('user', self.df.columns)
        self.assertIn('message', self.df.columns)

    def test_fetch_stats(self):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats('Overall', self.df)
        self.assertEqual(num_messages, 5)
        self.assertEqual(num_media_messages, 1)

    def test_monthly_timeline(self):
        timeline = helper.monthly_timeline('Overall', self.df)
        self.assertIsInstance(timeline, pd.DataFrame)
        self.assertIn('time', timeline.columns)
        self.assertIn('message', timeline.columns)

    def test_daily_timeline(self):
        timeline = helper.daily_timeline('Overall', self.df)
        self.assertIsInstance(timeline, pd.DataFrame)
        self.assertIn('only_date', timeline.columns)
        self.assertIn('message', timeline.columns)

    def test_week_activity_map(self):
        week_map = helper.week_activity_map('Overall', self.df)
        self.assertIsInstance(week_map, pd.Series)

    def test_month_activity_map(self):
        month_map = helper.month_activity_map('Overall', self.df)
        self.assertIsInstance(month_map, pd.Series)

    def test_activity_heatmap(self):
        heatmap = helper.activity_heatmap('Overall', self.df)
        self.assertIsInstance(heatmap, pd.DataFrame)

    def test_most_common_words(self):
        common_words = helper.most_common_words('Overall', self.df)
        self.assertIsInstance(common_words, pd.DataFrame)

    def test_emoji_helper(self):
        emoji_df = helper.emoji_helper('Overall', self.df)
        self.assertIsInstance(emoji_df, pd.DataFrame)

    def test_create_wordcloud(self):
        wc = helper.create_wordcloud('Overall', self.df)
        self.assertIsNotNone(wc)  # wordcloud object is created


if __name__ == '__main__':
    unittest.main()

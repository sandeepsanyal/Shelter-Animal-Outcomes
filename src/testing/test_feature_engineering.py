import unittest
from src.feature_engineering import create_features, transform_features

class TestFeatureEngineering(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.sample_data = [
            {'AgeuponOutcome': '1 year', 'SexuponOutcome': 'Neutered Male', 'Breed': 'Labrador Retriever Mix'},
            {'AgeuponOutcome': '2 years', 'SexuponOutcome': 'Spayed Female', 'Breed': 'German Shepherd'},
            {'AgeuponOutcome': '3 months', 'SexuponOutcome': 'Intact Male', 'Breed': 'Beagle'},
        ]

    def test_create_features(self):
        # Test the feature creation function
        features = create_features(self.sample_data)
        self.assertIn('Age_in_months', features[0])
        self.assertEqual(features[0]['Age_in_months'], 12)

    def test_transform_features(self):
        # Test the feature transformation function
        transformed_data = transform_features(self.sample_data)
        self.assertIn('Sex', transformed_data[0])
        self.assertEqual(transformed_data[0]['Sex'], 'Neutered')

if __name__ == '__main__':
    unittest.main()
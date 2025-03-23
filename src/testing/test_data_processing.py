import pandas as pd
import pytest
from src.data_processing import load_data, preprocess_data

def test_load_data():
    # Test loading the train dataset
    train_data = load_data('data/train.csv')
    assert isinstance(train_data, pd.DataFrame)
    assert not train_data.empty
    assert 'OutcomeType' in train_data.columns

    # Test loading the test dataset
    test_data = load_data('data/test.csv')
    assert isinstance(test_data, pd.DataFrame)
    assert not test_data.empty
    assert 'ID' in test_data.columns

def test_preprocess_data():
    # Test preprocessing on the train dataset
    train_data = load_data('data/train.csv')
    processed_train_data = preprocess_data(train_data)
    assert 'OutcomeType' in processed_train_data.columns
    assert processed_train_data['OutcomeType'].isnull().sum() == 0

    # Test preprocessing on the test dataset
    test_data = load_data('data/test.csv')
    processed_test_data = preprocess_data(test_data)
    assert 'ID' in processed_test_data.columns
    assert processed_test_data['AnimalType'].isnull().sum() == 0

# Run the tests
if __name__ == "__main__":
    pytest.main()
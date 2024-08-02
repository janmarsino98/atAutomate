import unittest
from unittest.mock import patch, Mock, call
import pandas as pd
import os
import scraper  # Asegúrate de que el nombre del archivo original sea `scraper.py` o cambia esto según corresponda

class TestScraper(unittest.TestCase):

    @patch('scraper.requests.get')
    def test_get_response(self, mock_get):
        mock_response = Mock()
        expected_data = {'tasks': []}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        data = scraper.get_response()
        self.assertEqual(data, expected_data)

    def test_get_tasks(self):
        data = {
            "tasks": [
                {"slug": "test-slug-1", "name": "Test Task 1", "price": 100, "state": "posted", "bid_on": False},
                {"slug": "test-slug-2", "name": "Test Task 2", "price": 200, "state": "posted", "bid_on": True},
            ]
        }
        tasks = scraper.get_tasks(data)
        expected_tasks = [
            {"slug": "test-slug-1", "name": "Test Task 1", "price": 100, "state": "posted", "bid_on": False},
            {"slug": "test-slug-2", "name": "Test Task 2", "price": 200, "state": "posted", "bid_on": True},
        ]
        self.assertEqual(tasks, expected_tasks)

    @patch('scraper.pd.DataFrame.to_excel')
    @patch('scraper.pd.read_excel')
    @patch('scraper.os.path.isfile')
    def test_store_tasks(self, mock_isfile, mock_read_excel, mock_to_excel):
        tasks = [
            {"slug": "test-slug-1", "name": "Test Task 1", "price": 100, "state": "posted", "bid_on": False},
            {"slug": "test-slug-2", "name": "Test Task 2", "price": 200, "state": "posted", "bid_on": True},
        ]
        df_path = 'test_db.xlsx'
        
        # Simular que el archivo no existe
        mock_isfile.return_value = False

        with patch('scraper.c.DDBB_PATH', df_path):
            scraper.store_tasks(tasks)
            
            # Verificar que to_excel fue llamado
            self.assertTrue(mock_to_excel.called)
            
            # Recuperar el DataFrame pasado a to_excel
            df = mock_to_excel.call_args[0][0]  # DataFrame pasado a to_excel
            
            # Imprimir el DataFrame para depuración
            print("Contenido del DataFrame en test_store_tasks:")
            print(df)
            
            # Verificar que el DataFrame tiene los datos correctos
            self.assertEqual(len(df), 2)
            self.assertIn("classification", df.columns)
            self.assertIn("applied", df.columns)
            self.assertEqual(df.at[0, "slug"], "test-slug-1")
            self.assertEqual(df.at[1, "slug"], "test-slug-2")
            self.assertEqual(df.at[0, "classification"], "")
            self.assertEqual(df.at[0, "applied"], "No")
            self.assertEqual(df.at[1, "classification"], "")
            self.assertEqual(df.at[1, "applied"], "No")

    @patch('scraper.pd.DataFrame.to_excel')
    @patch('scraper.pd.read_excel')
    @patch('scraper.os.path.isfile')
    def test_store_tasks_existing_file(self, mock_isfile, mock_read_excel, mock_to_excel):
        tasks = [
            {"slug": "test-slug-3", "name": "Test Task 3", "price": 300, "state": "posted", "bid_on": False},
        ]
        df_path = 'test_db.xlsx'
        
        # Simular que el archivo existe
        mock_isfile.return_value = True
        
        # Simular un DataFrame existente retornado por read_excel
        existing_df = pd.DataFrame([
            {"slug": "test-slug-1", "name": "Test Task 1", "price": 100, "state": "posted", "bid_on": False, "classification": "", "applied": "No"},
            {"slug": "test-slug-2", "name": "Test Task 2", "price": 200, "state": "posted", "bid_on": True, "classification": "", "applied": "No"},
        ])
        mock_read_excel.return_value = existing_df

        with patch('scraper.c.DDBB_PATH', df_path):
            scraper.store_tasks(tasks)
            
            # Verificar que to_excel fue llamado
            self.assertTrue(mock_to_excel.called)
            
            # Recuperar el DataFrame pasado a to_excel
            df = mock_to_excel.call_args[0][0]  # DataFrame pasado a to_excel
            
            # Imprimir el DataFrame para depuración
            print("Contenido del DataFrame en test_store_tasks_existing_file:")
            print(df)
            
            # Verificar que el DataFrame tiene los datos correctos
            self.assertEqual(len(df), 3)
            self.assertIn("classification", df.columns)
            self.assertIn("applied", df.columns)
            self.assertEqual(df.at[0, "slug"], "test-slug-1")
            self.assertEqual(df.at[1, "slug"], "test-slug-2")
            self.assertEqual(df.at[2, "slug"], "test-slug-3")
            self.assertEqual(df.at[0, "classification"], "")
            self.assertEqual(df.at[0, "applied"], "No")
            self.assertEqual(df.at[1, "classification"], "")
            self.assertEqual(df.at[1, "applied"], "No")
            self.assertEqual(df.at[2, "classification"], "")
            self.assertEqual(df.at[2, "applied"], "No")

if __name__ == '__main__':
    unittest.main()

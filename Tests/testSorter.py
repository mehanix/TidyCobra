import unittest 
from unittest.mock import patch
from tempfile import mkdtemp
from shutil import rmtree
from Utils.sorter import sortFolderByExtensions
from os import path, makedirs

class TestSorter(unittest.TestCase):
    
    def setUp(self) -> None:
        
        self.tempDirectory:str = mkdtemp()
        self.sourceDirectory:str = path.join(self.tempDirectory,'source')
        self.firstDestinationDirectory:str = path.join(self.tempDirectory,'dest1')
        self.secondDestinationDirectory:str = path.join(self.tempDirectory,'dest2')

        makedirs(self.sourceDirectory)
        makedirs(self.firstDestinationDirectory)
        makedirs(self.secondDestinationDirectory)

        open(path.join(self.sourceDirectory, 'test1.txt'), 'w').close()
        open(path.join(self.sourceDirectory, 'test2.doc'), 'w').close()
        open(path.join(self.sourceDirectory, 'test3.jpg'), 'w').close()
        open(path.join(self.sourceDirectory, 'test4.pdf'), 'w').close()
        open(path.join(self.sourceDirectory, 'test5.xyz'), 'w').close()
        open(path.join(self.sourceDirectory, 'test6.JPG'), 'w').close()

        self.testRule:dict = {
            "sourceFolder": self.sourceDirectory,
            "destinationFolders": [
                {
                    "extensions": [".txt", ".doc"],
                    "destinationPath": self.firstDestinationDirectory
                },
                {
                    "extensions": [".pdf", ".jpg"],
                    "destinationPath": self.secondDestinationDirectory
                }
            ]
        }

    def tearDown(self) -> None:

        rmtree(self.tempDirectory)

    def test_SuccessfulSort(self) -> None:
        
        result:dict = sortFolderByExtensions(self.testRule)

        self.assertEqual(result['successCount'],5)
        self.assertEqual(result['failCount'], 0)
        self.assertEqual(result['message'], 'Success!')

        self.assertTrue(path.exists(path.join(self.firstDestinationDirectory, 'test1.txt')))
        self.assertTrue(path.exists(path.join(self.firstDestinationDirectory, 'test2.doc')))
        self.assertTrue(path.exists(path.join(self.secondDestinationDirectory, 'test3.jpg')))
        self.assertTrue(path.exists(path.join(self.secondDestinationDirectory, 'test4.pdf')))

        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test5.xyz')))
        self.assertTrue(path.exists(path.join(self.secondDestinationDirectory, 'test6.JPG')))

    def test_ExtensionsWithoutLeadingDot(self) -> None:

        rule:dict = {
            "sourceFolder": self.sourceDirectory,
            "destinationFolders": [
                {
                    "extensions": ["txt", "doc"],
                    "destinationPath": self.firstDestinationDirectory
                }
            ]
        }

        result:dict = sortFolderByExtensions(rule)

        self.assertEqual(result['successCount'], 2)
        self.assertEqual(result['failCount'], 0)
        self.assertEqual(result['message'], 'Success!')

        self.assertTrue(path.exists(path.join(self.firstDestinationDirectory, 'test1.txt')))
        self.assertTrue(path.exists(path.join(self.firstDestinationDirectory, 'test2.doc')))

    def test_InvalidSource(self) -> None:

        invalidRule:dict = self.testRule.copy()
        invalidRule['sourceFolder'] = path.join(self.sourceDirectory,'nonExistingDirectory')

        result:dict = sortFolderByExtensions(invalidRule)

        self.assertEqual(result['successCount'], 0)
        self.assertEqual(result['failCount'], 0)
        self.assertTrue('does not exist' in result['message'])

        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test1.txt')))
        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test2.doc')))
        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test3.jpg')))
        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test4.pdf')))
        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test6.JPG')))

    def test_DuplicateHandling(self) -> None:

        open(path.join(self.secondDestinationDirectory, 'test4.pdf'), 'w').close()

        sortFolderByExtensions(self.testRule)

        self.assertTrue(path.exists(path.join(self.secondDestinationDirectory, 'test4.pdf')))
        self.assertTrue(path.exists(path.join(self.secondDestinationDirectory, 'd1_test4.pdf')))

    @patch('Utils.sorter.move')
    def test_PermissionDenied(self,mockMove) -> None:

        mockMove.side_effect = PermissionError()

        result:dict = sortFolderByExtensions(self.testRule)
        

        self.assertEqual(result['successCount'], 0)
        self.assertEqual(result['failCount'], 5)
        self.assertEqual(result['message'], 'Access denied for some files!')

        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test1.txt')))
        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test2.doc')))
        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test3.jpg')))
        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test4.pdf')))
        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test6.JPG')))


# to run this use: python -m unittest Tests.testSorter
if __name__ == "__main__":
    
    unittest.main()

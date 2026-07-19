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

        self.assertEqual(result['successCount'],4)
        self.assertEqual(result['failCount'], 0)
        self.assertEqual(result['message'], 'Success!')

        self.assertTrue(path.exists(path.join(self.firstDestinationDirectory, 'test1.txt')))
        self.assertTrue(path.exists(path.join(self.firstDestinationDirectory, 'test2.doc')))
        self.assertTrue(path.exists(path.join(self.secondDestinationDirectory, 'test3.jpg')))
        self.assertTrue(path.exists(path.join(self.secondDestinationDirectory, 'test4.pdf')))

        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test5.xyz')))

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
        self.assertEqual(result['failCount'], 4)
        self.assertEqual(result['message'], 'Access denied for some files!')

        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test1.txt')))
        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test2.doc')))
        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test3.jpg')))
        self.assertTrue(path.exists(path.join(self.sourceDirectory, 'test4.pdf')))
#new test added to check for move failures not losing files
    @patch('Utils.sorter.move')
    def test_MoveFailureDoesNotLoseFile(self, mockMove) -> None:
        #simulates mid-operation write failure
        mockMove.side_effect = IOError("Simulated mid-operation write failure")

        #writes content to be checked again
        test_file_path = path.join(self.sourceDirectory, 'test1.txt')
        with open(test_file_path, 'w') as f:
            f.write("Important Original Data")

        #runs sorter
        result: dict = sortFolderByExtensions(self.testRule)

        self.assertEqual(result['successCount'], 0)
        
        #checking if original file still exists
        self.assertTrue(path.exists(test_file_path), "CRITICAL ERROR: Source file was lost after failed move!")
        with open(test_file_path, 'r') as f:
            self.assertEqual(f.read(), "Important Original Data", "CRITICAL ERROR: File content was corrupted or cleared!")

# to run this use: python -m unittest Tests.testSorter
if __name__ == "__main__":
    
    unittest.main()
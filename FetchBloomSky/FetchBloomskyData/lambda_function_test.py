import unittest
#import import_lib
import lambda_function
# lambda_function = input('lambda_function')
# importlib.import_module(lambda_function)

class TestBloomskyPython(unittest.TestCase):
    
    def testChangeDateFormat(self):
        ts = 1558925920
        print(lambda_function.changeDateFormat(ts))
        self.assertEquals("2019-05-26_20:58", lambda_function.changeDateFormat(ts))
        
        
    def testGetS3KeyName(self):
        sampleUrl = "http://s3-us-west-1.amazonaws.com/bskyimgs/faBiuZWsnpaorqi2qJ1lq52wl5immJY=.jpg"
        print(lambda_function.getS3KeyName(sampleUrl))
        self.assertEquals("faBiuZWsnpaorqi2qJ1lq52wl5immJY=.jpg", lambda_function.getS3KeyName(sampleUrl))
        
if __name__ == '__main__':
    unittest.main()
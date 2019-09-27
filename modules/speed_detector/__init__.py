from .speed_detector import *

package_directory = os.path.dirname(os.path.abspath(__file__))

with open(package_directory + "/digit_detector.pkl",'rb') as file:
        digit_detector = pickle.load(file)
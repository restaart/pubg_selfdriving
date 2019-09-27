from .azimuth_detector import *

package_directory = os.path.dirname(os.path.abspath(__file__))

print(package_directory)

with open(package_directory + '/azimut_digit_detector_clf.plk', 'rb') as f:
    azimut_digit_detector_clf = pickle.load(f)

with open(package_directory + '/azimut_percise_detector_clf.plk', 'rb') as f:
    azimut_percise_detector_clf = pickle.load(f)
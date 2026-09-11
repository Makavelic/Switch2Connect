import hashlib
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from dualsense_descriptors import (  # noqa: E402
    DUALSENSE_CONFIGURATION_DESCRIPTOR,
    DUALSENSE_CONFIGURATION_DESCRIPTOR_NO_AUDIO,
    DUALSENSE_HID_REPORT_DESCRIPTOR,
    DUALSENSE_MIC_BYTES_PER_INTERVAL,
    DUALSENSE_STRING_PRODUCT,
    DUALSENSE_USBIP_SPEED,
)


# Physical CFI-ZCT1 descriptor capture:
# https://github.com/nondebug/dualsense/blob/main/lsusb-descriptor-info.txt
PHYSICAL_CONFIGURATION_SHA256 = (
    "a3fb919f2a70bcbd67ba6fb7efc5016f8ef7dc43790f8f0f6e11f06881a22816"
)
PHYSICAL_HID_REPORT_SHA256 = (
    "7587a72ee49550f24da50cbbad203742a0eb9aefbb753c2aaa5bedf8466c0d33"
)


class DualSenseDescriptorTests(unittest.TestCase):
    def test_configuration_matches_physical_controller(self):
        descriptor = DUALSENSE_CONFIGURATION_DESCRIPTOR

        self.assertEqual(len(descriptor), 227)
        self.assertEqual(int.from_bytes(descriptor[2:4], "little"), len(descriptor))
        self.assertEqual(
            hashlib.sha256(descriptor).hexdigest(),
            PHYSICAL_CONFIGURATION_SHA256,
        )

    def test_hid_report_matches_physical_controller(self):
        descriptor = DUALSENSE_HID_REPORT_DESCRIPTOR

        self.assertEqual(len(descriptor), 273)
        self.assertEqual(
            hashlib.sha256(descriptor).hexdigest(),
            PHYSICAL_HID_REPORT_SHA256,
        )

    def test_hid_only_configuration_advertises_the_same_report_length(self):
        descriptor = DUALSENSE_CONFIGURATION_DESCRIPTOR_NO_AUDIO

        self.assertEqual(len(descriptor), 41)
        self.assertEqual(int.from_bytes(descriptor[2:4], "little"), len(descriptor))
        self.assertIn(b"\x09\x21\x11\x01\x00\x01\x22\x11\x01", descriptor)

    def test_product_name_matches_physical_controller(self):
        descriptor = DUALSENSE_STRING_PRODUCT
        product_name = descriptor[2:].decode("utf-16le")

        self.assertEqual(product_name, "Wireless Controller")

    def test_usb_timing_matches_physical_controller(self):
        self.assertEqual(DUALSENSE_USBIP_SPEED, 3)
        self.assertEqual(DUALSENSE_MIC_BYTES_PER_INTERVAL, 192)


if __name__ == "__main__":
    unittest.main()

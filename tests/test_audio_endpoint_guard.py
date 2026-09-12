import ctypes
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from audio_endpoint_guard import DualSenseAudioEndpointGuard


@unittest.skipUnless(sys.platform == "win32", "Windows COM ABI")
class AudioEndpointGuardTests(unittest.TestCase):
    def test_property_value_buffer_matches_native_propvariant_size(self):
        guard = DualSenseAudioEndpointGuard()
        self.assertTrue(guard._ensure_interfaces_ready())
        # PROPVARIANT includes BLOB/counted-array members even for string reads.
        # IPropertyStore::GetValue may initialize the entire native structure.
        expected_size = 24 if ctypes.sizeof(ctypes.c_void_p) == 8 else 16
        self.assertEqual(ctypes.sizeof(guard._PROPVARIANT), expected_size)
        self.assertEqual(guard._PROPVARIANT.union.offset, 8)


if __name__ == "__main__":
    unittest.main()

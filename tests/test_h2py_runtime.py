import unittest


from harmony_model_checker.h2py.h2py_runtime import H, P, HAddr, HDict, hcompare


class TestH2PyRuntimeH(unittest.TestCase):
    
    def test_none(self):
        self.assertIsNone(H(None))

    def test_int(self):
        self.assertEqual(H(42), 42)

    def test_true(self):
        self.assertEqual(H(True), True)

    def test_false(self):
        self.assertEqual(H(False), False)

    def test_dict_1(self):
        self.assertEqual(
            H({ True: False, 0: 1 }),
            HDict({ True: False, 0: 1 })
        )

    def test_dict_2(self):
        self.assertEqual(
            H({ H({ True: False }): H({ 0: 1 }) }),
            HDict({ HDict({ True: False }): HDict({ 0: 1 }) })
        )

    def test_addr_1(self):
        self.assertIsNone(H(None))


class TestH2PyRuntimeP(unittest.TestCase):

    def test_none(self):
        self.assertIsNone(P(None))

    def test_int(self):
        self.assertEqual(P(42), 42)

    def test_true(self):
        self.assertEqual(P(True), True)

    def test_false(self):
        self.assertEqual(P(False), False)


class TestH2PyRuntimeHcompare(unittest.TestCase):

    def test_typeorder(self):
        self.assertLess(hcompare(H(False), H(42)), 0)
        self.assertLess(hcompare(H(False), H("abc")), 0)
        self.assertLess(hcompare(H(False), H({})), 0)
        self.assertLess(hcompare(H(False), HAddr(("x",))), 0)
        self.assertLess(hcompare(H(42), H("abc")), 0)
        self.assertLess(hcompare(H(42), H({})), 0)
        self.assertLess(hcompare(H(42), HAddr(("x",))), 0)
        self.assertLess(hcompare(H("abc"), H({})), 0)
        self.assertLess(hcompare(H("abc"), HAddr(("x",))), 0)
        self.assertLess(hcompare(H({}), HAddr(("x",))), 0)

    def test_int(self):
        self.assertLess(hcompare(H(42), H(43)), 0)
        self.assertEqual(hcompare(H(42), H(42)), 0)
        self.assertGreater(hcompare(H(43), H(42)), 0)

    def test_bool(self):
        self.assertEqual(hcompare(H(False), H(False)), 0)
        self.assertLess(hcompare(H(False), H(True)), 0)
        self.assertGreater(hcompare(H(True), H(False)), 0)
        self.assertEqual(hcompare(H(True), H(True)), 0)

    def test_atom(self):
        self.assertLess(hcompare(H("abc"), H("abcd")), 0)
        self.assertLess(hcompare(H("abc"), H("abd")), 0)
        self.assertEqual(hcompare(H("abc"), H("abc")), 0)
        self.assertGreater(hcompare(H("abcd"), H("abc")), 0)
        self.assertGreater(hcompare(H("abd"), H("abc")), 0)

    def test_dict(self):
        self.assertLess(hcompare(H({}), H({0: 1})), 0)
        self.assertEqual(hcompare(H({0: 1}), H({0: 1})), 0)
        self.assertGreater(hcompare(H({0: 1, 2: 3}), H({0: 1})), 0)

    def test_addr(self):
        self.assertLess(hcompare(H(None), HAddr(("x",))), 0)
        self.assertEqual(hcompare(HAddr(("x",)), HAddr(("x",))), 0)
        self.assertGreater(hcompare(HAddr(("x", "y")), HAddr(("x",))), 0)


if __name__ == '__main__':
    unittest.main()

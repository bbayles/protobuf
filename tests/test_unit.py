#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Runs unit tests.

eigenein (c) 2011
"""

from __future__ import absolute_import, print_function

import io
import unittest

from pure_protobuf.protobuf import (
    Bool,
    Bytes,
    EmbeddedMessage,
    Flags,
    Float32,
    Int32,
    Int64,
    MessageType,
    TypeMetadata,
    UInt64,
    Unicode,
    UVarint,
    Varint,
)


class TestUVarint(unittest.TestCase):
    def test_dumps_1(self):
        self.assertEqual(UVarint.dumps(0), b"\x00")

    def test_dumps_2(self):
        self.assertEqual(UVarint.dumps(3), b"\x03")

    def test_dumps_3(self):
        self.assertEqual(UVarint.dumps(270), b"\x8E\x02")

    def test_dumps_4(self):
        self.assertEqual(UVarint.dumps(86942), b"\x9E\xA7\x05")

    def test_loads_1(self):
        self.assertEqual(UVarint.loads(b"\x00"), 0)

    def test_loads_2(self):
        self.assertEqual(UVarint.loads(b"\x03"), 3)

    def test_loads_3(self):
        self.assertEqual(UVarint.loads(b"\x8E\x02"), 270)

    def test_loads_4(self):
        self.assertEqual(UVarint.loads(b"\x9E\xA7\x05"), 86942)


class TestVarint(unittest.TestCase):
    def test_dumps_1(self):
        self.assertEqual(Varint.dumps(0), b"\x00")

    def test_dumps_2(self):
        self.assertEqual(Varint.dumps(-1), b"\x01")

    def test_dumps_3(self):
        self.assertEqual(Varint.dumps(1), b"\x02")

    def test_dumps_4(self):
        self.assertEqual(Varint.dumps(-2), b"\x03")

    def test_loads_1(self):
        self.assertEqual(Varint.loads(b"\x00"), 0)

    def test_loads_2(self):
        self.assertEqual(Varint.loads(b"\x01"), -1)

    def test_loads_3(self):
        self.assertEqual(Varint.loads(b"\x02"), 1)

    def test_loads_4(self):
        self.assertEqual(Varint.loads(b"\x03"), -2)


class TestBool(unittest.TestCase):
    def test_dumps_1(self):
        self.assertEqual(Bool.dumps(True), b"\x01")
        self.assertEqual(Bool.dumps(False), b"\x00")

    def test_loads_1(self):
        self.assertEqual(Bool.loads(b"\x00"), False)
        self.assertEqual(Bool.loads(b"\x01"), True)


class TestUInt64(unittest.TestCase):
    def test_dumps_1(self):
        self.assertEqual(UInt64.dumps(1), b"\x00\x00\x00\x00\x00\x00\x00\x01")

    def test_loads_1(self):
        self.assertEqual(UInt64.loads(b"\x00\x00\x00\x00\x00\x00\x00\x01"), 1)


class TestInt64(unittest.TestCase):
    def test_dumps_1(self):
        self.assertEqual(Int64.dumps(-2), b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE")

    def test_loads_1(self):
        self.assertEqual(Int64.loads(b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE"), -2)


class TestInt32(unittest.TestCase):
    def test_dumps_1(self):
        self.assertEqual(Int32.dumps(-2), b"\xFF\xFF\xFF\xFE")

    def test_loads_1(self):
        self.assertEqual(Int32.loads(b"\xFF\xFF\xFF\xFE"), -2)


class TestBytes(unittest.TestCase):
    def test_dumps_1(self):
        self.assertEqual(
            Bytes.dumps(b"testing"), b"\x07\x74\x65\x73\x74\x69\x6e\x67"
        )

    def test_loads_1(self):
        self.assertEqual(
            Bytes.loads(b"\x07\x74\x65\x73\x74\x69\x6e\x67"), b"testing"
        )


class TestUnicode(unittest.TestCase):
    def test_dumps_1(self):
        self.assertEqual(
            Unicode.dumps(u"Привет"),
            b"\x0c\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82",
        )

    def test_loads_1(self):
        self.assertEqual(
            Unicode.loads(
                b"\x0c\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82"
            ),
            u"Привет",
        )


class TestMessageType(unittest.TestCase):
    def test_dump_1(self):
        Test2 = MessageType()
        Test2.add_field(2, "b", Bytes)
        msg = Test2()
        msg.b = b"testing"
        fp = io.BytesIO()
        msg.dump(fp)
        self.assertEqual(
            fp.getvalue(), b"\x12\x07\x74\x65\x73\x74\x69\x6e\x67"
        )

    def test_dumps_1(self):
        Test2 = MessageType()
        Test2.add_field(2, "b", Bytes)
        msg = Test2()
        msg.b = b"testing"
        self.assertEqual(msg.dumps(), b"\x12\x07\x74\x65\x73\x74\x69\x6e\x67")

    def test_dumps_2(self):
        """
        Tests missing optional value.
        """
        Test2 = MessageType()
        Test2.add_field(2, "b", Bytes)
        msg = Test2()
        self.assertEqual(msg.dumps(), b"")

    def test_dumps_3(self):
        """
        Tests missing required value.
        """
        Test2 = MessageType()
        Test2.add_field(2, "b", Bytes, flags=Flags.REQUIRED)
        msg = Test2()
        with self.assertRaises(ValueError):
            msg.dumps()

    def test_dumps_4(self):
        """
        Tests repeated value.
        """
        Test2 = MessageType()
        Test2.add_field(1, "b", UVarint, flags=Flags.REPEATED)
        msg = Test2()
        msg.b = (1, 2, 3)
        self.assertEqual(msg.dumps(), b"\x08\x01\x08\x02\x08\x03")

    def test_dumps_5(self):
        """
        Tests packed repeated value.
        """
        Test4 = MessageType()
        Test4.add_field(4, "d", UVarint, flags=Flags.PACKED_REPEATED)
        msg = Test4()
        msg.d = (3, 270, 86942)
        self.assertEqual(msg.dumps(), b"\x22\x06\x03\x8E\x02\x9E\xA7\x05")

    def test_loads_1(self):
        """
        Tests missing optional value.
        """
        Test2 = MessageType()
        Test2.add_field(2, "b", Bytes)
        msg = Test2.loads(b"")
        self.assertNotIn("b", msg)

    def test_loads_1_1(self):
        """
        Tests missing required value.
        """
        Test2 = MessageType()
        Test2.add_field(2, "b", Bytes, flags=Flags.REQUIRED)
        with self.assertRaises(ValueError):
            Test2.loads(b"")

    def test_loads_2(self):
        """
        Tests that the last value in the input stream is assigned to
        a non-repeated field.
        """
        Test2 = MessageType()
        Test2.add_field(1, "b", UVarint)
        msg = Test2.loads(b"\x08\x01\x08\x02\x08\x03")
        self.assertEqual(msg.b, 3)

    def test_loads_3(self):
        """
        Tests repeated value.
        """
        Test2 = MessageType()
        Test2.add_field(1, "b", UVarint, flags=Flags.REPEATED)
        msg = Test2.loads(b"\x08\x01\x08\x02\x08\x03")
        self.assertIn("b", msg)
        self.assertEqual(msg.b, [1, 2, 3])

    def test_loads_4(self):
        """
        Tests packed repeated value.
        """
        Test4 = MessageType()
        Test4.add_field(4, "d", UVarint, flags=Flags.PACKED_REPEATED)
        msg = Test4.loads(b"\x22\x06\x03\x8E\x02\x9E\xA7\x05")
        self.assertIn("d", msg)
        self.assertEqual(msg.d, [3, 270, 86942])

    def test_hash_1(self):
        """
        Tests __hash__.
        """
        Type1, Type2, Type3, Type4 = (
            MessageType(),
            MessageType(),
            MessageType(),
            MessageType(),
        )
        Type1.add_field(1, "b", UVarint)
        Type2.add_field(1, "a", UVarint)
        Type3.add_field(2, "a", UVarint)
        Type4.add_field(1, "b", UVarint, flags=Flags.REPEATED)
        self.assertEqual(hash(Type1), hash(Type2))
        self.assertNotEqual(hash(Type1), hash(Type3))
        self.assertNotEqual(hash(Type1), hash(Type4))

    def test_iter_1(self):
        """
        Tests __iter__.
        """
        Type1 = MessageType()
        Type1.add_field(1, "b", UVarint, flags=Flags.REPEATED)
        Type1.add_field(2, "c", Bytes, flags=Flags.PACKED_REPEATED)
        i = iter(Type1)
        self.assertEqual(next(i), (1, "b", UVarint, Flags.REPEATED))
        self.assertEqual(next(i), (2, "c", Bytes, Flags.PACKED_REPEATED))

    def test_empty_optional_bytes(self):
        """
        Regression test to prove that a bytes field of length zero is loaded
        correctly.
        """
        Type1 = MessageType()
        Type1.add_field(1, "a", Bytes)
        msg = Type1.loads(b"\n\x00")
        self.assertEqual(msg.a, "")


class TestEmbeddedMessage(unittest.TestCase):
    def test_dumps_1(self):
        """
        Tests general dumps.
        """
        Test1 = MessageType()
        Test1.add_field(1, "a", UVarint)
        Test3 = MessageType()
        Test3.add_field(3, "c", EmbeddedMessage(Test1))
        msg = Test3()
        msg.c = Test1()
        msg.c.a = 150
        self.assertEqual(msg.dumps(), b"\x1a\x03\x08\x96\x01")

    def test_dumps_and_loads(self):
        """
        Tests that boundaries of embedded messages are properly read.
        """
        Type1, Type2 = MessageType(), MessageType()
        Type2.add_field(1, "a", UVarint)
        Type1.add_field(1, "a", UVarint)
        Type1.add_field(2, "b", EmbeddedMessage(Type2))
        Type1.add_field(3, "c", UVarint)
        msg = Type1()
        msg.a = 1
        msg.c = 3
        msg.b = Type2()
        msg.b.a = 2
        msg = Type1.loads(msg.dumps())
        self.assertEqual(msg.a, 1)
        self.assertEqual(msg.c, 3)
        self.assertEqual(msg.b.a, 2)

    def test_loads_1(self):
        Test1 = MessageType()
        Test1.add_field(1, "a", UVarint)
        Test3 = MessageType()
        Test3.add_field(3, "c", EmbeddedMessage(Test1))
        msg = Test3.loads(b"\x1a\x03\x08\x96\x01")
        self.assertIn("c", msg)
        self.assertIn("a", msg.c)
        self.assertEqual(msg.c.a, 150)


class TestTypeMetadata(unittest.TestCase):
    def test_dumps_1(self):
        """
        Simple test.
        """
        Test2 = MessageType()
        Test2.add_field(2, "b", Bytes)
        Type1 = MessageType()
        Type1.add_field(1, "t", TypeMetadata)
        msg = Type1()
        msg.t = Test2
        self.assertEqual(
            msg.dumps(), b"\n\x10\n\x0e\x08\x02\x12\x01b\x1a\x05Bytes \x00"
        )

    def test_loads_1(self):
        """
        Simple test.
        """
        Type1 = MessageType()
        Type1.add_field(1, "t", TypeMetadata)
        msg = Type1.loads(b"\n\x10\n\x0e\x08\x02\x12\x01b\x1a\x05Bytes \x00")
        self.assertIsInstance(msg.t, MessageType)
        i = iter(msg.t)
        self.assertEqual(next(i), (2, "b", Bytes, Flags.SIMPLE))
        self.assertRaises(StopIteration, lambda: next(i))

    def test_dumps_and_loads_1(self):
        """
        Integration test.
        """
        A, B = MessageType(), MessageType()
        A.add_field(1, "a", Bytes)
        A.add_field(2, "b", TypeMetadata)
        A.add_field(3, "c", Bytes)
        msg = A()
        msg.a = b"!"
        msg.b = B
        msg.c = b"!"
        data = msg.dumps()
        msg = A.loads(data)
        self.assertEqual(hash(msg.b), hash(B))

    def test_dumps_and_loads_2(self):
        """
        Integration test.
        """
        A, B, C = MessageType(), MessageType(), MessageType()
        A.add_field(1, "a", UVarint)
        A.add_field(2, "b", TypeMetadata, flags=Flags.REPEATED)
        A.add_field(3, "c", Bytes)
        B.add_field(4, "ololo", Float32)
        B.add_field(5, "c", TypeMetadata, flags=Flags.REPEATED)
        B.add_field(6, "d", Bool, flags=Flags.PACKED_REPEATED)
        C.add_field(7, "ghjhdf", UVarint)
        msg = A()
        msg.a = 1
        msg.b = [B, C]
        msg.c = "ololo"
        bytes = msg.dumps()
        msg = A.loads(bytes)
        self.assertEqual(hash(msg.b[0]), hash(B))
        self.assertEqual(hash(msg.b[1]), hash(C))


if __name__ == "__main__":
    unittest.main()

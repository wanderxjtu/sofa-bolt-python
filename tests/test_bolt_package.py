# coding=utf-8
"""
    Copyright (c) 2018-present, Ant Financial Service Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
   ------------------------------------------------------
   File Name : test_bolt_package
   Author : jiaqi.hjq
   Create Time : 2018/4/28 11:58
   Description : description what the main function of this file
   Change Activity:
        version0 : 2018/4/28 11:58 by jiaqi.hjq  init
"""
import unittest

from anthunder.command.heartbeat import HeartbeatRequest, HeartbeatResponse
from anthunder.protocol import BoltResponse, BoltRequest, SofaHeader
from anthunder.protocol._sofa_header import _str_to_bytes_with_len, _bytes_to_str
from anthunder.protocol.constants import PTYPE, CMDCODE, RESPSTATUS
from .proto.python import SampleServicePbResult_pb2, SampleServicePbRequest_pb2


class TestBoltPackage(unittest.TestCase):
    def test_str_to_bytes_with_len(self):
        s = "abcdefg"
        bs = _str_to_bytes_with_len(s)
        print(bs)
        self.assertEqual(bs, b'\x00\x00\x00\x07abcdefg')

    def test_repr(self):
        p = BoltResponse(SofaHeader(a='1', b='2'), b"cdefgab", ptype=PTYPE.ONEWAY, request_id=0,
                         cmdcode=CMDCODE.HEARTBEAT,
                         respstatus=1)
        print(p)
        s = p.to_stream()
        pr = BoltResponse.from_stream(s)
        self.assertNotEqual(id(p), id(pr))
        self.assertEqual(p.header, pr.header)
        self.assertEqual(p.content, pr.content)
        self.assertEqual(p.cmdcode, pr.cmdcode)
        self.assertEqual(p.request_id, pr.request_id)
        print(pr)

        p = BoltRequest(SofaHeader(a='1', b='2'), b"jklmnhi", ptype=PTYPE.ONEWAY, request_id=0,
                        cmdcode=CMDCODE.HEARTBEAT,
                        timeout=-1)
        print(p)
        s = p.to_stream()
        pr = BoltRequest.from_stream(s)
        self.assertNotEqual(id(p), id(pr))
        self.assertEqual(p.header, pr.header)
        self.assertEqual(p.content, pr.content)
        self.assertEqual(p.cmdcode, pr.cmdcode)
        self.assertEqual(p.request_id, pr.request_id)
        print(pr)

    def test_header(self):
        h = SofaHeader(keya='key1', keyabcxcs='key2')
        b = h.to_bytes()
        self.assertEqual(len(h), len(b))
        print(b)
        h_recover = SofaHeader.from_bytes(b)
        print(h_recover)
        self.assertEqual(h, h_recover)

    def test_from_stream(self):
        bs = b'\x01\x00\x00\x02\x01\x00\x00\x00\x84\x0b\x00\x00\x00\x2e\x00\x00\x00\x00\x00\x03\x63\x6f\x6d\x2e\x61\x6c\x69\x70\x61\x79\x2e\x73\x6f\x66\x61\x2e\x72\x70\x63\x2e\x63\x6f\x72\x65\x2e\x72\x65\x73\x70\x6f\x6e\x73\x65\x2e\x53\x6f\x66\x61\x52\x65\x73\x70\x6f\x6e\x73\x65\x0a\x01\x61'
        p = BoltResponse.from_stream(bs)
        self.assertEqual(p.body_len, len(bs) - p.bolt_header_size())
        print(p.content)
        re = SampleServicePbResult_pb2.SampleServicePbResult()
        re.ParseFromString(p.content)
        # print(p)
        print(re.result)
        self.assertEqual(re.result, 'a')

        bs = b'\x01\x01\x00\x01\x01\x00\x00\x00\x6d\x0b\x00\x00\x00\x64\x00\x2c\x02\xe6\x00\x00\x00\x03\x63\x6f\x6d\x2e\x61\x6c\x69\x70\x61\x79\x2e\x73\x6f\x66\x61\x2e\x72\x70\x63\x2e\x63\x6f\x72\x65\x2e\x72\x65\x71\x75\x65\x73\x74\x2e\x53\x6f\x66\x61\x52\x65\x71\x75\x65\x73\x74\x00\x00\x00\x18\x73\x6f\x66\x61\x5f\x68\x65\x61\x64\x5f\x74\x61\x72\x67\x65\x74\x5f\x73\x65\x72\x76\x69\x63\x65\x00\x00\x00\x3b\x63\x6f\x6d\x2e\x61\x6c\x69\x70\x61\x79\x2e\x72\x70\x63\x2e\x63\x6f\x6d\x6d\x6f\x6e\x2e\x73\x65\x72\x76\x69\x63\x65\x2e\x66\x61\x63\x61\x64\x65\x2e\x70\x62\x2e\x53\x61\x6d\x70\x6c\x65\x53\x65\x72\x76\x69\x63\x65\x50\x62\x3a\x31\x2e\x30\x00\x00\x00\x1b\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x73\x6f\x66\x61\x52\x70\x63\x49\x64\x00\x00\x00\x01\x30\x00\x00\x00\x1f\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x7a\x70\x72\x6f\x78\x79\x54\x69\x6d\x65\x6f\x75\x74\x00\x00\x00\x03\x31\x30\x30\x00\x00\x00\x1d\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x73\x6f\x66\x61\x54\x72\x61\x63\x65\x49\x64\x00\x00\x00\x1e\x30\x62\x61\x36\x31\x36\x61\x31\x31\x35\x32\x33\x32\x35\x31\x38\x31\x39\x31\x31\x34\x31\x30\x30\x32\x31\x38\x37\x33\x38\x00\x00\x00\x1f\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x73\x6f\x66\x61\x43\x61\x6c\x6c\x65\x72\x49\x64\x63\x00\x00\x00\x03\x64\x65\x76\x00\x00\x00\x1e\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x73\x6f\x66\x61\x43\x61\x6c\x6c\x65\x72\x49\x70\x00\x00\x00\x0d\x31\x31\x2e\x31\x36\x36\x2e\x32\x32\x2e\x31\x36\x31\x00\x00\x00\x1e\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x73\x6f\x66\x61\x50\x65\x6e\x41\x74\x74\x72\x73\x00\x00\x00\x00\x00\x00\x00\x1b\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x7a\x70\x72\x6f\x78\x79\x55\x49\x44\x00\x00\x00\x00\x00\x00\x00\x20\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x73\x6f\x66\x61\x43\x61\x6c\x6c\x65\x72\x5a\x6f\x6e\x65\x00\x00\x00\x05\x47\x5a\x30\x30\x42\x00\x00\x00\x14\x73\x6f\x66\x61\x5f\x68\x65\x61\x64\x5f\x74\x61\x72\x67\x65\x74\x5f\x61\x70\x70\x00\x00\x00\x04\x62\x61\x72\x31\x00\x00\x00\x07\x73\x65\x72\x76\x69\x63\x65\x00\x00\x00\x3b\x63\x6f\x6d\x2e\x61\x6c\x69\x70\x61\x79\x2e\x72\x70\x63\x2e\x63\x6f\x6d\x6d\x6f\x6e\x2e\x73\x65\x72\x76\x69\x63\x65\x2e\x66\x61\x63\x61\x64\x65\x2e\x70\x62\x2e\x53\x61\x6d\x70\x6c\x65\x53\x65\x72\x76\x69\x63\x65\x50\x62\x3a\x31\x2e\x30\x00\x00\x00\x19\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x45\x6c\x61\x73\x74\x69\x63\x00\x00\x00\x01\x46\x00\x00\x00\x1d\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x73\x79\x73\x50\x65\x6e\x41\x74\x74\x72\x73\x00\x00\x00\x00\x00\x00\x00\x22\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x7a\x70\x72\x6f\x78\x79\x54\x61\x72\x67\x65\x74\x5a\x6f\x6e\x65\x00\x00\x00\x00\x00\x00\x00\x1f\x72\x70\x63\x5f\x74\x72\x61\x63\x65\x5f\x63\x6f\x6e\x74\x65\x78\x74\x2e\x73\x6f\x66\x61\x43\x61\x6c\x6c\x65\x72\x41\x70\x70\x00\x00\x00\x03\x66\x6f\x6f\x00\x00\x00\x15\x73\x6f\x66\x61\x5f\x68\x65\x61\x64\x5f\x6d\x65\x74\x68\x6f\x64\x5f\x6e\x61\x6d\x65\x00\x00\x00\x05\x68\x65\x6c\x6c\x6f\x0a\x01\x61'
        p = BoltRequest.from_stream(bs)
        print(p.header)
        re = SampleServicePbRequest_pb2.SampleServicePbRequest()
        re.ParseFromString(p.content)
        print(re)
        self.assertEqual(re.name, "a")

    def test_heartbeat(self):
        pkg = HeartbeatRequest.new_request()
        print(pkg)
        print(pkg.to_stream())
        print(pkg.header)
        self.assertEqual(pkg.class_len, 0)
        self.assertEqual(pkg.header_len, 0)
        self.assertEqual(pkg.content_len, 0)
        self.assertEqual(pkg.cmdcode, CMDCODE.HEARTBEAT)

        resp = HeartbeatResponse.response_to(pkg.request_id)
        print(resp)
        print(resp.to_stream())
        self.assertEqual(resp.class_len, 0)
        self.assertEqual(resp.header_len, 0)
        self.assertEqual(resp.content_len, 0)
        self.assertEqual(resp.cmdcode, CMDCODE.HEARTBEAT)
        self.assertEqual(resp.respstatus, RESPSTATUS.SUCCESS)
        self.assertEqual(pkg.request_id, resp.request_id)


if __name__ == '__main__':
    unittest.main()

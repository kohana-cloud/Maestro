# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: unary.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bunary.proto\x12\x05unary\"\xf9\x01\n\rStartHoneypot\x12\x0e\n\x06hpType\x18\x01 \x01(\r\x12\x0f\n\x07ownerId\x18\x02 \x01(\r\x12\x17\n\x0fstartAfterBuild\x18\x03 \x01(\x08\x12\x10\n\x08targetIp\x18\x04 \x01(\r\x12\x14\n\x0ctargetSubnet\x18\x05 \x01(\r\x12\x43\n\x12resourceAllocation\x18\x06 \x01(\x0e\x32\'.unary.StartHoneypot.ResourceAllocation\"A\n\x12ResourceAllocation\x12\t\n\x05micro\x10\x00\x12\t\n\x05small\x10\x01\x12\n\n\x06medium\x10\x02\x12\t\n\x05large\x10\x03\";\n\x15StartHoneypotResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x11\n\terrorCode\x18\x02 \x01(\r2R\n\x05Unary\x12I\n\x11GetServerResponse\x12\x14.unary.StartHoneypot\x1a\x1c.unary.StartHoneypotResponse\"\x00\x62\x06proto3')



_STARTHONEYPOT = DESCRIPTOR.message_types_by_name['StartHoneypot']
_STARTHONEYPOTRESPONSE = DESCRIPTOR.message_types_by_name['StartHoneypotResponse']
_STARTHONEYPOT_RESOURCEALLOCATION = _STARTHONEYPOT.enum_types_by_name['ResourceAllocation']
StartHoneypot = _reflection.GeneratedProtocolMessageType('StartHoneypot', (_message.Message,), {
  'DESCRIPTOR' : _STARTHONEYPOT,
  '__module__' : 'unary_pb2'
  # @@protoc_insertion_point(class_scope:unary.StartHoneypot)
  })
_sym_db.RegisterMessage(StartHoneypot)

StartHoneypotResponse = _reflection.GeneratedProtocolMessageType('StartHoneypotResponse', (_message.Message,), {
  'DESCRIPTOR' : _STARTHONEYPOTRESPONSE,
  '__module__' : 'unary_pb2'
  # @@protoc_insertion_point(class_scope:unary.StartHoneypotResponse)
  })
_sym_db.RegisterMessage(StartHoneypotResponse)

_UNARY = DESCRIPTOR.services_by_name['Unary']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STARTHONEYPOT._serialized_start=23
  _STARTHONEYPOT._serialized_end=272
  _STARTHONEYPOT_RESOURCEALLOCATION._serialized_start=207
  _STARTHONEYPOT_RESOURCEALLOCATION._serialized_end=272
  _STARTHONEYPOTRESPONSE._serialized_start=274
  _STARTHONEYPOTRESPONSE._serialized_end=333
  _UNARY._serialized_start=335
  _UNARY._serialized_end=417
# @@protoc_insertion_point(module_scope)

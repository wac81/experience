# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hello.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='hello.proto',
  package='hello',
  syntax='proto3',
  serialized_pb=_b('\n\x0bhello.proto\x12\x05hello\"\x1c\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1d\n\nHelloReply\x12\x0f\n\x07message\x18\x01 \x01(\t\"v\n\x0eHelloReply_map\x12\x34\n\x08\x64ict_map\x18\x01 \x03(\x0b\x32\".hello.HelloReply_map.DictMapEntry\x1a.\n\x0c\x44ictMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32\xb5\x01\n\x07Greeter\x12\x34\n\x08SayHello\x12\x13.hello.HelloRequest\x1a\x11.hello.HelloReply\"\x00\x12\x37\n\x0bWacSayHello\x12\x13.hello.HelloRequest\x1a\x11.hello.HelloReply\"\x00\x12;\n\x0bMapSayHello\x12\x13.hello.HelloRequest\x1a\x15.hello.HelloReply_map\"\x00\x62\x06proto3')
)




_HELLOREQUEST = _descriptor.Descriptor(
  name='HelloRequest',
  full_name='hello.HelloRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='hello.HelloRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=50,
)


_HELLOREPLY = _descriptor.Descriptor(
  name='HelloReply',
  full_name='hello.HelloReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='hello.HelloReply.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=52,
  serialized_end=81,
)


_HELLOREPLY_MAP_DICTMAPENTRY = _descriptor.Descriptor(
  name='DictMapEntry',
  full_name='hello.HelloReply_map.DictMapEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='hello.HelloReply_map.DictMapEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='hello.HelloReply_map.DictMapEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=155,
  serialized_end=201,
)

_HELLOREPLY_MAP = _descriptor.Descriptor(
  name='HelloReply_map',
  full_name='hello.HelloReply_map',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dict_map', full_name='hello.HelloReply_map.dict_map', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_HELLOREPLY_MAP_DICTMAPENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=201,
)

_HELLOREPLY_MAP_DICTMAPENTRY.containing_type = _HELLOREPLY_MAP
_HELLOREPLY_MAP.fields_by_name['dict_map'].message_type = _HELLOREPLY_MAP_DICTMAPENTRY
DESCRIPTOR.message_types_by_name['HelloRequest'] = _HELLOREQUEST
DESCRIPTOR.message_types_by_name['HelloReply'] = _HELLOREPLY
DESCRIPTOR.message_types_by_name['HelloReply_map'] = _HELLOREPLY_MAP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HelloRequest = _reflection.GeneratedProtocolMessageType('HelloRequest', (_message.Message,), dict(
  DESCRIPTOR = _HELLOREQUEST,
  __module__ = 'hello_pb2'
  # @@protoc_insertion_point(class_scope:hello.HelloRequest)
  ))
_sym_db.RegisterMessage(HelloRequest)

HelloReply = _reflection.GeneratedProtocolMessageType('HelloReply', (_message.Message,), dict(
  DESCRIPTOR = _HELLOREPLY,
  __module__ = 'hello_pb2'
  # @@protoc_insertion_point(class_scope:hello.HelloReply)
  ))
_sym_db.RegisterMessage(HelloReply)

HelloReply_map = _reflection.GeneratedProtocolMessageType('HelloReply_map', (_message.Message,), dict(

  DictMapEntry = _reflection.GeneratedProtocolMessageType('DictMapEntry', (_message.Message,), dict(
    DESCRIPTOR = _HELLOREPLY_MAP_DICTMAPENTRY,
    __module__ = 'hello_pb2'
    # @@protoc_insertion_point(class_scope:hello.HelloReply_map.DictMapEntry)
    ))
  ,
  DESCRIPTOR = _HELLOREPLY_MAP,
  __module__ = 'hello_pb2'
  # @@protoc_insertion_point(class_scope:hello.HelloReply_map)
  ))
_sym_db.RegisterMessage(HelloReply_map)
_sym_db.RegisterMessage(HelloReply_map.DictMapEntry)


_HELLOREPLY_MAP_DICTMAPENTRY.has_options = True
_HELLOREPLY_MAP_DICTMAPENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))

_GREETER = _descriptor.ServiceDescriptor(
  name='Greeter',
  full_name='hello.Greeter',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=204,
  serialized_end=385,
  methods=[
  _descriptor.MethodDescriptor(
    name='SayHello',
    full_name='hello.Greeter.SayHello',
    index=0,
    containing_service=None,
    input_type=_HELLOREQUEST,
    output_type=_HELLOREPLY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='WacSayHello',
    full_name='hello.Greeter.WacSayHello',
    index=1,
    containing_service=None,
    input_type=_HELLOREQUEST,
    output_type=_HELLOREPLY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='MapSayHello',
    full_name='hello.Greeter.MapSayHello',
    index=2,
    containing_service=None,
    input_type=_HELLOREQUEST,
    output_type=_HELLOREPLY_MAP,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_GREETER)

DESCRIPTOR.services_by_name['Greeter'] = _GREETER

# @@protoc_insertion_point(module_scope)

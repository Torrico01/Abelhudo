// Auto-generated. Do not edit!

// (in-package abelhudo_pkg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Encoder_msg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.estado = null;
    }
    else {
      if (initObj.hasOwnProperty('estado')) {
        this.estado = initObj.estado
      }
      else {
        this.estado = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Encoder_msg
    // Serialize message field [estado]
    bufferOffset = _serializer.uint16(obj.estado, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Encoder_msg
    let len;
    let data = new Encoder_msg(null);
    // Deserialize message field [estado]
    data.estado = _deserializer.uint16(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 2;
  }

  static datatype() {
    // Returns string type for a message object
    return 'abelhudo_pkg/Encoder_msg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e2deebe8d363b67fc8693d7c1c1dea0f';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint16 estado
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Encoder_msg(null);
    if (msg.estado !== undefined) {
      resolved.estado = msg.estado;
    }
    else {
      resolved.estado = 0
    }

    return resolved;
    }
};

module.exports = Encoder_msg;

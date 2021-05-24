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

class Motor_msg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.pwm = null;
      this.dir = null;
      this.motor = null;
    }
    else {
      if (initObj.hasOwnProperty('pwm')) {
        this.pwm = initObj.pwm
      }
      else {
        this.pwm = 0;
      }
      if (initObj.hasOwnProperty('dir')) {
        this.dir = initObj.dir
      }
      else {
        this.dir = 0;
      }
      if (initObj.hasOwnProperty('motor')) {
        this.motor = initObj.motor
      }
      else {
        this.motor = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Motor_msg
    // Serialize message field [pwm]
    bufferOffset = _serializer.uint16(obj.pwm, buffer, bufferOffset);
    // Serialize message field [dir]
    bufferOffset = _serializer.int16(obj.dir, buffer, bufferOffset);
    // Serialize message field [motor]
    bufferOffset = _serializer.uint16(obj.motor, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Motor_msg
    let len;
    let data = new Motor_msg(null);
    // Deserialize message field [pwm]
    data.pwm = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [dir]
    data.dir = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [motor]
    data.motor = _deserializer.uint16(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 6;
  }

  static datatype() {
    // Returns string type for a message object
    return 'abelhudo_pkg/Motor_msg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e2b198c4bf4a0862124ad2db607e83d5';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint16 pwm
    int16 dir
    uint16 motor
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Motor_msg(null);
    if (msg.pwm !== undefined) {
      resolved.pwm = msg.pwm;
    }
    else {
      resolved.pwm = 0
    }

    if (msg.dir !== undefined) {
      resolved.dir = msg.dir;
    }
    else {
      resolved.dir = 0
    }

    if (msg.motor !== undefined) {
      resolved.motor = msg.motor;
    }
    else {
      resolved.motor = 0
    }

    return resolved;
    }
};

module.exports = Motor_msg;

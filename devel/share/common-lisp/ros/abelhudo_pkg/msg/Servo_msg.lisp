; Auto-generated. Do not edit!


(cl:in-package abelhudo_pkg-msg)


;//! \htmlinclude Servo_msg.msg.html

(cl:defclass <Servo_msg> (roslisp-msg-protocol:ros-message)
  ((angle
    :reader angle
    :initarg :angle
    :type cl:fixnum
    :initform 0))
)

(cl:defclass Servo_msg (<Servo_msg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Servo_msg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Servo_msg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name abelhudo_pkg-msg:<Servo_msg> is deprecated: use abelhudo_pkg-msg:Servo_msg instead.")))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <Servo_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader abelhudo_pkg-msg:angle-val is deprecated.  Use abelhudo_pkg-msg:angle instead.")
  (angle m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Servo_msg>) ostream)
  "Serializes a message object of type '<Servo_msg>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'angle)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'angle)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Servo_msg>) istream)
  "Deserializes a message object of type '<Servo_msg>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'angle)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'angle)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Servo_msg>)))
  "Returns string type for a message object of type '<Servo_msg>"
  "abelhudo_pkg/Servo_msg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Servo_msg)))
  "Returns string type for a message object of type 'Servo_msg"
  "abelhudo_pkg/Servo_msg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Servo_msg>)))
  "Returns md5sum for a message object of type '<Servo_msg>"
  "ffcccce422d555eeedf1005a7637b109")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Servo_msg)))
  "Returns md5sum for a message object of type 'Servo_msg"
  "ffcccce422d555eeedf1005a7637b109")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Servo_msg>)))
  "Returns full string definition for message of type '<Servo_msg>"
  (cl:format cl:nil "uint16 angle~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Servo_msg)))
  "Returns full string definition for message of type 'Servo_msg"
  (cl:format cl:nil "uint16 angle~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Servo_msg>))
  (cl:+ 0
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Servo_msg>))
  "Converts a ROS message object to a list"
  (cl:list 'Servo_msg
    (cl:cons ':angle (angle msg))
))

; Auto-generated. Do not edit!


(cl:in-package abelhudo_pkg-msg)


;//! \htmlinclude Encoder_msg.msg.html

(cl:defclass <Encoder_msg> (roslisp-msg-protocol:ros-message)
  ((estado
    :reader estado
    :initarg :estado
    :type cl:fixnum
    :initform 0))
)

(cl:defclass Encoder_msg (<Encoder_msg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Encoder_msg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Encoder_msg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name abelhudo_pkg-msg:<Encoder_msg> is deprecated: use abelhudo_pkg-msg:Encoder_msg instead.")))

(cl:ensure-generic-function 'estado-val :lambda-list '(m))
(cl:defmethod estado-val ((m <Encoder_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader abelhudo_pkg-msg:estado-val is deprecated.  Use abelhudo_pkg-msg:estado instead.")
  (estado m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Encoder_msg>) ostream)
  "Serializes a message object of type '<Encoder_msg>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'estado)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'estado)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Encoder_msg>) istream)
  "Deserializes a message object of type '<Encoder_msg>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'estado)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'estado)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Encoder_msg>)))
  "Returns string type for a message object of type '<Encoder_msg>"
  "abelhudo_pkg/Encoder_msg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Encoder_msg)))
  "Returns string type for a message object of type 'Encoder_msg"
  "abelhudo_pkg/Encoder_msg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Encoder_msg>)))
  "Returns md5sum for a message object of type '<Encoder_msg>"
  "e2deebe8d363b67fc8693d7c1c1dea0f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Encoder_msg)))
  "Returns md5sum for a message object of type 'Encoder_msg"
  "e2deebe8d363b67fc8693d7c1c1dea0f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Encoder_msg>)))
  "Returns full string definition for message of type '<Encoder_msg>"
  (cl:format cl:nil "uint16 estado~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Encoder_msg)))
  "Returns full string definition for message of type 'Encoder_msg"
  (cl:format cl:nil "uint16 estado~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Encoder_msg>))
  (cl:+ 0
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Encoder_msg>))
  "Converts a ROS message object to a list"
  (cl:list 'Encoder_msg
    (cl:cons ':estado (estado msg))
))

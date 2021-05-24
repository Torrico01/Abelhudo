; Auto-generated. Do not edit!


(cl:in-package abelhudo_pkg-msg)


;//! \htmlinclude Motor_msg.msg.html

(cl:defclass <Motor_msg> (roslisp-msg-protocol:ros-message)
  ((pwm
    :reader pwm
    :initarg :pwm
    :type cl:fixnum
    :initform 0)
   (dir
    :reader dir
    :initarg :dir
    :type cl:fixnum
    :initform 0)
   (motor
    :reader motor
    :initarg :motor
    :type cl:fixnum
    :initform 0))
)

(cl:defclass Motor_msg (<Motor_msg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Motor_msg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Motor_msg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name abelhudo_pkg-msg:<Motor_msg> is deprecated: use abelhudo_pkg-msg:Motor_msg instead.")))

(cl:ensure-generic-function 'pwm-val :lambda-list '(m))
(cl:defmethod pwm-val ((m <Motor_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader abelhudo_pkg-msg:pwm-val is deprecated.  Use abelhudo_pkg-msg:pwm instead.")
  (pwm m))

(cl:ensure-generic-function 'dir-val :lambda-list '(m))
(cl:defmethod dir-val ((m <Motor_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader abelhudo_pkg-msg:dir-val is deprecated.  Use abelhudo_pkg-msg:dir instead.")
  (dir m))

(cl:ensure-generic-function 'motor-val :lambda-list '(m))
(cl:defmethod motor-val ((m <Motor_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader abelhudo_pkg-msg:motor-val is deprecated.  Use abelhudo_pkg-msg:motor instead.")
  (motor m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Motor_msg>) ostream)
  "Serializes a message object of type '<Motor_msg>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pwm)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'pwm)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'dir)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'motor)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'motor)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Motor_msg>) istream)
  "Deserializes a message object of type '<Motor_msg>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pwm)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'pwm)) (cl:read-byte istream))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'dir) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'motor)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'motor)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Motor_msg>)))
  "Returns string type for a message object of type '<Motor_msg>"
  "abelhudo_pkg/Motor_msg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Motor_msg)))
  "Returns string type for a message object of type 'Motor_msg"
  "abelhudo_pkg/Motor_msg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Motor_msg>)))
  "Returns md5sum for a message object of type '<Motor_msg>"
  "e2b198c4bf4a0862124ad2db607e83d5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Motor_msg)))
  "Returns md5sum for a message object of type 'Motor_msg"
  "e2b198c4bf4a0862124ad2db607e83d5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Motor_msg>)))
  "Returns full string definition for message of type '<Motor_msg>"
  (cl:format cl:nil "uint16 pwm~%int16 dir~%uint16 motor~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Motor_msg)))
  "Returns full string definition for message of type 'Motor_msg"
  (cl:format cl:nil "uint16 pwm~%int16 dir~%uint16 motor~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Motor_msg>))
  (cl:+ 0
     2
     2
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Motor_msg>))
  "Converts a ROS message object to a list"
  (cl:list 'Motor_msg
    (cl:cons ':pwm (pwm msg))
    (cl:cons ':dir (dir msg))
    (cl:cons ':motor (motor msg))
))

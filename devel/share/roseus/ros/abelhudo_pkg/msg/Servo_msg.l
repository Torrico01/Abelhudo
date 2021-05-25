;; Auto-generated. Do not edit!


(when (boundp 'abelhudo_pkg::Servo_msg)
  (if (not (find-package "ABELHUDO_PKG"))
    (make-package "ABELHUDO_PKG"))
  (shadow 'Servo_msg (find-package "ABELHUDO_PKG")))
(unless (find-package "ABELHUDO_PKG::SERVO_MSG")
  (make-package "ABELHUDO_PKG::SERVO_MSG"))

(in-package "ROS")
;;//! \htmlinclude Servo_msg.msg.html


(defclass abelhudo_pkg::Servo_msg
  :super ros::object
  :slots (_angle ))

(defmethod abelhudo_pkg::Servo_msg
  (:init
   (&key
    ((:angle __angle) 0)
    )
   (send-super :init)
   (setq _angle (round __angle))
   self)
  (:angle
   (&optional __angle)
   (if __angle (setq _angle __angle)) _angle)
  (:serialization-length
   ()
   (+
    ;; uint16 _angle
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint16 _angle
       (write-word _angle s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint16 _angle
     (setq _angle (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get abelhudo_pkg::Servo_msg :md5sum-) "ffcccce422d555eeedf1005a7637b109")
(setf (get abelhudo_pkg::Servo_msg :datatype-) "abelhudo_pkg/Servo_msg")
(setf (get abelhudo_pkg::Servo_msg :definition-)
      "uint16 angle
")



(provide :abelhudo_pkg/Servo_msg "ffcccce422d555eeedf1005a7637b109")



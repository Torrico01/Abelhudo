;; Auto-generated. Do not edit!


(when (boundp 'abelhudo_pkg::Motor_msg)
  (if (not (find-package "ABELHUDO_PKG"))
    (make-package "ABELHUDO_PKG"))
  (shadow 'Motor_msg (find-package "ABELHUDO_PKG")))
(unless (find-package "ABELHUDO_PKG::MOTOR_MSG")
  (make-package "ABELHUDO_PKG::MOTOR_MSG"))

(in-package "ROS")
;;//! \htmlinclude Motor_msg.msg.html


(defclass abelhudo_pkg::Motor_msg
  :super ros::object
  :slots (_pwm _dir _motor ))

(defmethod abelhudo_pkg::Motor_msg
  (:init
   (&key
    ((:pwm __pwm) 0)
    ((:dir __dir) 0)
    ((:motor __motor) 0)
    )
   (send-super :init)
   (setq _pwm (round __pwm))
   (setq _dir (round __dir))
   (setq _motor (round __motor))
   self)
  (:pwm
   (&optional __pwm)
   (if __pwm (setq _pwm __pwm)) _pwm)
  (:dir
   (&optional __dir)
   (if __dir (setq _dir __dir)) _dir)
  (:motor
   (&optional __motor)
   (if __motor (setq _motor __motor)) _motor)
  (:serialization-length
   ()
   (+
    ;; uint16 _pwm
    2
    ;; int16 _dir
    2
    ;; uint16 _motor
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint16 _pwm
       (write-word _pwm s)
     ;; int16 _dir
       (write-word _dir s)
     ;; uint16 _motor
       (write-word _motor s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint16 _pwm
     (setq _pwm (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _dir
     (setq _dir (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint16 _motor
     (setq _motor (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get abelhudo_pkg::Motor_msg :md5sum-) "e2b198c4bf4a0862124ad2db607e83d5")
(setf (get abelhudo_pkg::Motor_msg :datatype-) "abelhudo_pkg/Motor_msg")
(setf (get abelhudo_pkg::Motor_msg :definition-)
      "uint16 pwm
int16 dir
uint16 motor
")



(provide :abelhudo_pkg/Motor_msg "e2b198c4bf4a0862124ad2db607e83d5")



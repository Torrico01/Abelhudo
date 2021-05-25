;; Auto-generated. Do not edit!


(when (boundp 'abelhudo_pkg::Encoder_msg)
  (if (not (find-package "ABELHUDO_PKG"))
    (make-package "ABELHUDO_PKG"))
  (shadow 'Encoder_msg (find-package "ABELHUDO_PKG")))
(unless (find-package "ABELHUDO_PKG::ENCODER_MSG")
  (make-package "ABELHUDO_PKG::ENCODER_MSG"))

(in-package "ROS")
;;//! \htmlinclude Encoder_msg.msg.html


(defclass abelhudo_pkg::Encoder_msg
  :super ros::object
  :slots (_estado ))

(defmethod abelhudo_pkg::Encoder_msg
  (:init
   (&key
    ((:estado __estado) 0)
    )
   (send-super :init)
   (setq _estado (round __estado))
   self)
  (:estado
   (&optional __estado)
   (if __estado (setq _estado __estado)) _estado)
  (:serialization-length
   ()
   (+
    ;; uint16 _estado
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint16 _estado
       (write-word _estado s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint16 _estado
     (setq _estado (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get abelhudo_pkg::Encoder_msg :md5sum-) "e2deebe8d363b67fc8693d7c1c1dea0f")
(setf (get abelhudo_pkg::Encoder_msg :datatype-) "abelhudo_pkg/Encoder_msg")
(setf (get abelhudo_pkg::Encoder_msg :definition-)
      "uint16 estado
")



(provide :abelhudo_pkg/Encoder_msg "e2deebe8d363b67fc8693d7c1c1dea0f")



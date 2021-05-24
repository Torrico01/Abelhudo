
(cl:in-package :asdf)

(defsystem "abelhudo_pkg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Motor_msg" :depends-on ("_package_Motor_msg"))
    (:file "_package_Motor_msg" :depends-on ("_package"))
    (:file "Servo_msg" :depends-on ("_package_Servo_msg"))
    (:file "_package_Servo_msg" :depends-on ("_package"))
  ))
<?php
session_start();
session_destroy(); // Xóa phiên
header("Location: login.html"); // Quay lại màn hình đăng nhập
exit();
?>

<?php
session_start();

// Giả sử bạn có thông tin đăng nhập ở đây
$valid_username = "admin";
$valid_password = "password123"; // Thay đổi mật khẩu này cho an toàn hơn

// Lấy thông tin từ form
$username = $_POST['username'];
$password = $_POST['password'];

// Kiểm tra thông tin đăng nhập
if ($username === $valid_username && $password === $valid_password) {
    // Lưu thông tin đăng nhập vào phiên
    $_SESSION['username'] = $username;

    // Chuyển hướng đến trang chính
    header("Location: index.html");
    exit();
} else {
    // Thông báo lỗi và quay lại màn hình đăng nhập
    echo "<script>alert('Tên đăng nhập hoặc mật khẩu không đúng!'); window.location.href='login.html';</script>";
}
?>

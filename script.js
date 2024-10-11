// Hiện bảng điều khiển ngay khi tải trang
document.querySelector(".dashboard-container").style.display = "block";

function filterExercises() {
  const filterValue = document.getElementById("language").value;
  const exercises = document.querySelectorAll(".exercise");
  exercises.forEach((exercise) => {
    if (filterValue === "all" || exercise.dataset.language === filterValue) {
      exercise.style.display = "block";
    } else {
      exercise.style.display = "none";
    }
  });
}

function selectExercise(button) {
  const exerciseDiv = button.parentElement;
  const title = exerciseDiv.querySelector("h4").innerText;
  const description = exerciseDiv.querySelector("p").innerText;

  document.getElementById("exerciseTitle").innerText = title;
  document.getElementById("exerciseDescription").innerText = description;

  // Hiển thị test cases cho bài tập đã chọn
  displayTestCases(title);

  // Hiển thị phần soạn mã
  document.querySelector(".dashboard-container").style.display = "none";
  document.querySelector(".coding-container").style.display = "block";
}

function displayTestCases(title) {
  const testCasesDiv = document.getElementById("testCases");
  testCasesDiv.innerHTML = ""; // Xóa nội dung cũ

  let testCases = [];

  // Thêm test cases cho từng bài tập
  switch (title) {
    case "Bài Tập 1: Giải Phương Trình Bậc Nhất":
      testCases = ["Test Case 1: 2x + 3 = 7", "Test Case 2: 4x - 5 = 3"];
      break;
    case "Bài Tập 2: Sắp Xếp Mảng":
      testCases = ["Test Case 1: [5, 2, 9]", "Test Case 2: [1, 4, 3]"];
      break;
    case "Bài Tập 3: Tính Tổng Hai Số":
      testCases = ["Test Case 1: 3, 5", "Test Case 2: 10, 20"];
      break;
    case "Bài Tập 4: In Dãy Số Fibonacci":
      testCases = ["Test Case 1: 5", "Test Case 2: 10"];
      break;
    case "Bài Tập 5: Đảo Ngược Chuỗi":
      testCases = ["Test Case 1: 'hello'", "Test Case 2: 'world'"];
      break;
    case "Bài Tập 6: Tính Giai Thừa":
      testCases = ["Test Case 1: 5", "Test Case 2: 7"];
      break;
    case "Bài Tập 7: Tìm Kiếm Phần Tử Trong Mảng":
      testCases = ["Test Case 1: [1, 2, 3, 4], 3", "Test Case 2: [5, 6, 7], 8"];
      break;
    case "Bài Tập 8: Tính Số Nguyên Tố":
      testCases = ["Test Case 1: 7", "Test Case 2: 10"];
      break;
    case "Bài Tập 9: Sắp Xếp Một Mảng":
      testCases = ["Test Case 1: [3, 1, 2]", "Test Case 2: [9, 8, 7]"];
      break;
    case "Bài Tập 10: Tính Trung Bình Cộng":
      testCases = ["Test Case 1: [1, 2, 3]", "Test Case 2: [4, 5, 6]"];
      break;
  }

  // Hiển thị các test case với input
  testCases.forEach((testCase, index) => {
    const input = `<div><label>${testCase}:</label> <input type="text" id="testCase${index}" placeholder="Nhập giá trị" /></div>`;
    testCasesDiv.innerHTML += input;
  });
}

function backToDashboard() {
  document.querySelector(".coding-container").style.display = "none";
  document.querySelector(".dashboard-container").style.display = "block";
}

function submitFeedback() {
  const feedback = document.getElementById("feedback").value;
  alert("Phản hồi của bạn đã được gửi: " + feedback);
  document.getElementById("feedback").value = "";
}

function getHint() {
  alert(
    "Gợi ý cho bài tập này: Thử sử dụng vòng lặp và điều kiện để giải quyết bài toán."
  );
}

function runCode() {
  const code = document.getElementById("codeEditor").value;

  // Lấy giá trị từ các test case
  const testCases = [];
  const inputs = document.querySelectorAll("#testCases input");
  inputs.forEach((input) => {
    testCases.push(input.value);
  });

  // Tạo một hàm tạm thời để chạy mã
  try {
    const result = eval(code);
    alert(
      "Kết quả của mã: " + result + "\nTest Cases: " + testCases.join(", ")
    );
  } catch (error) {
    alert("Có lỗi khi chạy mã: " + error.message);
  }
}

function clearCode() {
  document.getElementById("codeEditor").value = "";
  alert("Mã đã được xóa.");
}

function submitCode() {
  const code = document.getElementById("codeEditor").value;
  alert("Bạn đã nộp bài: \n" + code);
}

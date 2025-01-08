 // Hàm sử dụng AJAX để tải nội dung Lab
      function loadLabContent(labFile) {
        // Gửi yêu cầu AJAX để tải nội dung của từng Lab
        $.ajax({
          url: labFile, // Đường dẫn tới tệp Lab (lab1.html, lab2.html, ...)
          method: "GET",
          success: function (response) {
            // Chèn nội dung của Lab vào khu vực #lab-content
            $("#lab-content").html(response);

            // Kiểm tra nếu labFile là lab6.html thì thêm thẻ link để tải CSS
            if (labFile === "lab6.html") {
              $("head").append(
                '<link rel="stylesheet" type="text/css" href="lab6.css">'
              );
              // Thiết lập lại các sự kiện cần thiết cho lab6.html
              setupLab6Events();
            }
            // Kiểm tra nếu labFile là lab3.html thì thêm thẻ link để tải CSS
            if (labFile === "lab3.html") {
              $("head").append(
                '<link rel="stylesheet" type="text/css" href="lab3.css">'
              );
            }
          },
          error: function () {
            // Xử lý lỗi nếu không tải được nội dung
            $("#lab-content").html(
              "<p>Không thể tải nội dung Lab này. Vui lòng thử lại sau.</p>"
            );
          },
        });
      }

      // Hàm sử dụng AJAX để tải nội dung chi tiết
      function loadDetailContent(detailFile) {
        $.ajax({
          url: detailFile,
          method: "GET",
          success: function (response) {
            $("#lab-content").html(response);
          },
          error: function () {
            $("#lab-content").html(
              "<p>Không thể tải nội dung chi tiết. Vui lòng thử lại sau.</p>"
            );
          },
        });
      }

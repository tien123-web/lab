        let courses = JSON.parse(localStorage.getItem("courses")) || [];
        let isEditing = false;
        let editingIndex = -1;

        // Hàm hiển thị form thêm khóa học
        function showCourseForm() {
          document.getElementById("course-form").style.display = "block";
          document.getElementById("form-title").innerText = "Thêm Khóa Học";
          isEditing = false;
          clearForm();
        }

        // Hàm hủy form thêm khóa học
        function cancelCourse() {
          document.getElementById("course-form").style.display = "none";
        }

        // Hàm xóa form khi không có dữ liệu
        function clearForm() {
          document.getElementById("course-name").value = "";
          document.getElementById("course-description").value = "";
          document.getElementById("course-instructor").value = "Nguyễn Văn A";
        }

        // Hàm lưu khóa học
        function saveCourse() {
          const name = document.getElementById("course-name").value;
          const description =
            document.getElementById("course-description").value;
          const instructor = document.getElementById("course-instructor").value;

          if (name.trim() === "") {
            alert("Tên khóa học không được để trống!");
            return;
          }

          if (isEditing) {
            courses[editingIndex] = {
              name,
              description,
              instructor,
              createdAt: courses[editingIndex].createdAt,
            };
          } else {
            courses.push({
              name,
              description,
              instructor,
              createdAt: new Date().toLocaleString(),
            });
          }
          localStorage.setItem("courses", JSON.stringify(courses));
          renderCourseList();
          cancelCourse();
        }

        // Hàm render danh sách khóa học
        function renderCourseList() {
          const courseList = document.getElementById("course-list");
          courseList.innerHTML = "";
          courses.forEach((course, index) => {
            const row = document.createElement("tr");
            row.innerHTML = `
              <td>${index + 1}</td>
              <td>${course.name}</td>
              <td>${course.instructor}</td>
              <td>${course.createdAt}</td>
              <td>
                <button onclick="editCourse(${index})">Chỉnh sửa</button>
                <button onclick="deleteCourse(${index})">Xóa</button>
              </td>
            `;
            courseList.appendChild(row);
          });
        }

        // Hàm chỉnh sửa khóa học
        function editCourse(index) {
          const course = courses[index];
          document.getElementById("course-name").value = course.name;
          document.getElementById("course-description").value =
            course.description;
          document.getElementById("course-instructor").value =
            course.instructor;
          document.getElementById("form-title").innerText =
            "Chỉnh sửa Khóa Học";
          document.getElementById("course-form").style.display = "block";
          isEditing = true;
          editingIndex = index;
        }

        // Hàm xóa khóa học
        function deleteCourse(index) {
          if (confirm("Bạn chắc chắn muốn xóa khóa học này?")) {
            courses.splice(index, 1);
            localStorage.setItem("courses", JSON.stringify(courses));
            renderCourseList();
          }
        }

        // Hàm tìm kiếm khóa học
        function searchCourse() {
          const searchTerm = document
            .getElementById("search")
            .value.toLowerCase();
          const filteredCourses = courses.filter(
            (course) =>
              course.name.toLowerCase().includes(searchTerm) ||
              course.instructor.toLowerCase().includes(searchTerm)
          );
          renderFilteredCourses(filteredCourses);
        }

        // Hàm render danh sách khóa học sau khi tìm kiếm
        function renderFilteredCourses(filteredCourses) {
          const courseList = document.getElementById("course-list");
          courseList.innerHTML = "";
          filteredCourses.forEach((course, index) => {
            const row = document.createElement("tr");
            row.innerHTML = `
              <td>${index + 1}</td>
              <td>${course.name}</td>
              <td>${course.instructor}</td>
              <td>${course.createdAt}</td>
              <td>
                <button onclick="editCourse(${index})">Chỉnh sửa</button>
                <button onclick="deleteCourse(${index})">Xóa</button>
              </td>
            `;
            courseList.appendChild(row);
          });
        }

        // Gọi hàm render khi tải trang
        renderCourseList();

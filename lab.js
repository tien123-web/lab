let courses1 = [];
let isEditing = false;
let editingIndex = -1;

function showLab(lab, tab) {
    const labs = ["lab1", "lab2", "lab3"];
    labs.forEach((l) => {
        document.getElementById(l).style.display = l === lab ? "block" : "none";
    });

    const tabs = document.querySelectorAll(".tab");
    tabs.forEach((t) => {
        t.classList.remove("active");
    });
    tab.classList.add("active");
}

function showCourseForm(lab) {
    document.getElementById(`course-form-${lab.charAt(lab.length - 1)}`).style.display = "block";
    resetForm(lab);
}

function cancelCourse(lab) {
    document.getElementById(`course-form-${lab.charAt(lab.length - 1)}`).style.display = "none";
    resetForm(lab);
}

function resetForm(lab) {
    document.getElementById(`course-name-${lab.charAt(lab.length - 1)}`).value = "";
    document.getElementById(`course-description-${lab.charAt(lab.length - 1)}`).value = "";
    document.getElementById(`course-instructor-${lab.charAt(lab.length - 1)}`).value = "1";
    isEditing = false;
    editingIndex = -1;
}

function saveCourse(lab) {
    const name = document.getElementById(`course-name-${lab.charAt(lab.length - 1)}`).value;
    const description = document.getElementById(`course-description-${lab.charAt(lab.length - 1)}`).value;
    const instructor = document.getElementById(`course-instructor-${lab.charAt(lab.length - 1)}`).value;

    if (name.trim() === "") {
        alert("Tên khóa học không được để trống!");
        return;
    }

    if (isEditing) {
        courses1[editingIndex] = { name, description, instructor };
    } else {
        const newCourse = { name, description, instructor };
        courses1.push(newCourse);
    }

    renderCourseList();
    cancelCourse(lab);
}

function renderCourseList() {
    const courseListId = `course-list-1`;
    const courseList = document.getElementById(courseListId);
    courseList.innerHTML = "";

    courses1.forEach((course, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
        <td>${index + 1}</td>
        <td>${course.name}</td>
        <td>${course.instructor}</td>
        <td>${new Date().toLocaleString()}</td>
        <td>
            <button onclick="editCourse(${index}, 'lab1')">Chỉnh Sửa</button>
            <button onclick="deleteCourse(${index}, 'lab1')">Xóa</button>
        </td>`;
        courseList.appendChild(row);
    });
}

function editCourse(index, lab) {
    const course = courses1[index];
    document.getElementById(`course-name-${lab.charAt(lab.length - 1)}`).value = course.name;
    document.getElementById(`course-description-${lab.charAt(lab.length - 1)}`).value = course.description;
    document.getElementById(`form-title-${lab.charAt(lab.length - 1)}`).innerText = "Chỉnh Sửa Khóa Học";
    document.getElementById(`course-form-${lab.charAt(lab.length - 1)}`).style.display = "block";
    isEditing = true;
    editingIndex = index;
}

function deleteCourse(index, lab) {
    if (confirm("Bạn có chắc chắn muốn xóa khóa học này?")) {
        courses1.splice(index, 1);
        renderCourseList();
    }
}

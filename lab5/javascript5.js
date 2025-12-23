function loadContent(pageId) {
  const contents = document.getElementsByClassName("content");
  for (let i = 0; i < contents.length; i++) {
    contents[i].classList.remove("active");
  }
  document.getElementById(pageId).classList.add("active");
}

function importBadge() {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".jpg, .jpeg, .png";
  input.onchange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const imgElement = document.createElement("img");
        imgElement.src = e.target.result;
        imgElement.alt = file.name;
        document.querySelector(".certification-list").appendChild(imgElement);
      };
      reader.readAsDataURL(file);
    }
  };
  input.click();
}

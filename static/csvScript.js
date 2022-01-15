console.log("csv script connected");

const csv_form = document.querySelector(".csv-form");
const input_file = document.getElementById("csv-file");
const uploadBtn = document.getElementById("csv-btn");
const errorDiv = document.querySelector(".csv-error-message");

csv_form.addEventListener("submit", function (e) {
  e.preventDefault();
  if (!isFileSelected()) {
    errorDiv.innerText = "No file has choosen..!";
  } else {
    if (!isFileCSV()) {
      errorDiv.innerText =
        "Choosen file is not a csv file! please upload a csv file.";
    } else {
      errorDiv.innerText = "";
      const xhr = new XMLHttpRequest();
      file = input_file.files[0];
      const data = new FormData();
      console.log(file);

      data.append("file", file);

      xhr.open("post", "/predict_from_csv", true);
      xhr.onload = function () {
        console.log("form submitted");
        // if status === error
        errorDiv.innerText = JSON.parse(this.responseText);
      };
      xhr.send(data);
    }
  }
});

function isFileSelected() {
  if (input_file.value !== "") {
    return true;
  } else {
    return false;
  }
}

function isFileCSV() {
  const pos_of_dot = input_file.value.lastIndexOf(".") + 1;
  const ext = input_file.value.substring(pos_of_dot);
  if (ext === "csv") {
    return true;
  } else {
    return false;
  }
}

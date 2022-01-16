console.log("csv script connected");

const csv_form = document.querySelector(".csv-form");
const input_file = document.getElementById("csv-file");
const uploadBtn = document.getElementById("csv-btn");
const errorDiv = document.querySelector(".csv-error-message");
const loaderOutput = document.querySelector(".csv-loader");
const csvResult = document.querySelector(".csv-show-result");
const loaderText = document.querySelector(".loader-text");
const resultBox = document.querySelector(".result-csv");

csv_form.addEventListener("submit", function (e) {
  e.preventDefault();
  if (!isFileSelected()) {
    errorDiv.innerText = "No file has choosen..!";
    errorDiv.classList.add("error-style");
  } else {
    if (!isFileCSV()) {
      errorDiv.innerText =
        "Choosen file is not a csv file! please upload a csv file.";
      errorDiv.classList.add("error-style");
    } else {
      errorDiv.innerText = "";
      errorDiv.classList.remove("error-style");
      const xhr = new XMLHttpRequest();
      file = input_file.files[0];
      const data = new FormData();
      console.log(file);

      data.append("file", file);

      xhr.open("post", "/predict_from_csv", true);
      xhr.onload = function () {
        console.log("form submitted");
        outputObj = JSON.parse(this.response);
        console.log(outputObj);
        if (outputObj["status"] === "error") {
          loaderOutput.style.display = "none";
          console.log("displaying validation error");

          errorDiv.innerText = outputObj["val_error"];
          errorDiv.classList.add("error-style");
        } else {
          console.log("displaying result box");

          errorDiv.innerText = "";
          errorDiv.classList.remove("error-style");

          loaderText.innerText = "Predicting the output..";
          loaderOutput.style.display = "none";
          csvResult.style.display = "flex";
          resultBox.style.display = "flex";
        }
      };
      xhr.send(data);
      loaderOutput.style.display = "flex";
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

csvResult.addEventListener("click", function () {
  csvResult.style.display = "none";
  resultBox.style.display = "none";
});

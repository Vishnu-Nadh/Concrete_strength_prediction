console.log("js file is connected");

const result = document.querySelector(".show-result");
const form = document.getElementById("form");
// const message = document.getElementById("message");

const cement = document.getElementById("cement");
const blast_furnace_slag = document.getElementById("blast_furnace_slag");
const fly_ash = document.getElementById("fly_ash");
const water = document.getElementById("water");
const super_plasticizer = document.getElementById("super_plasticizer");
const coarse_aggregate = document.getElementById("coarse_aggregate");
const fine_aggregate = document.getElementById("fine_aggregate");
const Age = document.getElementById("Age");

const arr = [
  cement,
  blast_furnace_slag,
  fly_ash,
  water,
  super_plasticizer,
  coarse_aggregate,
  fine_aggregate,
  Age,
];

form.addEventListener("submit", (e) => {
  output = checkInputs();
  console.log(output);
  if (output === "error") {
    e.preventDefault();
  } else {
    e.preventDefault();
    const data = {
      cement: cement.value.trim(),
      blast_furnace_slag: blast_furnace_slag.value.trim(),
      fly_ash: fly_ash.value.trim(),
      water: water.value.trim(),
      super_plasticizer: super_plasticizer.value.trim(),
      coarse_aggregate: coarse_aggregate.value.trim(),
      fine_aggregate: fine_aggregate.value.trim(),
      Age: Age.value.trim(),
    };
    const xhr = new XMLHttpRequest();
    xhr.open("post", "/predict_from_values", true);
    xhr.setRequestHeader("content-type", "application/json");
    document.querySelector(".loader").style.display = "flex";

    xhr.onload = function () {
      console.log("form has submitted");
      console.log(this.responseText);
      result.style.display = "flex";
      document.getElementById("text_box").innerText = JSON.parse(
        this.responseText
      );
      document.querySelector(".loader").style.display = "none";

      //   document.getElementById("output").style.display = "flex";
    };
    xhr.send(JSON.stringify(data));
  }
});

result.addEventListener("click", function () {
  result.style.display = "none";
});

function checkInputs() {
  // get all the values
  const cementValue = cement.value.trim();
  const blast_furnace_slagValue = blast_furnace_slag.value.trim();
  const fly_ashValue = fly_ash.value.trim();
  const waterValue = water.value.trim();
  const super_plasticizerValue = super_plasticizer.value.trim();
  const coarse_aggregateValue = coarse_aggregate.value.trim();
  const fine_aggregateValue = fine_aggregate.value.trim();
  const AgeValue = Age.value.trim();

  let message;
  if (cementValue === "") {
    // show error
    // add error class
    msg = "This feild cannot be blank";
    setError(cement, msg);
    message = "error";
  } else {
    // add succuss class
    setSuccess(cement);
  }

  if (blast_furnace_slagValue === "") {
    // show error
    // add error class
    msg = "This feild cannot be blank";
    setError(blast_furnace_slag, msg);
    message = "error";
  } else {
    // add succuss class
    setSuccess(blast_furnace_slag);
  }

  if (fly_ashValue === "") {
    // show error
    // add error class
    msg = "This feild cannot be blank";
    setError(fly_ash, msg);
    message = "error";
  } else {
    // add succuss class
    setSuccess(fly_ash);
  }
  if (waterValue === "") {
    // show error
    // add error class
    msg = "This feild cannot be blank";
    setError(water, msg);
    message = "error";
  } else {
    // add succuss class
    setSuccess(water);
  }
  if (super_plasticizerValue === "") {
    // show error
    // add error class
    msg = "This feild cannot be blank";
    setError(super_plasticizer, msg);
    message = "error";
  } else {
    // add succuss class
    setSuccess(super_plasticizer);
  }
  if (coarse_aggregateValue === "") {
    // show error
    // add error class
    msg = "This feild cannot be blank";
    setError(coarse_aggregate, msg);
    message = "error";
  } else {
    // add succuss class
    setSuccess(coarse_aggregate);
  }

  if (fine_aggregateValue === "") {
    // show error
    // add error class
    msg = "This feild cannot be blank";
    setError(fine_aggregate, msg);
    message = "error";
  } else {
    // add succuss class
    setSuccess(fine_aggregate);
  }

  if (AgeValue === "") {
    // show error
    // add error class
    msg = "This feild cannot be blank";
    setError(Age, msg);
    message = "error";
  } else {
    // add succuss class
    setSuccess(Age);
  }

  if (message === "error") {
    return message;
  }
}

function setError(input, message) {
  const formField = input.parentElement; // .form-feild
  const error_div = formField.querySelector(".error-message");

  // add error message in small tag
  error_div.innerText = message;

  // add error class
  formField.classList.remove("success");
  formField.classList.add("error");
}

function setSuccess(input) {
  const formField = input.parentElement; // .form-feild
  formField.classList.remove("error");
  formField.classList.add("success");
}

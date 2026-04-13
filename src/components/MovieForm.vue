<template>
  <form id="movieForm" @submit.prevent="saveMovie" class="container mt-4">
    
    <div class="mb-3">
      <label class="form-label">Movie Title</label>
      <input type="text" name="title" class="form-control" />
    </div>

    <div class="mb-3">
      <label class="form-label">Description</label>
      <textarea name="description" class="form-control"></textarea>
    </div>

    <div class="mb-3">
      <label class="form-label">Poster</label>
      <input type="file" name="poster" class="form-control" />
    </div>

    <button type="submit" class="btn btn-primary">Submit</button>

  </form>
</template>
<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");

function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      csrf_token.value = data.csrf_token;
    })
    .catch((error) => {
      console.log(error);
    });
}

function saveMovie() {
  console.log("saveMovie called");

  let movieForm = document.getElementById("movieForm");
  let form_data = new FormData(movieForm);

  fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value
    }
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.log(error);
    });
}

onMounted(() => {
  getCsrfToken();
});
</script>
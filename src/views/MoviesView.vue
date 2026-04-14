<template>
  <div class="container mt-4">
    <h1 class="mb-3">Movies</h1>

    <div class="row g-4">
      <div class="col-md-6" v-for="movie in movies" :key="movie.id">
        <div class="card movie-card h-100">
          <div class="row g-0 h-100">
            <div class="col-4">
              <img :src="movie.poster" class="img-fluid rounded-start movie-poster" alt="Movie Poster" />
            </div>
            <div class="col-8">
              <div class="card-body">
                <h5 class="card-title">{{ movie.title }}</h5>
                <p class="card-text">{{ movie.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);

function fetchMovies() {
  fetch("/api/v1/movies")
    .then((response) => response.json())
    .then((data) => {
      movies.value = data.movies;
    })
    .catch((error) => {
      console.log(error);
    });
}

onMounted(() => {
  fetchMovies();
});
</script>

<style scoped>
.movie-card {
  overflow: hidden;
}

.movie-card {
  min-height: 220px;
  overflow: hidden;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card-title {
  margin-bottom: 0.75rem;
}
</style>
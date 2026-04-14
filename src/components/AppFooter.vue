<template>
  <footer class="bg-light text-center py-3 mt-5 border-top">
    <div class="container">
      <p class="mb-0">
        © {{ year }} Nathan Hansle | Movie App
      </p>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear();
</script>

<style scoped>
footer {
  width: 100%;
}
</style>
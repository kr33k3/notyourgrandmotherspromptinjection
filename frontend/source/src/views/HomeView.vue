<template>
  <div class="hello-world">
    {{ message }}
  </div>
</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue'

const message: Ref<string> = ref('Hello World')
</script>

<style scoped>
.hello-world {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 2em;
}
</style>


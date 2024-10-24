<template>
  <div class="main-area">
    <slot></slot>
  </div>
</template>
<style lang="scss">
.main-area {
  height: 100%;
  width: 100%;
  grid-column-start: 1;
  grid-column-end: 3;
  grid-row: 2;
  @media (min-width: 1000px) {
    grid-column: 2;
  }
}
</style>

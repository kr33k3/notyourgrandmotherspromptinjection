<template>
  <AlertPopups></AlertPopups>
  <LoadingOverlay></LoadingOverlay>
  <div class="main-layout">
    <!-- <NavigationDrawer :showMenu="showMenu" @toggleMenu="showMenu = !showMenu"></NavigationDrawer> -->
    <ApplicationBar
      @showSearch="isSearching = true"
      @toggleMenu="showMenu = !showMenu"
    ></ApplicationBar>
    <MainContent style="z-index: 0">
      <SearchModal
        :active="isSearching"
        @closeSearch="isSearching = false"
        @selectSearchItem="routeToSearchItem($event)"
      ></SearchModal>
      <slot></slot>
    </MainContent>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router'

import NavigationDrawer from '@/components/layouts/NavigationDrawer.vue'
import ApplicationBar from '@/components/layouts/ApplicationBar.vue'
import MainContent from '@/components/layouts/MainContent.vue'
import ApplicationFooter from '@/components/layouts/ApplicationFooter.vue'
//import LoadingOverlay from '@/components/utility/LoadingOverlay.vue'
//import AlertPopups from '@/components/utility/AlertPopups.vue'


import { ref } from 'vue'

const showMenu = ref(false)
const isSearching = ref(false)
const router = useRouter()

const routeToSearchItem = (contentId: string) => {
  isSearching.value = false
  router.push({ name: 'content', params: { contentId } })
}
</script>

<style lang="scss">
@import './layoutSizes.scss';
@import '@/css/colors.scss';
@import '@/css/base.scss';
.main-layout {
  height: 100%;
  display: grid;
  background-color: $background-color;
  width: 100%;
  grid-template-columns: ($nav-bar-size + 1.5rem) calc(100vw - ($nav-bar-size + 2.55rem)); //I dont know why 2.55 it just happens to be the correct size to get it to fill the rest of the screen.
  grid-template-rows: $header-height 1fr;
  overflow: hidden;
}

$scrollbar-color: $tertiary-background-color;
</style>

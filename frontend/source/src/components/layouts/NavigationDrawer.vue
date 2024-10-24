<template>
  <div :class="'nav-bar ' + (showMenu ? 'nav-bar-active' : '')">
    <div class="nav-bar-header" style="display: flex; justify-content: space-between">
      <ProfileAvatar
        :height="54"
        :width="54"
        :userGraphId="profileInfo?.GraphId"
        :showUsername="true"
      ></ProfileAvatar>
      <v-btn variant="icon" icon="mdi-menu-down">
        <v-icon style="color: darkslategray"></v-icon>
        <v-menu activator="parent">
          <v-list style="font-size: 0.75rem">
            <!-- <v-list-item @click=""><v-icon icon="mdi-cog"></v-icon> Settings</v-list-item> -->
            <v-list-item @click="logout()"><v-icon icon="mdi-logout"></v-icon> Log Out</v-list-item>
          </v-list>
        </v-menu>
      </v-btn>
    </div>
    <div class="nav-bar-header" style="padding-right: 0.5rem; padding-left: 0.5rem">
      <v-text-field
        style="background-color: #201c24"
        label="Search"
        prepend-inner-icon="mdi-magnify"
        v-model="searchQuery"
        hide-details
        @keydown.enter="search()"
      ></v-text-field>
    </div>
    <div class="nav-bar-items">
      <div
        :class="'nav-bar-item ' + (activeItem == navItem.title ? 'nav-bar-item-active' : '')"
        v-for="navItem in navItems"
        :key="navItem.title"
        @click="routeToLink(navItem)"
        v-ripple
      >
        <v-icon style="transform: translateY(-2.5px)" size="2rem" :icon="navItem.icon"></v-icon>
        {{ navItem.title }}
      </div>
    </div>
  </div>
  <transition name="slide">
    <div v-if="showMenu" class="nav-bar-overlay" @click="emit('toggleMenu')"></div>
  </transition>
</template>
<script setup lang="ts">
import LoginService from '@/domains/login/LoginService'

import { useRouter } from 'vue-router'
import { onMounted, type Ref, ref, type ComputedRef, computed } from 'vue'

import { type Response } from '@/types/response'
import { type UserProfileResponse } from '@/types/userProfileResponse'
import ProfileService from '@/services/api/ProfileService'
import { Permissions } from '@/stores/permissionsStore'

import ProfileAvatar from '@/components/profile/ProfileAvatar.vue'

const props = defineProps(['showMenu'])
const emit = defineEmits(['toggleMenu'])

const searchQuery: Ref<string> = ref('')

interface NavItem {
  icon: string
  title: string
  route: string
}
const activeItem: Ref<string> = ref('Explore')
const navItems: ComputedRef<NavItem[]> = computed(() => {
  let items: { icon: string; title: string; route: string }[] = [
    {
      icon: 'mdi-compass',
      title: 'Explore',
      route: '/'
    },
    {
      icon: 'mdi-bulletin-board',
      title: 'Videos',
      route: '/videos'
    },
    // {
    //   icon: 'mdi-sign-direction',
    //   title: 'Roadmap',
    //   route: '/roadmap'
    // },
    {
      icon: 'mdi-comment-quote-outline',
      title: 'Feedback',
      route: '/feedback'
    },
    // {
    //   icon: 'mdi-trophy',
    //   title: 'Training',
    //   route: '/rewards'
    // },
    {
      icon: 'mdi-account',
      title: 'Profile',
      route: '/profile'
    }
  ]

  if (Permissions.AdminTab.value) {
    items.push({
      icon: 'mdi-account-multiple',
      title: 'Administration',
      route: '/admin'
    })
  }

  return items
})

const profileInfo: Ref<UserProfileResponse> = ref(null)

const router = useRouter()

const routeToLink = (item: NavItem) => {
  activeItem.value = item.title
  router.push(item.route)
  if (props.showMenu) {
    emit('toggleMenu')
  }
}

onMounted(() => {
  ProfileService.getMyProfileInfo().then((val: Response<UserProfileResponse>) => {
    profileInfo.value = val.body
  })
})

const search = () => {
  router.push(`/search/?q=${searchQuery.value}`)
  searchQuery.value = ''
}

const logout = () => {
  LoginService.logout()
  router.push('/login')
}
</script>
<style lang="scss">
@import '@/css/colors.scss';
@import '@/css/base.scss';
@import './layoutSizes.scss';
$header-height: 6.25rem; //TODO: Create share scss to store vars
$slideTransition: all 0.2s ease-in-out;

// TODO - have nav-bar's height react to at least contain it's sub-elements
.nav-bar {
  width: $nav-bar-size;
  height: calc(100vh - 2rem);
  transform: translateX(-($nav-bar-size + 4rem));
  transition: $slideTransition;
  background-color: $secondary-background-color;
  margin: 0.75rem 1rem;
  border-radius: $border-radius;
  grid-row-start: 1;
  grid-row-end: 3;
  grid-column: 1;
  z-index: 1;
  @media (min-width: 1000px) {
    transform: translateX(0);
  }

  &-active {
    transform: translateX(0);
    z-index: 5;
  }

  &-header {
    border-bottom: 1px solid #131619;
    padding: calc(($header-height - 54px) / 2) 1.5rem;
  }

  $activeBackground: $tertiary-action-item-background; //linear-gradient(164deg, #202427, $secondary-background-color);
  &-item {
    margin: 1.25rem 0.5rem;
    padding: 1rem;
    font-weight: bold;
    font-size: 1rem;
    transition: background 1s ease;
    border-radius: $border-radius;
    &-active,
    &:hover {
      background: $activeBackground;
    }
  }
  &-overlay {
    background-color: gray;
    height: 100%;
    width: 100%;
    opacity: 0.5;
    z-index: 1;
    display: block;
    position: absolute;
    @media (min-width: 1000px) {
      display: none;
    }
  }
}

.slide-enter-active,
.slide-leave-active {
  transition: $slideTransition;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-$nav-bar-size);
  opacity: 0;
}
</style>

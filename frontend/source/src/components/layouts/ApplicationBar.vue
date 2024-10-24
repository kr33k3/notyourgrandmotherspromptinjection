<template>
  <div class="app-bar">
    <div style="display: flex; align-items: center; justify-content: space-around">
      <img
        @click="routeToLink(navItems[0])"
        class="app-bar-logo app-bar-logo-large"
        src="@/assets/BCFullLogo.png"
      />
      <img
        @click="routeToLink(navItems[0])"
        class="app-bar-logo app-bar-logo-small"
        src="@/assets/NewBCLogo.png"
      />
      <div
        v-for="item in navItems"
        @click="routeToLink(item)"
        :key="item.title"
        :class="'tab ' + (isActive(item.route) ? 'tab-active' : '')"
      >
        {{ item.title }}
      </div>
    </div>
    <div>
      <div style="display: flex; justify-content: space-between">
        <ProfileAvatar
          @click="$router.push('/profile')"
          :height="54"
          :width="54"
          :userGraphId="profileInfo?.GraphId"
          :showUsername="false"
          :clickable="true"
        />
        <v-btn variant="icon" icon="mdi-menu-down">
          <v-icon style="color: darkslategray"></v-icon>
          <v-menu activator="parent">
            <v-list style="font-size: 0.75rem">
              <!-- <v-list-item @click=""><v-icon icon="mdi-cog"></v-icon> Settings</v-list-item> -->
              <v-list-item @click="logout()"
                ><v-icon icon="mdi-logout"></v-icon> Log Out</v-list-item
              >
            </v-list>
          </v-menu>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useTheme } from 'vuetify'
import { useRoute } from 'vue-router'


// consts
const route = useRoute()


import { useRouter } from 'vue-router'
import { onMounted, type Ref, ref, type ComputedRef, computed } from 'vue'

import { type Response } from '@/types/response'
import { type UserProfileResponse } from '@/types/userProfileResponse'
import ProfileService from '@/services/api/ProfileService'
import { Permissions } from '@/stores/permissionsStore'

const searchQuery: Ref<string> = ref('')

interface NavItem {
  icon: string
  title: string
  route: string
}

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
    {
      icon: 'mdi-comment-quote-outline',
      title: 'Feedback',
      route: '/feedback'
    }
  ]

  if (Permissions.AdminTab.value) {
    items.push({
      icon: 'mdi-account-multiple',
      title: 'Administration',
      route: '/admin'
    })
  }
  if (Permissions.QuizTab.value) {
    items.push({
      icon: 'mdi-comment-quote-outline',
      title: 'Quiz Lab',
      route: '/quiz'
    })
  }

  return items
})

const profileInfo: Ref<UserProfileResponse | null> = ref(null)

const router = useRouter()

const routeToLink = (item: NavItem) => {
  router.push(item.route)
}

const isActive = (route: string) => {
  const baseRoute = router.currentRoute.value.path.split('/')[1]
  if (route == '/' && [route, 'search', 'content'].includes(baseRoute)) {
    return true
  }
  if ([route].includes('/' + baseRoute)) {
    return true
  }
  return false
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
const emit = defineEmits(['showSearch', 'toggleMenu'])
const theme = useTheme()
const toggleTheme = () => {
  theme.global.name.value = theme.global.current.value.dark
    ? 'buildCyberLightTheme'
    : 'buildCyberDarkTheme'
}
</script>
<style lang="scss">
@import '@/css/utility.scss';
@import '@/css/colors.scss';

.app-bar {
  height: 100%;
  width: 100%;
  padding: 1rem;
  grid-column-start: 1;
  grid-column-end: 3;
  grid-row: 1;
  background-color: $background-color;
  z-index: 1;
  @media (min-width: 1000px) {
    grid-column: 2;
  }
  display: flex;
  justify-content: space-between;
  &-logo {
    &-large {
      @media (max-width: 500px) {
        display: none;
      }
    }
    &-small {
      @media (min-width: 500px) {
        display: none;
      }
    }
    height: 3rem;
    margin-bottom: 0.5rem;
    margin-right: 0.5rem;
    cursor: pointer;
  }
}
.menu-button {
  display: inline-block;
  @media (min-width: 1000px) {
    display: none;
  }
}
.tab {
  padding: 0.25rem 0.5rem;
  cursor: pointer;

  &-active {
    font-weight: 500;
    color: $primary-color;
    border-radius: 0.25rem 0.25rem 0 0;
    border-bottom: 0;
  }
}
img {
  image-rendering: auto; /* Ensures smooth scaling */
}
</style>

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { VDateInput } from 'vuetify/labs/VDateInput'
import { mdi, aliases } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'
import { md2 } from 'vuetify/blueprints'

const buildCyberDarkTheme = {
  dark: true,
  colors: {
    background: '#1E1E1E',
    surface: '#1F1E28',
    primary: '#7AC8F0', //'#0a7dbc',
    passive: '#FFFFFF',
    wow: '#7AC8F0',
    //'primary-darken-1': '#05518B',
    secondary: '#63899E',
    //'secondary-darken-1': '#018786',
    error: '#f00911',
    info: '#63899E',
    success: '#4CAF50',
    warning: '#FB8C00'
  }
}

const buildCyberLightTheme = {
  dark: false,
  colors: {
    background: '#FFFFFF',
    surface: '#63899E',
    primary: '#0a7dbc',
    //'primary-darken-1': '#05518B',
    secondary: '#062555',
    //'secondary-darken-1': '#018786',
    error: '#f00911',
    info: '#63899E',
    success: '#4CAF50',
    warning: '#FB8C00'
  }
}

export default createVuetify({
  blueprint: md2,
  components: { ...components, VDateInput },
  directives,
  theme: {
    defaultTheme: 'buildCyberDarkTheme',
    themes: {
      dark: {
        dark: true
      },
      buildCyberDarkTheme,
      buildCyberLightTheme
    }
  },
  icons: {
    defaultSet: 'mdi',
    iconfont: 'mdi',
    aliases,
    sets: {
      mdi
    }
  },
  defaults: {
    VTextField: {
      variant: 'outlined'
    },
    VCard: {
      variant: 'outlined'
    },
    VTextarea: {
      variant: 'outlined'
    }
  },
  styles: {
    configFiles: 'src/css/vuetify-settings.scss'
  }
})

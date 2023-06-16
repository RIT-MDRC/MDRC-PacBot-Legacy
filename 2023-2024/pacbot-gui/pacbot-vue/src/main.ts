import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})

// Konva
import VueKonva from 'vue-konva';

const app = createApp(App)

app.use(router)
app.use(vuetify)
app.use(VueKonva)

app.mount('#app')

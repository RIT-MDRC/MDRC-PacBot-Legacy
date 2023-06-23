/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'
import VueKonva from 'vue-konva';

const app = createApp(App)

registerPlugins(app)
app.use(VueKonva);

app.mount('#app')

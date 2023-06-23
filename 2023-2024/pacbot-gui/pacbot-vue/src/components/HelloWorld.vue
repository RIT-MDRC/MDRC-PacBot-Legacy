<template>
  <v-toolbar>
    <v-toolbar-title>RIT Pacbot</v-toolbar-title>
  </v-toolbar>
  <v-row class="fill-height">
    <v-col ref="konvaContainer">
      <v-container class="text-center">
        <v-stage :config="configKonva">
          <v-layer>
            <v-circle :config="configCircle"></v-circle>
          </v-layer>
        </v-stage>
      </v-container>
    </v-col>
    <v-col>
      <div class="d-flex flex-row">
        <v-tabs
          v-model="tab"
          direction="vertical"
          color="primary"
        >
          <v-tab v-for="service in services" :value="service.name">
            <v-icon v-if="service.icon" start>
              mdi-account
            </v-icon>
            {{ service.name }}
          </v-tab>
        </v-tabs>
        <v-window v-model="tab" style="flex-grow: 1;" class="ml-2">
          <v-window-item v-for="service in services" :value="service.name">
            <div v-for="status in service.statuses" class="d-flex align-center mt-2">
              <v-chip :color="status.status" class="mr-2">
                {{ status.chip }}
                <v-tooltip
                  v-if="status.message"
                  activator="parent"
                  location="bottom"
                >{{ status.message }}</v-tooltip>
              </v-chip>
              <div>{{ status.name }}</div>
            </div>
            <v-divider class="mt-2"></v-divider>
            <v-checkbox label="Checkbox" hide-details="auto"></v-checkbox>
            <v-combobox
              hide-details="auto"
              label="Combobox"
              :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']"
            ></v-combobox>
            <v-divider class="mt-2"></v-divider>
            <div v-for="debug in service.debug" class="d-flex align-center mt-2">
              {{ debug.name }}: {{ debug.value }}
            </div>
          </v-window-item>
        </v-window>
      </div>
    </v-col>
  </v-row>
</template>

<style>
  /* h2, h3 {
    margin-bottom: 10px;
  }

  h3 {
    margin-top: 10px;
  } */
</style>

<script setup lang="ts">
  import { stat } from 'fs';
import { nextTick } from 'process';
import { onMounted } from 'vue';
import { ref, Ref, computed } from 'vue'

  let tab = ref('option-1');

  let konvaContainer: any = ref(null);

  let gridWidth = ref(100);

  onMounted(() => {
    window.addEventListener('resize', onResize);
  })

  function onResize() {
    gridWidth.value = Math.min(Math.floor(window.innerHeight * 0.8), Math.floor(window.innerWidth / 2));
  }
  
  let configKonva = computed(() => ({
    width: gridWidth.value,
    height: gridWidth.value
  }))

  let configCircle = computed(() => ({
    x: gridWidth.value/2,
    y: gridWidth.value/2,
    radius: gridWidth.value/2,
    fill: "red",
    stroke: "black",
    strokeWidth: 4
  }))

  let services = [
    {
      id: 0,
      name: 'Robomodules Client',
      status: 'success',
      chip: 'OK',
      statuses: [
        {
          name: 'Internet Connection',
          status: 'success',
          chip: 'OK'
        },
        {
          name: 'Robomodules Connection',
          status: 'warning',
          chip: 'WARNING',
          message: 'Connecting...'
        }
      ],
      options: [
        {
          name: 'Active',
          type: 'checkbox'
        }
      ],
      debug: [
        {
          name: 'Test',
          value: 123
        }
      ]
    },
    {
      id: 1,
      name: 'Particle Filter',
      status: 'error',
      chip: 'ERROR',
      icon: 'mdi-information-outline',
      statuses: [],
      options: [
        {
          name: 'Number of Particles',
          type: 'number'
        }
      ],
      debug: []
    }
  ]
</script>

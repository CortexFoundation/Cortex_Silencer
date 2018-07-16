<template>
  <div id="app">
    <b-container>
      <b-row>
        <upload/>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import Upload from './components/Upload'

export default {
  name: 'App',
  data () {
    return {
    }
  },
  components: {
    Upload,
  }
}
</script>

<style>
body {
    color: rgba(255,255,255,0.85);
    background-color: #24292e;
    background-repeat: repeat-x;
    background-position: center 0, 0 0, 0 0;

}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

img.logo {
  width: 32px;
  height: 32px;
}
</style>

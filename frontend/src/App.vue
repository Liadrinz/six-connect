<template>
  <div id="app">
    <Chessboard :x="19" :y="19" :person-color="0" @change="printBoardData"/>
  </div>
</template>

<script>
import Chessboard from '@/components/Chessboard'

export default {
  name: "App",
  components: {Chessboard},
  methods: {
    printBoardData(data) {
      console.log(data);
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

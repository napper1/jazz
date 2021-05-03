<template>
  <div id="custom-songs">
    <div class="row">
      <div class="col">
        <p>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
        name: "CustomSongs.vue",
        computed: {
            songs() {
                return this.$store.state.songs
            },
            count () {
              return this.$store.state.count
            }
        },
        data(){
            return{
              test: 0,
            }
        },
        methods: {
        },
    }
</script>

<style scoped>

</style>

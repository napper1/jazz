<template>
  <div id="spotify-tracks">
    <div class="row" v-for="song in tracks">
      <div class="col-sm-12">
        <div class="song d-flex"
             :class="getSongClass(song)"
             @mouseover="showActions(song)"
             @click="setSongSelection(song)"
        >
          <div class="song-detail">
            <div class="row">
              <div class="col-1">
                <img class="song_thumbnail" :src="song.image" alt="">
              </div>
              <div class="col-7">
                <div class="song_name">
                  <h5><strong>{{ song.title }}</strong></h5>
                  <p class="artist">
                    <span v-for="(artist, a_idx) in song.artists" :key="a_idx">{{ artist }}<span v-if="a_idx !== song.artists.length - 1">, </span></span>
                  </p>
                </div>
              </div>
              <div class="col-4">
                  <div v-if="song === selected_song">
                    <audio controls="controls" v-if="song.preview_url">
                      <source :src="song.preview_url" type="audio/mpeg">
                    </audio>
                  </div>
              </div>
            </div>
          </div>
          <div class="song-actions d-flex justify-content-center align-items-center" v-if="song === selected_song">
            <a :href="song.url" target="_blank">
              <b-icon icon="play-fill" aria-hidden="true" class="play-btn"></b-icon>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
  export default{
    props: ['tracks'],
    data(){
        return{
            selected_song: null,
            active_song: null,
        }
    },
    methods: {
      showActions: function(song){
        this.selected_song = song;
      },
      getSongClass(song){
          if (this.active_song === song){
            return 'active-song'
          }
      },
      setSongSelection(song){
          this.active_song = song;
      },


    }
  }
</script>

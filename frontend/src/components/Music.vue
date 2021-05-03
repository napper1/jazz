<template>
  <div class="music w-100 h-100 mh-100"
       v-scroll="showScroller"
       v-bind:class="{ padd_top: prev_iframe_url }">
    <div class="container-fluid w-100 h-100 mh-100">
      <div class="row h-100 mh-100">
        <div class="col-2" id="sticky-sidebar">
          <div class="sticky-top">
            <div class="nav flex-column" id="side-col">
                <div class="pt-2">
                  <h1 class="fancy-title h1 d-inline-block mb-4"><i class="fa fa-music mr-1"></i>
                    Music
                  </h1>
                </div>
                <h3 class="fancy-title">Categories</h3>
                <div class="list-group list-filters">
                  <b-button class="list-group-item list-group-item-action" :class="getAllCategoryClass()" type="button" varient="warning" @click="getAllSongs">All</b-button>
                  <b-button class="list-group-item list-group-item-action" :class="getActiveCategory(cat)" type="button" varient="primary" v-for="(cat, index) in song_categories" :key="index"
                            @click="filterSongsByCategory(cat)">
                    {{ cat.text }}
                  </b-button>
                </div>
                <h3 class="fancy-title">Spotify</h3>
                <div class="list-group list-filters">
                  <b-button class="list-group-item list-group-item-action"
                            type="button" @click="spotifyLogin()">
                    Login
                  </b-button>
                  <b-button class="list-group-item list-group-item-action"
                            :class="{'active-cat': spotify_tracks_class}"
                            type="button" @click="getSpotifyTracks()">
                    My Tracks
                  </b-button>
                </div>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="row top-header">
            <div class="col">
              <div class="row d-flex justify-content-center align-items-center h-100">
                <div class="col-3">
                  <div class="d-inline-block">
                    <mycircle v-if="filter_loading"></mycircle>
                  </div>
                </div>
                <div class="col-3">
                  <input class="form-control search_box" v-model="song_query" type="text" placeholder="Search..."
                         @keyup="lookupSong()">
                </div>
                <div class="col-6">
                  <div class="d-inline-block pull-right top-filters">
                    <button type="button" class="btn btn-secondary btn-sm" @click="backupMusic()">Backup Songs</button>
                    <button type="button" class="btn btn-success btn-sm" v-b-modal.song-modal>Add Song</button>
                    <a href="https://www.abc.net.au/triplej/listen-live/double-j-player/"
                       class="btn btn-primary btn-sm" target="_blank">Double J</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="prev_iframe" v-if="show_video_box">
            <div class="close-video">
              <a href="#" @click="closeVideo()">
                <i class="fa fa-times"></i>
              </a>
            </div>
            <youtube :video-id="videoId" @ready="ready" @playing="playing" @ended="ended" :player-vars="{autoplay: 1}"></youtube>
          </div>
          <alert :message="message" class="music-alert-box" :class="{'alert-active': show_alert_msg}"></alert>
          <div class="row songs-section">
            <div class="col">
              <h1>{{ title }}</h1>
              <customsongs></customsongs>
              <spotifytracks :tracks="spotify_tracks"></spotifytracks>
              <div class="row" v-for="(song, index) in songs" :key="index">
                <div class="col-sm-12">
                  <div class="song d-flex" :class="getSongClass(song)" @mouseover="showActions(song)" @click="setSongSelection(song)">
  <!--                  <div class="song_num">-->
  <!--                    <p class="">{{ songNumber(index) }}</p>-->
  <!--                  </div>-->
                    <div class="song-detail">
                      <div class="row">
                        <div class="col-1">
                          <a :href="song.link" v-if="song.spotify" target="_blank">
                            <img class="song_thumbnail" src="https://via.placeholder.com/60" alt="">
                          </a>
                          <img v-else class="song_thumbnail" @click="showPreview(song)" v-b-modal.song-preview-modal src="https://via.placeholder.com/60" alt="">
                        </div>
                        <div class="col-10">
                          <div class="song_name">
                            <h5><strong>{{ song.title }}</strong>
                              <b-icon v-if="song.song_category && song.song_category.title == 'Favourites'" icon="heart-fill" aria-hidden="true" class="heart-icon"></b-icon>
                              <b-badge v-else-if="song.song_category">{{ song.song_category.title }}</b-badge>
                            </h5>
                            <p class="artist">{{ song.artist.name }} </p>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="song-actions d-flex justify-content-center align-items-center">
                      <div v-if="selected_song === song" class="pull-left">
                        <mycircle v-if="loading"></mycircle>
                      </div>
                      <div class="d-flex justify-content-center align-items-center" v-if="selected_song === song">
                        <a :href="song.link" v-if="song.spotify" target="_blank">
                          <b-icon icon="play-fill" aria-hidden="true" class="play-btn"></b-icon>
                        </a>
                        <b-icon v-else icon="play-fill" aria-hidden="true" class="play-btn" @click="showPreview(song)" v-b-modal.song-preview-modal></b-icon>
                        <b-dropdown id="dropdown-dropleft" dropleft class="song-actions-dropdown pull-right">
                          <template #button-content>
                            <b-icon icon="three-dots-vertical" aria-hidden="true"></b-icon>
                          </template>
                          <b-dropdown-item v-b-modal.song-update-modal @click="editSong(song)">
                            <i class="fa fa-edit" aria-hidden="true"></i>
                            Edit
                          </b-dropdown-item>
                          <b-dropdown-item @click="onDeleteSong(song)">
                            <i class="fa fa-times" aria-hidden="true"></i>
                            Delete
                          </b-dropdown-item>
                          <b-dropdown-divider></b-dropdown-divider>
                          <b-dropdown-item @click="downloadSong(song)" class="download-song">
                            <i class="fa fa-download" aria-hidden="true"></i>
                            Download to media
                          </b-dropdown-item>
                          <b-dropdown-item v-if="song.downloaded" class="download-song" :href="song.media_link" target="_blank">
                            <i class="fa fa-download" aria-hidden="true"></i>
                            Download to device
                          </b-dropdown-item>
                        </b-dropdown>
                      </div>
                    </div>
                  </div>
                </div>
                <hr>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <AddSongModal
      v-on:refresh-songs="addSongComplete"
      :song_categories="song_categories"
    />

    <EditSongModal
      v-on:refresh-songs="addSongComplete"
      :song_categories="song_categories"
      :song="active_song"
    />

    <b-modal ref="previewSongModal"
             id="song-preview-modal"
             title="Preview"
             hide-footer>
      <iframe class="youtube_iframe" :src="iframe_url" frameborder="0" width="560" height="315" autoplay allowfullscreen></iframe>
    </b-modal>
    <b-modal ref="backupModal"
             id="backup-modal"
             title="Backup Songs"
             hide-footer>
      <p>Run this command in shell. It backs up db to Dropbox.</p>
      <pre>python manage.py dbbackup</pre>
    </b-modal>
    <div id="topbutton" class="show" @click="scrollTop()" v-bind:class="{ hide: hide_scroller }">
      <span class="scroll-back-to-top-inner"><em class="fa fa-2x fa-arrow-circle-up"></em></span>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';
import Circle from 'vue-loading-spinner/src/components/Circle'
import { RotateSquare2 } from 'vue-loading-spinner'
import { Circle2 } from 'vue-loading-spinner'
import VueYouTubeEmbed from 'vue-youtube-embed'
import datePicker from 'vue-bootstrap-datetimepicker';
import SpotifyTracks from "./SpotifyTracks";
import CustomSongs from "./CustomSongs";
import AddSongModal from "./AddSongModal";
import EditSongModal from "./EditSongModal";

export default {
  name: 'Music',
  data() {
    return {
      songs: [],
      message: '',
      loading: false,
      filter_loading: false,
      selected_song: null,
      iframe_url: "",
      prev_iframe_url: "",
      columns: [
            { label: 'Title', field: 'title' },
            { label: 'Artist', field: 'artist.name' },
      ],
      rows: window.rows,
      hide_scroller: false,
      videoId: '',
      show_video_box: false,
      date: new Date(),
      options: {
          format: 'DD/MM/YYYY',
          useCurrent: false,
      },
      song_results: [],
      song_query: "",
      song_result: "",
      quantity_group: {
        code: "quantity",
        field_type: 'number',
        selected: "",
      },
      song_categories: [],
      alert_delay_time: 1500,
      show_alert_msg: false,
      selected_category: "",
      active_song: {},
      spotify_tracks: [],
      title: "All Songs",
    };
  },
  components: {
    alert: Alert,
    mycircle: Circle,
    RotateSquare2,
    Circle2,
    datePicker,
    spotifytracks: SpotifyTracks,
    customsongs: CustomSongs,
    AddSongModal,
    EditSongModal,
  },
  methods: {
    lookupSong() {
      const path = '/songs/?q=' + this.song_query;
      axios.get(path)
        .then((response) => {
          this.songs = response.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    setSelectedSong(song) {
      this.playPreview(song);
      this.song_results = [];
    },
    submitFile(){
      const json = JSON.stringify(this.groups);
      const blob = new Blob([json], {
        type: 'application/json'
      });
      let formData = new FormData();
      formData.append('file', this.file);
      formData.append('file_second', this.file_second);
      formData.append('groups', blob);
      axios.post('/api-document/', formData, {headers: {'Content-Type': 'multipart/form-data'}})
        .then(() => {
          console.log("doc saved");
        })
        .catch((error) => {
          console.log('error in posting');
        });
    },
    getClass(child, selected){
      return {
        'selected': selected.includes(child.field_value)
      }
    },
    getAllSongs(){
        this.selected_category = 'all';
        this.title = 'All Songs';
        this.getSongs();
    },
    getSongs() {
      this.spotify_tracks = [];
      this.filter_loading = true;
      const path = '/songs/';
      axios.get(path)
        .then((res) => {
          this.songs = res.data;
          this.filter_loading = false;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.filter_loading = false;
        });
    },
    getSongCategories() {
      const path = '/song-categories/';
      axios.get(path)
          .then((res) => {
              var data = res.data;
              for (var i = 0; i < data.length; i++){
                  var category = data[i];
                  console.log(category);
                  this.song_categories.push({value: category.id, text: category.title})
              }
          })
          .catch((error) => {
              console.log(error);
          })
    },
    editSong(song) {
      // make the song available in the EditSongModal as a prop
      this.active_song = song;
    },
    removeAlert() {
      // Clear the alert box by setting a timer for a few seconds before clearing alert message.
      console.log('start timer');
      const delay = ms => new Promise(res => setTimeout(res, ms));
      delay(this.alert_delay_time).then(() => {
         console.log('finished');
         this.show_alert_msg = false;
         // this.message = "";
      });
    },
    removeSong(song_id) {
      const path = `/songs/${song_id}/`;
      axios.delete(path)
        .then(() => {
          this.getSongs();
          this.show_alert_msg = true;
          this.message = 'Song removed!';
          this.removeAlert();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getSongs();
        });
    },
    getNextSong(song_id){
      const path = `/api-get-next/${song_id}/`;
      axios.get(path)
        .then((res) => {
          this.song = res.data;
          this.videoId = this.getSongID(this.song);
        })
        .catch((error) => {
        console.log(error)
        })
    },
    onDeleteSong(song) {
      this.removeSong(song.id);
    },
    downloadSong: function(song){
      if (this.selected_song === song) this.selected_song = null;
      else this.selected_song = song;
      this.loading = true;
      axios.post('/download/' + song.id + '/')
          .then(() => {
            this.show_alert_msg = true;
            this.message = "Song downloaded to media folder!";
            this.loading = false;
            // refresh songs list
            this.getSongs();
            this.removeAlert();
          })
          .catch((error) => {
            this.show_alert_msg = true;
            this.message = "An error occurred! " + error;
            this.removeAlert();
            this.loading = false;
          });
    },
    getEmbedUrl: function(song){
      var link = song.link;
      var song_id = link.split('?v=')[1];
      return 'https://www.youtube.com/embed/' + song_id
    },
    getSongID: function(song){
      var link = song.link;
      var song_id = link.split('?v=')[1];
      return song_id
    },
    showPreview: function(song){
      this.iframe_url = this.getEmbedUrl(song) + "?autoplay=1&loop=1&rel=0&wmode=transparent";
      this.prev_iframe_url = "";
    },
    showActions: function(song){
      this.selected_song = song;
    },
    songNumber: function(index){
      return index + 1
    },
    playPreview: function(song){
      this.selected_song = song;
      this.prev_iframe_url = this.getEmbedUrl(this.selected_song) + "?autoplay=1&loop=1&rel=0&wmode=transparent";
      this.iframe_url = "";
      this.videoId = this.getSongID(song);
      this.show_video_box = true;
    },
    scrollTop: function(){
      window.scrollTo(0,0);
      this.hide_scroller = true;
    },
    showScroller: function(evt, el){
      this.hide_scroller = true;
      if (window.scrollY > 50) {
        this.hide_scroller = false;
      }
    },
    ready (event) {
      this.player = event.target
    },
    playing (event) {
      // The player is playing a video.
    },
    ended (event) {
      console.log('video ended');
      console.log(this.selected_song);
      // find the next song and play it
      this.getNextSong(this.selected_song.id);
    },
    closeVideo: function(){
      this.show_video_box = false;
    },
    backupMusic: function(){
      this.loading = true;
      axios.post('/api/backup-music/')
          .then(() => {
            this.show_alert_msg = true;
            this.message = "Songs backed up to Dropbox!";
            this.loading = false;
            this.removeAlert();
          })
          .catch((error) => {
            this.show_alert_msg = true;
            this.message = "An error occurred! " + error;
            this.loading = false;
            this.removeAlert();
          });
    },
    filterSongsByCategory: function(category){
      this.selected_category = category;
      this.title = this.selected_category['text'];
      this.filter_loading = true;
      const path = '/songs/?category=' + category.value;
      axios.get(path)
        .then((response) => {
          this.songs = response.data;
          this.filter_loading = false;
          this.spotify_tracks = [];
        })
        .catch((error) => {
          console.error(error);
          this.filter_loading = false;
        });
    },
    getActiveCategory(category) {
        if (category === this.selected_category){
            return 'active-cat'
        }
    },
    getAllCategoryClass(){
        if (this.selected_category ==='all' || this.selected_category === ''){
            return 'active-cat'
        }
    },
    getSongClass(song){
        if (this.active_song === song){
          return 'active-song'
        }
    },
    setSongSelection(song){
        this.active_song = song;
    },
    spotifyLogin(){
      const path = '/spotify/callback/';
      axios.get(path)
          .then((response) => {
              console.log(response);
          })
          .catch((error) => {
              console.log(error);
          })
    },
    getSpotifyTracks(){
      this.title = "Spotify Tracks";
      const path = '/spotify/user/tracks';
      axios.get(path)
        .then((response) => {
            console.log(response);
            this.spotify_tracks = response.data;
            this.songs = [];
            this.selected_category = null;
        })
        .catch((error) => {
            console.log(error);
        })
    },
    addSongComplete(message){
      this.getSongs();
      this.show_alert_msg = true;
      this.message = message;
      this.removeAlert();
    },
  },
  created() {
    this.getSongs();
    this.getSongCategories();
    // this.$store.dispatch('getSongs')
  },
  computed: {
    now: function(){
      return Date.now()
    },
    spotify_tracks_class(){
        if (this.spotify_tracks.length > 0){
          return 'active-cat'
        }
    }
  },
};
</script>

<style lang="scss">
  @import "../styles/music.scss";
</style>

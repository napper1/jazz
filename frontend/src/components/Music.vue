<template>
  <div class="music" v-bind:class="{ padd_top: prev_iframe_url }" v-scroll="showScroller">
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-12">
          <div class="row">
            <div class="col-sm-4">
              <h1 class="d-inline-block">
                <i class="fa fa-music" style="margin-right:5px"></i>
                Music
              </h1>
            </div>
            <div class="col-sm-3">
              <input class="form-control search_box" v-model="song_query" type="text" placeholder="Search..."
                     @keyup="lookupSong()">
            </div>
            <div class="col-sm-5">
              <div class="d-inline-block pull-right top-filters">
                <button type="button" class="btn btn-secondary btn-sm" @click="backupMusic()">Backup Songs</button>
                <button type="button" class="btn btn-success btn-sm" v-b-modal.song-modal>Add Song</button>
                <a href="https://www.abc.net.au/triplej/listen-live/double-j-player/"
                   class="btn btn-primary btn-sm" target="_blank">Double J</a>
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

          <div class="row" style="display: none;">
            <div class="col-xs-12">
              <label>Quantity</label>
              <input :type="quantity_group.field_type" v-model.number="quantity_group.selected" v-if="quantity_group.field_type=='number'">
              <input :type="quantity_group.field_type" v-model="quantity_group.selected" v-else>
            </div>
          </div>

          <alert :message="message" v-if="message"></alert>
          <div class="songs-section">
            <div class="row" v-for="(song, index) in songs" :key="index">
              <div class="col-sm-12">
                <div class="song" @mouseover="showActions(song)">
                  <div class="song_num">
                    <p class="">{{ songNumber(index) }}</p>
                  </div>
                  <img @click="showPreview(song)" v-b-modal.song-preview-modal src="https://via.placeholder.com/70" alt="" width="70" height="70">
                  <div class="song_name">
                    <h5><strong>{{ song.title }}</strong></h5>
                    <p>{{ song.artist.name }}</p>
                  </div>
                  <div class="song-actions">
                    <div v-if="selected_song === song" class="pull-left m-md-2">
                      <mycircle v-if="loading"></mycircle>
                    </div>
                    <b-dropdown id="dropdown-dropleft" dropleft text="More" class="m-md-2 pull-right" v-if="selected_song === song">
                      <b-dropdown-item @click="showPreview(song)" v-b-modal.song-preview-modal>
                        <i class="fa fa-music" aria-hidden="true"></i>
                        Preview
                      </b-dropdown-item>
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
                      <b-dropdown-item v-if="song.downloaded" class="download-song" :href="api_host + song.media_link" target="_blank">
                        <i class="fa fa-download" aria-hidden="true"></i>
                        Download to device
                      </b-dropdown-item>
                    </b-dropdown>
                  </div>
                </div>
              </div>
              <hr>
            </div>
          </div>

        </div>
      </div>
    </div>
    <b-modal ref="addSongModal"
             id="song-modal"
             title="Add a new song"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addSongForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-artist-group"
                      label="Artist:"
                      label-for="form-artist-input">
            <b-form-input id="form-artist-input"
                          type="text"
                          v-model="addSongForm.artist"
                          required
                          placeholder="Enter artist">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-link-group" label="Link:" label-for="form-link-input">
          <b-form-input id="form-link-input" type="text" v-model="addSongForm.link" placeholder="Enter link">
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editSongModal"
             id="song-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-title-group"
                      label="Title:"
                      label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-artist-group"
                      label="Artist:"
                      label-for="form-artist-input">
          <b-form-input id="form-artist-input"
                        type="text"
                        v-model="editForm.artist.name"
                        required
                        placeholder="Enter artist">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-link-group" label="Link:" label-for="form-link-input">
          <b-form-input id="form-link-input" type="text" v-model="editForm.link" placeholder="Enter link">
          </b-form-input>
        </b-form-group>
        <b-button type="submit">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
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
import 'bootstrap/dist/css/bootstrap.css';
import datePicker from 'vue-bootstrap-datetimepicker';
import 'pc-bootstrap4-datetimepicker/build/css/bootstrap-datetimepicker.css';


export default {
  name: 'Music',
  data() {
    return {
      songs: [],
      message: '',
      addSongForm: {
        title: '',
        artist: '',
        link: '',
      },
      editForm: {
        id: '',
        title: '',
        artist: '',
        link: '',
      },
      loading: false,
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
      api_host: 'http://localhost:8000',
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
    };
  },
  components: {
    alert: Alert,
    mycircle: Circle,
    RotateSquare2,
    Circle2,
    datePicker,
  },
  methods: {
    lookupSong() {
      const path = this.api_host + '/songs/?q=' + this.song_query;
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
      axios.post(this.api_host + '/api-document/', formData, {headers: {'Content-Type': 'multipart/form-data'}})
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
    getSongs() {
      const path = this.api_host + '/songs/';
      axios.get(path)
        .then((res) => {
          this.songs = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addSong(payload) {
      const path = this.api_host + '/api-add-song/';
      axios.post(path, payload)
        .then(() => {
          this.getSongs();
          this.message = "Song added!";
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getSongs();
        });
    },
    initForm() {
      this.addSongForm.title = '';
      this.addSongForm.artist = '';
      this.addSongForm.link = '';
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.artist = '';
      this.editForm.link = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addSongModal.hide();
      const payload = {
        title: this.addSongForm.title,
        artist: this.addSongForm.artist,
        link: this.addSongForm.link,
      };
      this.addSong(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addSongModal.hide();
      this.initForm();
    },
    editSong(song) {
      this.editForm = song;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editSongModal.hide();
      const payload = {
        title: this.editForm.title,
        artist: this.editForm.artist.id,
        link: this.editForm.link
      };
      this.updateSong(payload, this.editForm.id);
    },
    updateSong(payload, song_id) {
      const path = this.api_host + '/songs/' + song_id + '/';
      axios.put(path, payload)
        .then(() => {
          this.getSongs();
          this.message = "Song updated!";
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getSongs();
          this.message = "An error occurred!";
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editSongModal.hide();
      this.initForm();
    },
    removeSong(song_id) {
      const path = this.api_host + `/songs/${song_id}/`;
      axios.delete(path)
        .then(() => {
          this.getSongs();
          this.message = 'Song removed!';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getSongs();
        });
    },
    getNextSong(song_id){
      const path = this.api_host + `/api-get-next/${song_id}/`;
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
      if (this.selected_song === song) this.selected_song = null
      else this.selected_song = song
      this.loading = true;
      axios.post(this.api_host + '/download/' + song.id + '/')
          .then(() => {
            this.message = "Song downloaded to media folder!"
            this.loading = false;
            // refresh songs list
            this.getSongs();
          })
          .catch((error) => {
            this.message = "An error occurred! " + error;
            this.loading = false;
          });
    },
    getEmbedUrl: function(song){
      var link = song.link;
      var song_id = link.split('?v=')[1]
      return 'https://www.youtube.com/embed/' + song_id
    },
    getSongID: function(song){
      var link = song.link;
      var song_id = link.split('?v=')[1]
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
      axios.post(this.api_host + '/api/backup-music/')
          .then(() => {
            this.message = "Songs backed up to Dropbox!"
            this.loading = false;
          })
          .catch((error) => {
            this.message = "An error occurred! " + error;
            this.loading = false;
          });
    }
  },
  created() {
    this.getSongs();
  },
  computed: {
    now: function(){
      return Date.now()
    },
  },
};
</script>


<style>
  html, .songs-section{
    background-color: #36454f;
  }
  h1, .song, .song .song_name{
    color: #bdcad6;
  }
  .music{
    padding: 0 85px;
  }
  .download-song{
    cursor: pointer;
  }
  .table{
    background-color: rgba(255, 255, 255, 0.7);
    color: #000;
  }
  iframe {
    width: 100%;
  }
  .green{
    color: #28a745;
  }
  .song{
    display: flex;
    flex-direction: row;
    padding: 16px 0;
    border-bottom: 1px solid #f1f1f1;
    transition: all 0.3s ease-out;
  }
  .song .song_name h5{
    transition: all 0.3s ease-out;
    border-bottom: 1px solid transparent;
  }
  .song .song_name h5:after{
    content: '';
    display: block;
    position: relative;
    border-bottom: 1px solid white;
    width: 0px;
    transition: all 2s ease-out;
  }
  .song:hover{
    background: #647b8e;
  }
  .song:hover .song_name h5{
    /*border-color: #f1f1f1;*/
  }
  .song:hover .song_name h5:after{
    width: 80%;
  }
  .song .song_num{
    width: 5%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .song .song_num > *{
    margin: 0;
  }
  .song img{
    width: 70px;
  }
  .song .song_name{
    width: 60%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin: 0 auto;
    padding: 0;
  }
  .song .song_name > *{
    margin: 0;
  }
  .songs-section{
    margin-top: 25px;
  }
  .song .song-actions{
    width: 22%;
  }
  .top-filters{
    margin-top:20px;
  }
  .prev_iframe{
    position: fixed;
    top:0;
    right:0;
    height: 300px;
    z-index:9999;
  }
  .padd_top{
    padding-top: 350px;
  }
  #topbutton {
      position: fixed;
      opacity: 0;
      overflow: hidden;
      text-align: center;
      z-index: 99999999;
      background-color: #777777;
      color: #eeeeee;
      width: 50px;
      height: 48px;
      line-height: 48px;
      right: 30px;
      bottom: 30px;
      padding-top: 2px;
      border-top-left-radius: 10px;
      border-top-right-radius: 10px;
      border-bottom-right-radius: 10px;
      border-bottom-left-radius: 10px;
      -webkit-transition: all 0.5s ease-in-out;
      -moz-transition: all 0.5s ease-in-out;
      -ms-transition: all 0.5s ease-in-out;
      -o-transition: all 0.5s ease-in-out;
      transition: all 0.5s ease-in-out;
      cursor: pointer;
  }
  #topbutton.show {
      visibility: visible;
      cursor: pointer;
      opacity: 1.0;
  }
  #topbutton.hide{
    visibility: hidden;
  }
  #topbutton .fa{
    padding-top: 6px;
  }
  .prev_iframe .close-video{
    display: inline-block;
    position: absolute;
    right: 32px;
    top: 0;
    color: white;
    font-size: 45px;
  }
  .prev_iframe .close-video a{
    color: white;
  }

  /**
  input[type=checkbox]:checked + label img
  {
    border: 1px solid blue;
  }
   */

  .selected{
    border: 1px solid blue;
  }
  .img_modal{
    position: relative;
  }
  .img_modal .modal_btn, .bs_datepicker{
    position: absolute;
    top:0;
    left:0;
    right:0;
    bottom:0;
  }
  .img_modal .modal_btn button{
    height:100%;
    opacity:0;
  }
  .bs_datepicker input{
    height:100%;
    opacity:0;
  }
  .search_box{
    margin-top: 15px;
  }

  @media (max-width: 768px){
    .music{
      padding: 0 0;
    }
    .song img{
      margin: 0 15px;
    }
    .song .song_name{
      width: 100%;
    }
  }
</style>

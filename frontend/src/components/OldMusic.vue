<template>
  <div class="music" v-bind:class="{ padd_top: prev_iframe_url }" v-scroll="showScroller">
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-12">
          <h1 class="d-inline-block">
            <i class="fa fa-music" style="margin-right:5px"></i>
            Music
          </h1>
          <div class="d-inline-block pull-right top-filters">
            <button type="button" class="btn btn-success btn-sm" v-b-modal.song-modal>Add Song</button>
            <a href="https://www.abc.net.au/triplej/listen-live/double-j-player/"
               class="btn btn-primary btn-sm" target="_blank">Double J</a>
          </div>
          <div class="prev_iframe" v-if="prev_iframe_url">
            <iframe class="youtube_iframe" :src="prev_iframe_url" frameborder="0" width="560" height="315" autoplay allowfullscreen></iframe>
          </div>
          <hr>
          <alert :message="message" v-if="message"></alert>
          <div class="songs-section">
            <div class="row" v-for="(song, index) in songs" :key="index">
              <div class="col-sm-12">
                <div class="song" @mouseover="showActions(song)">
                  <div class="song_num">
                    <p class="">{{ songNumber(index) }}</p>
                  </div>
                  <img @mouseover="playPreview(song)" src="https://via.placeholder.com/70" alt="" width="70" height="70">
                  <div class="song_name">
                    <h5><strong>{{ song.title }}</strong></h5>
                    <p>{{ song.artist.name }}</p>
                  </div>
                  <div class="song-actions">
                    <div v-if="selected_song === song" class="pull-left m-md-2">
                      <mycircle v-if="loading"></mycircle>
                    </div>
                    <b-dropdown id="ddown1" text="More" class="m-md-2 pull-right" v-if="selected_song === song">
                      <b-dropdown-item @click="showPreview(song)" v-b-modal.song-preview-modal>
                        <i class="fa fa-music" aria-hidden="true"></i>
                        Preview
                      </b-dropdown-item>
                      <b-dropdown-item v-b-modal.song-update-modal @click="editSong(song)">Edit</b-dropdown-item>
                      <b-dropdown-item @click="onDeleteSong(song)">Delete</b-dropdown-item>
                      <b-dropdown-divider></b-dropdown-divider>
                      <b-dropdown-item @click="downloadSong(song)" class="download-song">
                        <i v-if="song.downloaded" class="fa fa-check green" aria-hidden="true"></i>
                        <i v-else class="fa fa-download" aria-hidden="true"></i>
                      </b-dropdown-item>
                    </b-dropdown>
                  </div>
                </div>
              </div>
              <hr>
            </div>
          </div>


          <table class="table table-hover" style="display: none;">
            <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Artist</th>
              <th scope="col">Download</th>
              <th scope="col">Preview</th>
              <th></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(song, index) in songs" :key="index">
              <td>{{ song.title }}</td>
              <td>{{ song.artist.name }}</td>
              <td>
                <i v-if="song.downloaded" class="fa fa-check green" aria-hidden="true"></i>
                <a v-else @click="downloadSong(song)" class="download-song">
                  <i class="fa fa-download" aria-hidden="true"></i>
                </a>
                <div v-if="selected_song === song">
                  <mycircle v-if="loading"></mycircle>
                </div>
              </td>
              <td>
                <button type="button" class="btn btn-primary btn-sm" v-b-modal.song-preview-modal
                @click="showPreview(song)">Preview</button>
              </td>
              <td>
                <button type="button" class="btn btn-warning btn-sm" v-b-modal.song-update-modal
                @click="editSong(song)">Edit</button>
                <button type="button" class="btn btn-danger btn-sm"
                @click="onDeleteSong(song)">Delete</button>
              </td>
            </tr>
            </tbody>
          </table>



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
    };
  },
  components: {
    alert: Alert,
    mycircle: Circle,
    RotateSquare2,
    Circle2,
  },
  methods: {
    getSongs() {
      const path = 'http://localhost:8000/songs/';
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
      const path = 'http://localhost:8000/api-add-song/';
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
      const path = 'http://localhost:8000/songs/' + song_id + '/';
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
      const path = `http://localhost:8000/songs/${song_id}/`;
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
    onDeleteSong(song) {
      this.removeSong(song.id);
    },
    downloadSong: function(song){
      if (this.selected_song === song) this.selected_song = null
      else this.selected_song = song
      this.loading = true;
      axios.post('http://localhost:8000/download/' + song.id + '/')
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
    },
    scrollTop: function(){
      window.scrollTo(0,0);
      this.hide_scroller = true;
    },
    showScroller: function(evt, el){
      console.log('in');
      this.hide_scroller = true;
      if (window.scrollY > 50) {
        this.hide_scroller = false;
      }
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
  .music{
    padding: 0 85px;
  }
  .songs-section{
    margin-top: 25px;
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
  }
  .song:hover{
    background: #fafafa;
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
    background: #fff;
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
    left:0;
    right:0;
    height: 300px;
    z-index:9999;
  }
  .padd_top{
    padding-top: 300px;
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
</style>

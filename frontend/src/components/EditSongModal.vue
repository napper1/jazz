<template>
  <b-modal ref="editSongModal"
           id="song-update-modal"
           title="Update"
           @show="initModal"
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
      <b-form-group id="form-song-category-group"
                      label="Category:"
                      label-for="form-category-input">
          <b-form-select v-model="editForm.selected_category" :options="song_categories"></b-form-select>
      </b-form-group>
      <b-button type="submit">Update</b-button>
      <b-button @click="hideEditModal" variant="danger">Cancel</b-button>
    </b-form>
  </b-modal>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "EditSongModal",
        props: {
            song_categories: {
                type: Array,
                required: true,
            },
            song: {
                type: Object,
                required: false,
            },
        },
        data(){
          return{
            editForm: {
              id: '',
              title: '',
              artist: '',
              link: '',
              selected_category: '',
            },
          }
        },
        methods: {
          onSubmitUpdate(evt) {
            evt.preventDefault();
            this.$refs.editSongModal.hide();
            const payload = {
              title: this.editForm.title,
              artist: this.editForm.artist.id,
              link: this.editForm.link,
              category: this.editForm.selected_category,
            };
            this.updateSong(payload, this.editForm.id);
          },
          updateSong(payload, song_id) {
            const path = `/songs/${song_id}/`;
            axios.put(path, payload)
              .then(() => {
                this.$emit('refresh-songs', 'Song updated!')
              })
              .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
              });
          },
          onResetUpdate(evt) {
            evt.preventDefault();
            this.$refs.editSongModal.hide();
            this.initForm();
          },
          initForm() {
            this.editForm.id = '';
            this.editForm.title = '';
            this.editForm.artist = '';
            this.editForm.link = '';
            this.editForm.selected_category = '';
          },
          hideEditModal() {
            this.$refs['editSongModal'].hide();
          },
          initModal(){
              console.log('init modal')
              // console.log(this.song_form)
              this.editForm = this.song;
              if (this.song.category){
                this.editForm.selected_category = this.song.category;
              }
          }
        }
    }
</script>

<style scoped>

</style>
